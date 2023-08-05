#!/usr/bin/env python

"""Small wrapper library over paramiko that allows for parallel execution of SSH commands on remote hosts and executing simple single host commands over SSH.

parallel-ssh uses asychronous network requests - there is *no* multi-threading or multi-processing used.

This is a *requirement* for commands on many (hundreds/thousands/hundreds of thousands) of hosts which would grind a system to a halt simply by having so many processes/threads all wanting to execute if done with multi-threading/processing.

See :mod:`pssh.SSHClient` and :mod:`pssh.ParallelSSHClient` for class documentation.

Copyright (C) 2014 Panos Kittenis

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation, version 2.1.

This library is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
Lesser General Public License for more details.

You should have received a copy of the GNU Lesser General Public
License along with this library; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
"""

import logging
import gevent.pool
from gevent import socket
from gevent import monkey
monkey.patch_all()
import paramiko
import os

host_logger = logging.getLogger('host_logging')
handler = logging.StreamHandler()
host_log_format = logging.Formatter('%(message)s')
handler.setFormatter(host_log_format)
host_logger.addHandler(handler)
host_logger.setLevel(logging.INFO)
NUM_RETRIES = 3

logger = logging.getLogger(__name__)
    
class UnknownHostException(Exception):
    """Raised when a host is unknown (dns failure)"""
    pass


class ConnectionErrorException(Exception):
    """Raised on error connecting (connection refused/timed out)"""
    pass


class AuthenticationException(Exception):
    """Raised on authentication error (user/password/ssh key error)"""
    pass


class ProxyCommandException(Exception):
    """Raised on ProxyCommand error - ProxyCommand configured exited with error"""
    pass


class SSHClient(object):
    """Wrapper class over paramiko.SSHClient with sane defaults
    Honours ~/.ssh/config and /etc/ssh/ssh_config entries for host username \
    overrides"""

    def __init__(self, host,
                 user=None, password=None, port=None,
                 pkey=None, forward_ssh_agent=True,
                 _agent=None):
        """Connect to host honouring any user set configuration in ~/.ssh/config \
        or /etc/ssh/ssh_config
         
        :param host: Hostname to connect to
        :type host: str
        :param user: (Optional) User to login as. Defaults to logged in user or \
        user from ~/.ssh/config if set
        :type user: str
        :param password: (Optional) Password to use for login. Defaults to\
        no password
        :type password: str
        :param port: (Optional) Port number to use for SSH connection. Defaults\
        to None which uses SSH default
        :type port: int
        :param pkey: (Optional) Client's private key to be used to connect with
        :type pkey: :mod:`paramiko.PKey`
        :param forward_ssh_agent: (Optional) Turn on SSH agent forwarding - \
        equivalent to `ssh -A` from the `ssh` command line utility. \
        Defaults to True if not set.
        :type forward_ssh_agent: bool
        :param _agent: (Optional) Override SSH agent object with the provided. \
        This allows for overriding of the default paramiko behaviour of \
        connecting to local SSH agent to lookup keys with our own SSH agent. \
        Only really useful for testing, hence the internal variable prefix.
        :type _agent: :mod:`paramiko.agent.Agent`
        :raises: :mod:`pssh.AuthenticationException` on authentication error
        :raises: :mod:`pssh.UnknownHostException` on DNS resolution error
        :raises: :mod:`pssh.ConnectionErrorException` on error connecting
        :raises: :mod:`pssh.ProxyCommandException` on error with ProxyCommand configured
        """
        ssh_config = paramiko.SSHConfig()
        _ssh_config_file = os.path.sep.join([os.path.expanduser('~'),
                                             '.ssh',
                                             'config'])
        # Load ~/.ssh/config if it exists to pick up username, ProxyCommand
        # and host address if set
        if os.path.isfile(_ssh_config_file):
            ssh_config.parse(open(_ssh_config_file))
        host_config = ssh_config.lookup(host)
        resolved_address = (host_config['hostname'] if
                            'hostname' in host_config
                            else host)
        _user = host_config['user'] if 'user' in host_config else None
        user = user if user else _user
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.MissingHostKeyPolicy())
        self.forward_ssh_agent = forward_ssh_agent
        self.client = client
        self.channel = None
        self.user = user
        self.password = password
        self.pkey = pkey
        self.port = port if port else 22
        self.host = resolved_address
        self.proxy_command = paramiko.ProxyCommand(host_config['proxycommand']) if 'proxycommand' in \
                             host_config else None
        if self.proxy_command:
            logger.debug("Proxy configured for destination host %s - ProxyCommand: '%s'",
                         self.host, " ".join(self.proxy_command.cmd),)
        if _agent:
            self.client._agent = _agent
        self._connect()

    def _connect(self, retries=1):
        """Connect to host, throw UnknownHost exception on DNS errors"""
        try:
            self.client.connect(self.host, username=self.user,
                                password=self.password, port=self.port,
                                pkey=self.pkey,
                                sock=self.proxy_command)
        except socket.gaierror, e:
            logger.error("Could not resolve host '%s' - retry %s/%s",
                         self.host, retries, NUM_RETRIES)
            while retries < NUM_RETRIES:
                gevent.sleep(5)
                return self._connect(retries=retries+1)
            raise UnknownHostException("%s - %s" % (str(e.args[1]),
                                                    self.host,))
        except socket.error, e:
            logger.error("Error connecting to host '%s:%s' - retry %s/%s",
                         self.host, self.port, retries, NUM_RETRIES)
            while retries < NUM_RETRIES:
                gevent.sleep(5)
                return self._connect(retries=retries+1)
            raise ConnectionErrorException("%s for host '%s:%s' - retry %s/%s",
                                           str(e.args[1]), self.host, self.port,
                                           retries, NUM_RETRIES,)
        except paramiko.AuthenticationException, e:
            raise AuthenticationException(e)
        except paramiko.ProxyCommandFailure, e:
            logger.error("Error executing ProxyCommand - %s", e.message,)
            raise ProxyCommandException(e.message)

    def exec_command(self, command, sudo=False, **kwargs):
        """Wrapper to :mod:`paramiko.SSHClient.exec_command`

        Opens a new SSH session with a pty and runs command with given \
        `kwargs` if any. Greenlet then yields (sleeps) while waiting for \
        command to finish executing or channel to close indicating the same.

        :param command: Shell command to execute
        :type command: str
        :param sudo: (Optional) Run with sudo. Defaults to False
        :type sudo: bool
        :param kwargs: (Optional) Keyword arguments to be passed to remote \
        command
        :type kwargs: dict
        :rtype: Tuple of `(channel, hostname, stdout, stderr)`. \
        Channel is the remote SSH channel, needed to ensure all of stdout has \
        been got, hostname is remote hostname the copy is to, stdout and \
        stderr are buffers containing command output.
        """
        channel = self.client.get_transport().open_session()
        if self.forward_ssh_agent:
            agent_handler = paramiko.agent.AgentRequestHandler(channel)
        channel.get_pty()
        # stdin (unused), stdout, stderr
        (_, stdout, stderr) = (channel.makefile('wb'), channel.makefile('rb'),
                               channel.makefile_stderr('rb'))
        if sudo:
            command = 'sudo -S bash -c "%s"' % command.replace('"', '\\"')
        else:
            command = 'bash -c "%s"' % command.replace('"', '\\"')
        logger.debug("Running command %s on %s", command, self.host)
        channel.exec_command(command, **kwargs)
        logger.debug("Command finished executing")
        while not (channel.recv_ready() or channel.closed):
            gevent.sleep(.2)
        return channel, self.host, stdout, stderr

    def _make_sftp(self):
        """Make SFTP client from open transport"""
        transport = self.client.get_transport()
        transport.open_session()
        return paramiko.SFTPClient.from_transport(transport)

    def mkdir(self, sftp, directory):
        """Make directory via SFTP channel
        
        :param sftp: SFTP client object
        :type sftp: :mod:`paramiko.SFTPClient`
        :param directory: Remote directory to create
        :type directory: str

        Catches and logs at error level remote IOErrors on creating directory."""
        try:
            sftp.mkdir(directory)
        except IOError, error:
            logger.error("Error occured creating directory on %s - %s",
                         self.host, error)

    def copy_file(self, local_file, remote_file):
        """Copy local file to host via SFTP/SCP

        Copy is done natively using SFTP/SCP version 2 protocol, no scp command \
        is used or required.

        :param local_file: Local filepath to copy to remote host
        :type local_file: str
        :param remote_file: Remote filepath on remote host to copy file to
        :type remote_file: str
        """
        sftp = self._make_sftp()
        destination = remote_file.split(os.path.sep)
        remote_file = os.path.sep.join(destination)
        destination = destination[:-1]
        for directory in destination:
            try:
                sftp.stat(directory)
            except IOError:
                self.mkdir(sftp, directory)
        try:
            sftp.put(local_file, remote_file)
        except Exception, error:
            logger.error("Error occured copying file to host %s - %s",
                         self.host, error)
        else:
            logger.info("Copied local file %s to remote destination %s:%s",
                        local_file, self.host, remote_file)

class ParallelSSHClient(object):
    """Uses :mod:`pssh.SSHClient`, performs tasks over SSH on multiple hosts in \
    parallel.

    Connections to hosts are established in parallel when ``exec_command`` is called,
    therefor any connection and/or authentication exceptions will happen on the
    call to ``exec_command`` and need to be caught."""

    def __init__(self, hosts,
                 user=None, password=None, port=None, pkey=None,
                 forward_ssh_agent=True,
                 pool_size=10):
        """
        :param hosts: Hosts to connect to
        :type hosts: list(str)
        :param user: (Optional) User to login as. Defaults to logged in user or\
        user from ~/.ssh/config or /etc/ssh/ssh_config if set
        :type user: str
        :param password: (Optional) Password to use for login. Defaults to\
        no password
        :type password: str
        :param port: (Optional) Port number to use for SSH connection. Defaults\
        to None which uses SSH default
        :type port: int
        :param pkey: (Optional) Client's private key to be used to connect with
        :type pkey: :mod:`paramiko.PKey`
        :param forward_ssh_agent: (Optional) Turn on SSH agent forwarding - \
        equivalent to `ssh -A` from the `ssh` command line utility. \
        Defaults to True if not set.
        :type forward_ssh_agent: bool
        :param pool_size: (Optional) Greenlet pool size. Controls on how many\
        hosts to execute tasks in parallel. Defaults to 10
        :type pool_size: int
        :raises: :mod:`pssh.AuthenticationException` on authentication error
        :raises: :mod:`pssh.UnknownHostException` on DNS resolution error
        :raises: :mod:`pssh.ConnectionErrorException` on error connecting
        :raises: :mod:`pssh.ProxyCommandException` on error with ProxyCommand configured
        
        **Example**

        >>> from pssh import ParallelSSHClient, AuthenticationException,\
        		UnknownHostException, ConnectionErrorException
        >>> client = ParallelSSHClient(['myhost1', 'myhost2'])
        >>> try:
        >>> ... cmds = client.exec_command('ls -ltrh /tmp/aasdfasdf', sudo = True)
        >>> except (AuthenticationException, UnknownHostException, ConnectionErrorException):
        >>> ... return
        >>> output = [client.get_stdout(cmd) for cmd in cmds]
        [myhost1]     ls: cannot access /tmp/aasdfasdf: No such file or directory
        [myhost2]     ls: cannot access /tmp/aasdfasdf: No such file or directory
        >>> print output
        [{'myhost1': {'exit_code': 2}}, {'myhost2': {'exit_code': 2}}]

        **Example with returned stdout and stderr buffers**

        >>> from pssh import ParallelSSHClient, AuthenticationException,\
        		UnknownHostException, ConnectionErrorException
        >>> client = ParallelSSHClient(['myhost1', 'myhost2'])
        >>> try:
        >>> ... cmds = client.exec_command('ls -ltrh /tmp/aasdfasdf', sudo = True)
        >>> except (AuthenticationException, UnknownHostException, ConnectionErrorException):
        >>> ... return
        >>> output = [client.get_stdout(cmd, return_buffers=True) for cmd in cmds]
        >>> print output
        [{'myhost1': {'exit_code': 2,
        	      'stdout' : <generator object <genexpr>,
                      'stderr' : <generator object <genexpr>,}},
         {'myhost2': {'exit_code': 2,
         	      'stdout' : <generator object <genexpr>,
                      'stderr' : <generator object <genexpr>,}},
                      ]
        >>> for host_stdout in output:
            ... for line in host_stdout[host_output.keys()[0]]['stdout']:
                ... print line
                    ls: cannot access /tmp/aasdfasdf: No such file or directory
                    ls: cannot access /tmp/aasdfasdf: No such file or directory

        **Example with specified private key**

        >>> import paramiko
        >>> client_key = paramiko.RSAKey.from_private_key_file('user.key')
        >>> client = ParallelSSHClient(['myhost1', 'myhost2'], pkey=client_key)
        
        .. note ::
          
          **Connection persistence**
          
          Connections to hosts will remain established for the duration of the
          object's life. To close them, just `del` or reuse the object reference.
          
          >>> client = ParallelSSHClient(['localhost'])
          >>> cmds = client.exec_command('ls -ltrh /tmp/aasdfasdf')
          >>> cmds[0].join()
          
          :netstat: ``tcp        0      0 127.0.0.1:53054         127.0.0.1:22            ESTABLISHED``
          
          Connection remains active after commands have finished executing. Any \
          additional commands will use the same connection.
          
          >>> del client
          
          Connection is terminated.
        """
        self.pool = gevent.pool.Pool(size=pool_size)
        self.pool_size = pool_size
        self.hosts = hosts
        self.user = user
        self.password = password
        self.forward_ssh_agent = forward_ssh_agent
        self.port = port
        self.pkey = pkey
        # To hold host clients
        self.host_clients = dict((host, None) for host in hosts)

    def exec_command(self, *args, **kwargs):
        """Run command on all hosts in parallel, honoring self.pool_size

        :param args: Position arguments for command
        :type args: tuple
        :param kwargs: Keyword arguments for command
        :type kwargs: dict

        :rtype: List of :mod:`gevent.Greenlet`

        **Example**:
      
        >>> cmds = client.exec_command('ls -ltrh')
        
        Wait for completion, no stdout:
        
        >>> for cmd in cmds:
        >>>     cmd.join()
        
        Alternatively/in addition print stdout for each command:
        
        >>> print [get_stdout(cmd) for cmd in cmds]

        Retrieving stdout implies join, meaning get_stdout will wait
        for completion of all commands before returning output.
        
        You may call get_stdout on already completed greenlets to re-get
        their output as many times as you want."""
        return [self.pool.spawn(self._exec_command, host, *args, **kwargs)
                for host in self.hosts]
    
    def _exec_command(self, host, *args, **kwargs):
        """Make SSHClient, run command on host"""
        if not self.host_clients[host]:
            self.host_clients[host] = SSHClient(host, user=self.user,
                                                password=self.password,
                                                port=self.port, pkey=self.pkey,
                                                forward_ssh_agent=self.forward_ssh_agent)
        return self.host_clients[host].exec_command(*args, **kwargs)

    def get_stdout(self, greenlet, return_buffers=False):
        """Get/print stdout from greenlet and return exit code for host
        
        :mod:`pssh.get_stdout` will close the open SSH channel but this does
        **not** close the established connection to the remote host, only the
        authenticated SSH channel within it. This is standard practise
        in SSH when a command has finished executing. A new command
        will open a new channel which is very fast on already established
        connections.

        By default, stdout and stderr will be logged via the logger named \
        ``host_logger`` unless ``return_buffers`` is set to ``True`` in which case \
        both buffers are instead returned along with the exit status.

        :param greenlet: Greenlet object containing an \
        SSH channel reference, hostname, stdout and stderr buffers
        :type greenlet: :mod:`gevent.Greenlet`

        :param return_buffers: Flag to turn on returning stdout and stderr \
        buffers along with exit code. Defaults to off.
        :type return_buffers: bool

        :rtype: Dictionary containing ``{host: {'exit_code': exit code}}`` entry \
        for example ``{'myhost1': {'exit_code': 0}}``
        :rtype: With ``return_buffers=True``: ``{'myhost1': {'exit_code': 0,
                                                             'channel' : None or SSH channel of command if command is still executing,
         						     'stdout' : <iterable>,
                                                             'stderr' : <iterable>,}}``
        """
        channel, host, _stdout, _stderr = greenlet.get()
        stdout = self._read_output_buffer(_stdout)
        stderr = self._read_output_buffer(_stderr)
        if channel.exit_status_ready():
            channel.close()
        else:
            logger.debug("Command still executing on get_stdout call - not closing channel and returning None as exit code.")
            # If channel is not closed we cannot get full stdout/stderr so must return buffers
            return_buffers = True
        # Channel must be closed or reading stdout/stderr will block forever
        if not return_buffers and channel.closed:
            for line in stdout:
                host_logger.info("[%s]\t%s", host, line,)
            for line in stderr:
                host_logger.info("[%s] [err] %s", host, line,)
            return {host: {'exit_code': channel.recv_exit_status(),}}
        gevent.sleep(.2)
        return {host: {'exit_code': channel.recv_exit_status() if channel.exit_status_ready() else None,
                       'channel' : channel if not channel.closed else None,
                       'stdout' : stdout,
                       'stderr' : stderr, }}

    def wait_for_exit_status(self, channel):
        """Block and wait for exit status on channel.
        WARNING - this will block forever if the command executed never exits
        :rtype: int - Exit code of command executed"""
        while not channel.exit_status_ready():
            gevent.sleep(1)
        channel.close()
        return channel.recv_exit_status()

    def _read_output_buffer(self, output_buffer):
        """Read from output buffers,
        allowing coroutines to execute in between reading"""
        for line in output_buffer:
            gevent.sleep(1)
            yield line.strip()

    def copy_file(self, local_file, remote_file):
        """Copy local file to remote file in parallel
        
        :param local_file: Local filepath to copy to remote host
        :type local_file: str
        :param remote_file: Remote filepath on remote host to copy file to
        :type remote_file: str

        .. note ::
          Remote directories in `remote_file` that do not exist will be
          created as long as permissions allow.

        .. note ::
          Path separation is handled client side so it is possible to copy
          to/from hosts with differing path separators, like from/to Linux
          and Windows.

        :rtype: List(:mod:`gevent.Greenlet`) of greenlets for remote copy \
        commands
        """
        return [self.pool.spawn(self._copy_file, host, local_file, remote_file)
                for host in self.hosts]

    def _copy_file(self, host, local_file, remote_file):
        """Make sftp client, copy file"""
        if not self.host_clients[host]:
            self.host_clients[host] = SSHClient(host, user=self.user,
                                                password=self.password,
                                                port=self.port, pkey=self.pkey,
                                                forward_ssh_agent=self.forward_ssh_agent)
        return self.host_clients[host].copy_file(local_file, remote_file)
