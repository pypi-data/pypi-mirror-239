from session import SshSession

class Hping3Service:
    """
    Class for controlling hping3 docker image over SSH session.

        Args:
            ssh_session (SshSession): SSH session object.
            sudo_paswd (str): sudo password.
        
         Attributes:
            _ssh (SshSession): An SSH session object.
    """

    def __init__(self, ssh_session: SshSession, sudo_paswd: str):
        self._ssh = ssh_session

    def _check_conneted(self):
        """
        Check if the environment is ready for running the tests.

        Raises:
            ValueError: If SSH session is not connected or docker image "sflow/hping3" is not found.
        """
        if not self._ssh.is_connected():
            raise ValueError('SSH session not connected')

    def check_env(self):
        """
        Check the environment for the current SSH connection.

        Raises:
            ValueError: If the docker image "sflow/hping3" is not found.
        """
        self._check_conneted()
        output = self._ssh.command('docker images')
        if 'sflow/hping3' not in output:
            raise ValueError('docker image "sflow/hping3" not found')

    # pylint: disable=too-many-arguments
    def send(self,
             host: str,
             tcpudp_flags: list,
             count: int,
             interval: str = 'faster',
             port: int = None):
        """ 
        Send attcks hping as attack
            Args:
                host (str): destination host address

                port (int): destination host's port

                interval (str): it can be fast, faster, flood or uX for X microseconds

                tcpudp_flag (list): it can be fin, syn, rst, push, ack or urg

                package_count (int): packet count
            
            Raises 
                ValueError: If it cannot make command from tcp/udp flag
        """
        self._check_conneted()

        flag_cmd_map = {
            'null': '',
            'fin': '-F',
            'syn': '-S',
            'rst': '-R',
            'push': '-P',
            'ack': '-A',
            'urg': '-U',
            'tcp': '-S',
            'udp': '-2',
            'icmp': '-1',
        }
        try:
            _flags = ' '.join([flag_cmd_map[f] for f in tcpudp_flags])
        except KeyError as e:
            raise ValueError('cannot make command from tcp/udp flag') from e

        _interval = {
            'fast': '--fast',
            'faster': '--faster',
            'flood': '--flood',
        }.get(interval, f'-i u{interval}')

        # example: docker run --rm --net=host sflow/hping3 192.168.127.31
        #           -R -S -i u10000 -p 80 -c 200
        # cmd = f'docker run --rm --net=host sflow/hping3 {host} -p {port} ' \
        #       f'{_flags} {_interval} -c {count}'
        cmd = f'docker run --rm --net=host sflow/hping3 {host} '
        cmd += '' if port is None else f'-p {port} '
        cmd += f'{_flags} '
        cmd += f'-c {count} '
        cmd += f'{_interval} '

        print(cmd)
        self._ssh.command(cmd)
