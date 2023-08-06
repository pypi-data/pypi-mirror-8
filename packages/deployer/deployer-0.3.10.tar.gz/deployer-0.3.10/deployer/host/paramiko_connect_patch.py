"""
Patch for the paramiko SSHClient.connect function.
The only difference is that it calls a progress bar callback.
"""

from paramiko.config import SSH_PORT
from paramiko.util import retry_on_signal
import socket
import getpass

from paramiko.transport import Transport
from paramiko.resource import ResourceManager
from paramiko.ssh_exception import BadHostKeyException
from paramiko.py3compat import string_types


def connect(self, hostname, port=SSH_PORT, username=None, password=None, pkey=None,
            key_filename=None, timeout=None, allow_agent=True, look_for_keys=True,
            compress=False, sock=None, gss_auth=False, gss_kex=False,
            gss_deleg_creds=True, gss_host=None, banner_timeout=None,
            progress_bar_callback=None):
    """
    Patched ``paramiko.client.SSHClient.connect``.
    This adds callbacks for the connection progress bar.
    """
    if not sock:
        progress_bar_callback(1) # Resolving DNS

        for (family, socktype, proto, canonname, sockaddr) in socket.getaddrinfo(hostname, port, socket.AF_UNSPEC, socket.SOCK_STREAM):
            if socktype == socket.SOCK_STREAM:
                af = family
                addr = sockaddr
                break
        else:
            # some OS like AIX don't indicate SOCK_STREAM support, so just guess. :(
            af, _, _, _, addr = socket.getaddrinfo(hostname, port, socket.AF_UNSPEC, socket.SOCK_STREAM)

        progress_bar_callback(2) # Creating socket
        sock = socket.socket(af, socket.SOCK_STREAM)
        if timeout is not None:
            try:
                sock.settimeout(timeout)
            except:
                pass
        retry_on_signal(lambda: sock.connect(addr))

    progress_bar_callback(3) # Creating transport
    t = self._transport = Transport(sock, gss_kex=gss_kex, gss_deleg_creds=gss_deleg_creds)
    t.use_compression(compress=compress)
    if gss_kex and gss_host is None:
        t.set_gss_host(hostname)
    elif gss_kex and gss_host is not None:
        t.set_gss_host(gss_host)
    else:
        pass
    if self._log_channel is not None:
        t.set_log_channel(self._log_channel)
    if banner_timeout is not None:
        t.banner_timeout = banner_timeout
    t.start_client()
    ResourceManager.register(self, t)

    progress_bar_callback(4) # Exchange keys
    server_key = t.get_remote_server_key()
    keytype = server_key.get_name()

    if port == SSH_PORT:
        server_hostkey_name = hostname
    else:
        server_hostkey_name = "[%s]:%d" % (hostname, port)

    # If GSS-API Key Exchange is performed we are not required to check the
    # host key, because the host is authenticated via GSS-API / SSPI as
    # well as our client.
    if not self._transport.use_gss_kex:
        our_server_key = self._system_host_keys.get(server_hostkey_name,
                                                     {}).get(keytype, None)
        if our_server_key is None:
            our_server_key = self._host_keys.get(server_hostkey_name,
                                                 {}).get(keytype, None)
        if our_server_key is None:
            # will raise exception if the key is rejected; let that fall out
            self._policy.missing_host_key(self, server_hostkey_name,
                                          server_key)
            # if the callback returns, assume the key is ok
            our_server_key = server_key

        if server_key != our_server_key:
            raise BadHostKeyException(hostname, server_key, our_server_key)

    if username is None:
        username = getpass.getuser()

    if key_filename is None:
        key_filenames = []
    elif isinstance(key_filename, string_types):
        key_filenames = [key_filename]
    else:
        key_filenames = key_filename
    if gss_host is None:
        gss_host = hostname

    progress_bar_callback(5) # Authenticate
    self._auth(username, password, pkey, key_filenames, allow_agent,
               look_for_keys, gss_auth, gss_kex, gss_deleg_creds, gss_host)
