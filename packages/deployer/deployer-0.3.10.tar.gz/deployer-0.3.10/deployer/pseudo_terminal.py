"""
.. note:: This module is mainly for internal use.

Pty implements a terminal abstraction. This can be around the default stdin/out
pair, but also around a pseudo terminal that was created through the
``openpty`` system call.
"""

import StringIO
import array
import fcntl
import os
import select as _select
import sys
import termios
import logging


class Pty(object):
    """
    Terminal abstraction around a stdin/stdout pair.

    Contains helper function, for opening an additional Pty,
    if parallel deployments are supported.

    :stdin: The input stream. (``sys.__stdin__`` by default)
    :stdout: The output stream. (``sys.__stdout__`` by default)
    :interactive: When ``False``, we should never ask for input during
                         the deployment. Choose default options when possible.
    """
    def __init__(self, stdin=None, stdout=None, interactive=True, term_var=''):
        self._stdin = stdin or sys.__stdin__
        self._stdout = stdout or sys.__stdout__
        self._term_var = term_var
        self.interactive = interactive
        self.set_ssh_channel_size = None

    @property
    def stdin(self):
        """ Return the input file object. """
        return self._stdin

    @property
    def stdout(self):
        """ Return the output file object. """
        return self._stdout

    def get_size(self):
        # Thanks to fabric (fabfile.org), and
        # http://sqizit.bartletts.id.au/2011/02/14/pseudo-terminals-in-python/
        """
        Get the size of this pseudo terminal.

        :returns: A (rows, cols) tuple.
        """
        if self.stdout.isatty():
            # Buffer for the C call
            buf = array.array('h', [0, 0, 0, 0 ])

            # Do TIOCGWINSZ (Get)
            fcntl.ioctl(self.stdout.fileno(), termios.TIOCGWINSZ, buf, True)

            # Return rows, cols
            return buf[0], buf[1]
        else:
            # Default value
            return 24, 80

    def get_width(self):
        """
        Return the width.
        """
        return self.get_size()[1]

    def get_height(self):
        """
        Return the height.
        """
        return self.get_size()[0]

    def set_term_var(self, value):
        self._term_var = value

    def get_term_var(self):
        return self._term_var

    def set_size(self, rows, cols):
        """
        Set terminal size.

        (This is also mainly for internal use. Setting the terminal size
        automatically happens when the window resizes. However, sometimes the process
        that created a pseudo terminal, and the process that's attached to the output window
        are not the same, e.g. in case of a telnet connection, or unix domain socket, and then
        we have to sync the sizes by hand.)
        """
        if self.stdout.isatty():
            # Buffer for the C call
            buf = array.array('h', [rows, cols, 0, 0 ])

            # Do: TIOCSWINSZ (Set)
            fcntl.ioctl(self.stdout.fileno(), termios.TIOCSWINSZ, buf)

            self.trigger_resize()

    def trigger_resize(self):
        # Call size setter for SSH channel
        if self.set_ssh_channel_size:
            self.set_ssh_channel_size()

    @property
    def auxiliary_ptys_are_available(self):
        # Override this when secondary pty's are available.
        return False

    def run_in_auxiliary_ptys(self, callbacks):
        """
        For each callback, open an additional terminal, and call it with the
        new 'pty' as parameter. The callback can potentially run in another
        thread.

        The default behaviour is not in parallel, but sequential.
        Socket_server however, inherits this pty, and overrides this function
        for parrallel execution.

        :param callbacks: A list of callables.
        """
        logging.info('Could not open auxiliary pty. Running sequential.')

        # This should be overriden by other PTY objects, for environments
        # which support parallellism.

        class ForkResult(object):
            def __init__(s):
                # The callbacks parameter can be either a single callable, or a list
                if callable(callbacks):
                    s.result = callbacks(self)
                else:
                    s.result = [ c(self) for c in callbacks ]

            def join(s):
                pass # Wait for the thread to finish. No thread here.

        return ForkResult()


class DummyPty(Pty):
    """
    Pty compatible object which insn't attached to an interactive terminal, but
    to dummy StringIO instead.

    This is mainly for unit testing, normally you want to see the execution in
    your terminal.
    """
    def __init__(self, input_data=''):
        # StringIO for stdout
        self._output = StringIO.StringIO()
        self._input_data = input_data
        self._size = (40, 80)
        self._pipe = None

        Pty.__init__(self, None, self._output, interactive=False)

    @property
    def stdin(self):
        # Lazy pipe creation.
        if not self._pipe:
            self._pipe = self._make_pipe()
        return self._pipe

    def _make_pipe(self):
        """
        Create a pipe on which the input data is written. Return the output
        data. (Select will be used on this -- so StringIO won't work.)
        """
        r, w = os.pipe()

        with os.fdopen(w, 'w') as w:
            w.write(self._input_data)

        return os.fdopen(r, 'r')

    def __del__(self):
        if self._pipe:
            self._pipe.close()
            self._pipe = None

    def get_size(self):
        return self._size

    def set_size(self, rows, cols):
        self._size = (rows, cols)

    def get_output(self):
        return self._output.getvalue()

# Alternative pty_size implementation. (Will spawn a child process, so less
# efficient.)
def _pty_size(self):
    """
    Returns (height, width)
    """
    height, width = os.popen('stty size', 'r').read().split()
    return int(height), int(width)


def select(*args, **kwargs):
    """
    Wrapper around select.select.

    When the SIGWINCH signal is handled, other system calls, like select
    are aborted in Python. This wrapper will retry the system call.
    """
    import errno

    while True:
        try:
            return _select.select(*args, **kwargs)
        except Exception as e:
            # Retry select call when EINTR
            if e.args and e.args[0] == errno.EINTR:
                continue
            else:
                raise
