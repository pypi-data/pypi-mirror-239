from guerrilla_aaron.session import SshSession

class TrexConsoleService:
    """
    Class to control the TRex console.

        Args:
            ssh_session (SshSession): An SSH session object.
            sudo_paswd (str): The sudo password for the remote server.

        Attributes:
            _ssh (SshSession): SSH session object.
            _trex_path (str): Path to TRex directory.
    """

    def __init__(self, ssh_session: SshSession, sudo_paswd: str):
        self._ssh = ssh_session
        self._trex_path = '/home/rmd/trex/v2.99'

    def check_env(self):
        """
        Checks if the TRex server is running and if the TRex path is valid.

            Raises:
                ValueError: If TRex server is not running or TRex path is not valid.
        """
        output = self._ssh.command('ps -aux | grep trex')
        if 'scapy_server' not in output:
            raise ValueError('TRex Server not start')

        output = self._ssh.command(f'ls {self._trex_path}')
        if 'No such file or directory' in output:
            raise ValueError(f'TRex not found at {self._trex_path}')

    def start(self):
        """
        Start trex console.

            Raises:
                ValueError: If trex console fails to start or cannot find prompt.
        """
        self._ssh.command(f'cd {self._trex_path}')
        ret = self._ssh.command('./trex-console',
                                exact_prompts=['trex>'],
                                timeout=60)
        if ret is None:
            raise ValueError('Start trex console fail. Cannot find prompt')
        if ret.count('[SUCCESS]') != 3:
            raise ValueError(f'Start trex console error. Output:\n{ret}')

    def send_packet(self, packet_path: str, rate: int, unit: str, ports: list):
        """
        Send a packet to the specified ports.

            Args:
                packet_path (str): Path of the packet.
                rate (int): Rate of the packet.
                unit (str): Unit of the rate, eg: 'pps'.
                ports (list[int]): List of ports to send the packet. 
                
            Raises: 
                ValueError: If sending start command fails. 
        """
        port = ' '.join([str(p) for p in ports])
        # eg: start -f stl/icmpv6.py -m 10pps --port 0
        cmd = f'start -f {packet_path} -m {rate}{unit} --port {port}'
        ret = self._ssh.command(cmd, exact_prompts=['trex>'])
        if ret.count('[SUCCESS]') != 3:
            raise ValueError(f'Send start command error. Output:\n{ret}')

    def stop(self):
        """
        Stop the TRex traffic generator.
        """
        self._ssh.command('stop', exact_prompts=['trex>'])
        self._ssh.command('clear', exact_prompts=['trex>'])
        self._ssh.command('exit')


class TrexServerService:
    """
    Class for controlling a TRex server over SSH.

        Args:
            ssh_session (SshSession): An SSH session object.
            sudo_paswd (str): The sudo password for the remote server.

        Attributes:
            _ssh (SshSession): An SSH session object.
            _trex_path (str): The path to the TRex installation on the remote server.
            _screen_pid (int, optional): The process ID of the TRex screen session, if one is running. Defaults to None.
            _sudo_pwd (str): The sudo password for the remote server.
    """

    def __init__(self, ssh_session: SshSession, sudo_paswd: str):
        self._ssh = ssh_session
        self._trex_path = '/home/rmd/trex/v2.99'
        self._screen_pid = None
        self._sudo_pwd = sudo_paswd

    def check_env(self):
        """
        Check if TRex is installed in the given path.

            Raises:
                ValueError: If TRex is not found at the given path.
        """
        output = self._ssh.command(f'ls {self._trex_path}')
        if 'No such file or directory' in output:
            raise ValueError(f'TRex not found at {self._trex_path}')

    def start(self):
        """
        Start TRex on the remote server.

            Raises:
                ValueError: If wait server starts timeout.
            Usage:
                1. change dir to trex folder because there are related config files
                2. screen
                3. sudo ./t-rex-64 -i
                4. space
                5. ctrl + A D
        """
        self._ssh.command(f'cd {self._trex_path}')
        # NOTE: how to clean existed screen -> killall screen
        self._ssh.command(
            'screen',
            exact_prompts=['[Press Space for next page; Return to end.'])
        self._ssh.command(' ')

        ret = self._ssh.command(
            f'echo {self._sudo_pwd} | sudo -S ./t-rex-64 -i',
            exact_prompts=['test duration'],
            timeout=60)

        if ret is None:
            raise ValueError('Wait server starts timeout')

        self._ssh.sendcontrol('A')
        self._ssh.sendcontrol('D')

        output = self._ssh.command('')  # expect prompt to get output
        idx = output.find('[detached from ')
        msg = output[idx:]  # eg: should be [detached from 27397.pts-4.trex]
        name = msg.split()[-1]
        self._screen_pid = name.split('.')[0]

    def stop(self):
        """
        Stop the server.

            Usage:
                1. Change to working dir
                2. screen -R 27397
                3. send ctrl + C 
                4. exit.
        """
        self._ssh.command(f'screen -R {self._screen_pid}',
                          exact_prompts=['test duration'])
        # self._ssh.command('', exact_prompts=['test duration'])
        self._ssh.sendcontrol('C')
        self._ssh.command('')  # wait server stopped
        self._ssh.command('exit')  # leave screen


class TrexService:
    """
    Class for controlling TRex server.

        Args:
            ssh_session (SshSession): SSH session object.
            sudo_paswd (str): Password for sudo user.

        Attributes:
            _ssh (SshSession): SSH session object.
            _trex_path (str): Path to TRex server.
            _screen_pid (int): PID of the screen process running TRex server.
            _sudo_pwd (str): Password for sudo user.
    """

    def __init__(self, ssh_session: SshSession, sudo_paswd: str):
        self._ssh = ssh_session
        self._trex_path = '/home/rmd/trex/v2.99'
        self._screen_pid = None
        self._sudo_pwd = sudo_paswd

    def check_env(self):
        """
        Check if TRex is installed in the given path.

            Raises:
                ValueError: If TRex is not found at the given path.
        """
        output = self._ssh.command(f'ls {self._trex_path}')
        if 'No such file or directory' in output:
            raise ValueError(f'TRex not found at {self._trex_path}')

    def _start_server(self):
        """
        Start the TRex server on the remote machine.

            Raises:
                ValueError: If waiting for server start times out or an error occurs while starting the server. 
            
            Usage:
                1. change dir to trex folder because there are related config files
                2. screen
                3. sudo ./t-rex-64 -i
                4. space
                5. ctrl + A D
        """
        self._ssh.command(f'cd {self._trex_path}')
        # NOTE: how to clean existed screen -> killall screen
        self._ssh.command(
            'screen',
            exact_prompts=['[Press Space for next page; Return to end.'])
        self._ssh.command(' ')

        ret = self._ssh.command(
            f'echo {self._sudo_pwd} | sudo -S ./t-rex-64 -i',
            exact_prompts=['test duration'],
            timeout=60)

        if ret is None:
            raise ValueError('Wait server starts timeout')

        self._ssh.sendcontrol('A')
        self._ssh.sendcontrol('D')

        output = self._ssh.command('')  # expect prompt to get output
        idx = output.find('[detached from ')
        msg = output[idx:]  # eg: should be [detached from 27397.pts-4.trex]
        name = msg.split()[-1]
        self._screen_pid = name.split('.')[0]

    def _stop_server(self):
        """
        Stops the TRex server by sending the appropriate commands to the SSH connection.

            Usage:
                1. change to working dir
                2. screen -R 27397
                3. ctrl + C
                4. exit
        """
        self._ssh.command(f'screen -R {self._screen_pid}',
                          exact_prompts=['test duration'])
        # self._ssh.command('', exact_prompts=['test duration'])
        self._ssh.sendcontrol('C')
        self._ssh.command('')  # wait server stopped
        self._ssh.command('exit')  # leave screen

    def _start_console(self):
        """
        Start the TRex console.

            Raises:
                ValueError: If start trex console fail or output is not success.
        """
        self._ssh.command(f'cd {self._trex_path}')
        ret = self._ssh.command('./trex-console',
                                exact_prompts=['trex>'],
                                timeout=60)
        if ret is None:
            raise ValueError('Start trex console fail. Cannot find prompt')
        if ret.count('[SUCCESS]') != 3:
            raise ValueError(f'Start trex console error. Output:\n{ret}')

    def _send_packet(self, packet_path: str, rate: str, unit: str, ports: list):
        """
        Send a packet to the specified ports.

            Args:
                packet_path (str): Path of the packet.
                rate (str): Rate of the packet.
                unit (str): Unit of the rate, such as 'pps'.
                ports (list): List of ports. 

            Raises:
                ValueError: If sending start command fails. 
        """
        port = ' '.join([str(p) for p in ports])
        # eg: start -f stl/icmpv6.py -m 10pps --port 0
        cmd = f'start -f {packet_path} -m {rate}{unit} --port {port}'
        ret = self._ssh.command(cmd, exact_prompts=['trex>'])
        if ret.count('[SUCCESS]') != 3:
            raise ValueError(f'Send start command error. Output:\n{ret}')

    def _stop_console(self):
        """
        Stop the TRex console.
        """
        self._ssh.command('stop', exact_prompts=['trex>'])
        self._ssh.command('exit')

    def send(self, packet_path: str, rate: str, unit: str, port: str):
        """
        Send a packet to the server.

            Args:
                packet_path (str): Path of the packet to send.
                rate (str): Rate of the packet to send.
                unit (str): Unit of rate, e.g., 'bps'.
                port (str): Port number to send the packet.
             
        """
        self._start_server()
        self._start_console()
        self._send_packet(packet_path, rate, unit, port)

    def stop(self):
        """
        Stop the console and server.
        """
        self._stop_console()
        self._stop_server()
