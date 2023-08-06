from contextlib import nested
from deployer.host import Host
from deployer.exceptions import ExecCommandFailed
from deployer.utils import isclass, esc1
from functools import wraps

__all__ = ('HostContainer', 'HostsContainer', )


class HostsContainer(object):
    """
    Proxy to a group of :class:`~deployer.host.base.Host` instances.

    For instance, if you have a role, name 'www' inside the container, you
    could do:

    ::

        host_container.run(...)
        host_container[0].run(...)
        host_container.filter('www')[0].run(...)

    Typically, you get a :class:`~deployer.host_container.HostsContainer` class
    by accessing the :attr:`~deployer.node.base.Env.hosts` property of an
    :class:`~deployer.node.base.Env` (:class:`~deployer.node.base.Node`
    wrapper.)
    """
    def __init__(self, hosts, pty=None, logger=None, is_sandbox=False):
        # the hosts parameter is a dictionary, mapping roles to <Host> instances, or lists
        # of <Host>-instances.
        # e.g. hosts = { 'www': [ <host1>, <host2> ], 'queue': <host3> }
        self._logger = logger
        self._pty = pty
        self._sandbox = is_sandbox

        # Create
        self._hosts = { }

        def get(h):
            # Create host instance if class was given. Otherwise return
            # instance.
            if isclass(h):
                assert issubclass(h, Host)
                return h(pty=pty, logger=logger)
            else:
                assert isinstance(h, Host)
                return h

        for k, v in hosts.items():
            # A value should be a list of Host classes.
            assert isinstance(v, set)
            self._hosts[k] = { get(h) for h in v }

        # Validate hosts. No two host with the same slug can occur in a
        # same role within a container.
        for k, v in hosts.items():
            slugs = { } # Slug -> Host class
            for h in v:
                if h.slug in slugs and h != slugs[h.slug]:
                    raise Exception('Duplicate host slug %s found in HostsContainer.' % h.slug)
                else:
                    slugs[h.slug] = h

    @property
    def _all(self):
        return [ h for v in self._hosts.values() for h in v ]

    @classmethod
    def from_definition(cls, hosts_class, **kw):
        """
        Create a :class:`HostsContainer` from a Hosts class.
        """
        hosts = { }
        for k in dir(hosts_class):
            v = getattr(hosts_class, k)

            if isinstance(v, HostsContainer):
                # This happens when we define Hosts inline in an action, to be
                # initialized, e.g. by initialize_node.
                hosts[k] = v.get_hosts()
            elif isclass(v) and issubclass(v, Host):
                hosts[k] = { v }
            elif isinstance(v, (set, tuple)):
                for h in v:
                    assert issubclass(h, Host)
                hosts[k] = { h for h in v }
            elif not k.startswith('_'):
                raise TypeError('Invalid attribute in host definition %s: %r=%r' % (hosts_class, k, v))

        return cls(hosts, **kw)

    def get_hosts(self):
        """
        Return a set of :class:`deployer.host.Host` classes that appear in this
        container.  Each :class:`deployer.host.Host` class will abviously
        appear only once in the set, even when it appears in several roles.
        """
        return { h.__class__ for l in self._hosts.values() for h in l }

    def get_hosts_as_dict(self):
        """
        Return a dictionary which maps all the roles to the set of
        :class:`deployer.host.Host` classes for each role.
        """
        return { k: { h.__class__ for h in l } for k, l in self._hosts.items() }

    def __repr__(self):
        return ('<%s\n' % self.__class__.__name__ +
                ''.join('   %s: [%s]\n' % (r, ','.join(h.slug for h in self.filter(r))) for r in self.roles) +
                '>')

    def __eq__(self, other):
        """
        Return ``True`` when the roles/hosts are the same.
        """
        # We can't do this: host instances are created during initialisation.
        raise NotImplementedError('There is no valid definition for HostsContainer equality.')

    def _new(self, hosts):
        return HostsContainer(hosts, self._pty, self._logger, self._sandbox)

    def _new_1(self, host):
        return HostContainer({ 'host': {host} }, self._pty, self._logger, self._sandbox)

    def __len__(self):
        """
        Returns the amount of :class:`deployer.host.Host` instances in this
        container. If a host appears in several roles, each appearance will be
        taken in account.
        """
        return sum(len(v) for v in self._hosts.values())

    def __nonzero__(self):
        return len(self) > 0

    @property
    def roles(self):
        return sorted(self._hosts.keys())

    def __contains__(self, host):
        """
        Return ``True`` when this host appears in this host container.
        """
        raise Exception('No valid implementation for this...') # XXX

#        assert isinstance(host, (Host, HostContainer))
#
#        if isinstance(host, HostContainer):
#            host = host._host
#        return host.__class__ in self.get_hosts()

    def filter(self, *roles):
        """
        Returns a new HostsContainer instance, containing only the hosts
        matching this filter. The hosts are passed by reference, so if you'd
        call `cd()` on the returned container, it will also effect the hosts in
        this object.

        Examples:

        ::

            hosts.filter('role1', 'role2')
        """
        assert all(isinstance(r, basestring) for r in roles), TypeError('Unknown host filter %r' % roles)

        return self._new({ r: self._hosts.get(r, set()) for r in roles })

    def __getitem__(self, index):
        """
        Mostly for backwards-compatibility.

        You can use the [0] index operation, but as a HostContainer contains a
        set of hosts, there is no definition of the 'first' host in a set, so
        you shouldn't trust the order, and you shouldn't rely on the fact that it'll
        be always the same host that will be returned.
        This can be useful if you want to retrieve a value from one node in an
        array, but when it's not important which one.


        :returns: :class:`HostContainer`;
        """
        if index != 0:
            raise Exception('Only [0] index operation is allowed on HostsContainer instance.')

        hosts = list(self._all)

        if len(hosts) == 0:
            raise IndexError

        return self._new_1(hosts[index])

    def __iter__(self):
        for h in self._all:
            yield self._new_1(h)

    def expand_path(self, path):
        return [ h.expand_path(path) for h in self._all ]

    def run(self, *a, **kw):
        """run(command, sandbox=False, interactive=True, user=None, ignore_exit_status=False, initial_input=None)

        Call :func:`~deployer.host.base.Host.run` with this parameters on every
        :class:`~deployer.host.base.Host` in this container. It can be executed
        in parallel when we have multiple hosts.

        :returns: An array of all the results.
        """
        # First create a list of callables
        def closure(host):
            def call(pty):
                assert pty

                kw2 = dict(**kw)
                kw2.setdefault('sandbox', self._sandbox)

                new_host = host.copy(pty=pty)
                return new_host.run(*a, **kw2)
            return call

        callables = map(closure, self._all)

        # When addressing multiple hosts and auxiliary ptys are available,
        # do a parallel run.
        if len(callables) > 1 and self._pty.auxiliary_ptys_are_available:
            # Run in auxiliary ptys, wait for them all to finish,
            # and return result.
            print 'Forking to %i pseudo terminals...' % len(callables)

            # Wait for the forks to finish
            fork_result = self._pty.run_in_auxiliary_ptys(callables)
            fork_result.join()
            result = fork_result.result

            # Return result.
            print ''.join(result) # (Print it once more in the main terminal, not really sure whether we should do that.)
            return result

        # Otherwise, run all serially.
        else:
            return [ c(self._pty) for c in callables ]

    def sudo(self, *args, **kwargs):
        """sudo(command, sandbox=False, interactive=True, user=None, ignore_exit_status=False, initial_input=None)

        Call :func:`~deployer.host.base.Host.sudo` with this parameters on every
        :class:`~deployer.host.base.Host` in this container. It can be executed
        in parallel when we have multiple hosts.

        :returns: An array of all the results.
        """
        kwargs['use_sudo'] = True
        return HostsContainer.run(self, *args, **kwargs)
                    # NOTE: here we use HostsContainer instead of self, to be
                    #       sure that we don't call te overriden method in
                    #       HostContainer.

    def prefix(self, command):
        """
        Call :func:`~deployer.host.base.HostContext.prefix` on the
        :class:`~deployer.host.base.HostContext` of every host.

        ::

            with host.prefix('workon environment'):
                host.run('./manage.py migrate')
        """
        return nested(* [ h.host_context.prefix(command) for h in self._all ])

    def cd(self, path, expand=False):
        """
        Execute commands in this directory. Nesting of cd-statements is
        allowed.

        Call :func:`~deployer.host.base.HostContext.cd` on the
        :class:`~deployer.host.base.HostContext` of every host.

        ::

            with host_container.cd('directory'):
                host_container.run('ls')
        """
        return nested(* [ h.host_context.cd(path, expand=expand) for h in self._all ])

    def env(self, variable, value, escape=True):
        """
        Sets an environment variable.

        This calls :func:`~deployer.host.base.HostContext.env` on the
        :class:`~deployer.host.base.HostContext` of every host.

        ::

            with host_container.cd('VAR', 'my-value'):
                host_container.run('echo $VAR')
        """
        return nested(* [ h.host_context.env(variable, value, escape=escape) for h in self._all ])

    def getcwd(self):
        """ Calls :func:`~deployer.host.base.Host.getcwd` for every host and return the result as an array. """
        return [ h._host.getcwd() for h in self ]

    #
    # Commands
    # (these don't need sandboxing.)
    #
    def exists(self, filename, use_sudo=True):
        """
        Returns an array of boolean values that represent whether this a file
        with this name exist for each host.
        """
        def on_host(container):
            return container._host.exists(filename, use_sudo=use_sudo)

        return map(on_host, self)

    def has_command(self, command, use_sudo=False):
        """
        Test whether this command can be found in the bash shell, by executing a 'which'
        """
        def on_host(container):
            try:
                container.run("which '%s'" % esc1(command), use_sudo=use_sudo,
                                interactive=False, sandbox=False)
                return True
            except ExecCommandFailed:
                return False

        return map(on_host, self)

    @property
    def hostname(self): # TODO: Deprecate!!!
        with self.cd('/'):
            return self.run('hostname', sandbox=False).strip()

    @property
    def is_64_bit(self): # TODO: deprecate!!!
        with self.cd('/'):
            return 'x86_64' in self._run_silent('uname -m', sandbox=False)


class HostContainer(HostsContainer):
    """
    Similar to :class:`~deployer.host_container.HostsContainer`, but wraps only
    around exactly one :class:`~deployer.host.base.Host`.
    """
    @property
    def _host(self):
        """
        This host container has only one host.
        """
        assert len(self) == 1, AssertionError('Found multiple hosts in HostContainer')
        return self._all[0]

    @property
    def slug(self):
        return self._host.slug

    @wraps(Host.get_file)
    def get_file(self, *args, **kwargs):
        kwargs['sandbox'] = self._sandbox
        return self._host.get_file(*args, **kwargs)

    @wraps(Host.put_file)
    def put_file(self, *args, **kwargs):
        kwargs['sandbox'] = self._sandbox
        return self._host.put_file(*args, **kwargs)

    @wraps(Host.open)
    def open(self, *args, **kwargs):
        kwargs['sandbox'] = self._sandbox
        return self._host.open(*args, **kwargs)

    @wraps(HostsContainer.run)
    def run(self, *a, **kw):
        return HostsContainer.run(self, *a, **kw)[0]

    @wraps(HostsContainer.sudo)
    def sudo(self, *a, **kw):
        return HostsContainer.sudo(self, *a, **kw)[0]

    @wraps(HostsContainer.getcwd)
    def getcwd(self):
        return HostsContainer.getcwd(self)[0]

    def start_interactive_shell(self, command=None, initial_input=None):
        if not self._sandbox:
            return self._host.start_interactive_shell(command=command, initial_input=initial_input)
        else:
            print 'Interactive shell is not available in sandbox mode.'

    def __getattr__(self, name):
        """
        Proxy to the Host object. Following commands can be
        accessed when this hostcontainer contains exactly one host.
        """
        return getattr(self._host, name)

    @wraps(HostsContainer.expand_path)
    def expand_path(self, *a, **kw):
        return HostsContainer.expand_path(self, *a, **kw)[0]

    def exists(self, filename, use_sudo=True):
        """
        Returns ``True`` when this file exists on the hosts.
        """
        return HostsContainer.exists(self, filename, use_sudo=use_sudo)[0]

    def has_command(self, command, use_sudo=False):
        """
        Test whether this command can be found in the bash shell, by executing
        a ``which`` Returns ``True`` when the command exists.
        """
        return HostsContainer.has_command(self, command, use_sudo=use_sudo)[0]
