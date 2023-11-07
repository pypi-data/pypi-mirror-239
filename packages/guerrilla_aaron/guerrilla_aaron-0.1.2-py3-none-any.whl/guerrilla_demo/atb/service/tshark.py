from datetime import datetime
from session import SshSession

class TsharkService:
    """
    Class for providing control over tshark using an SSH session.

        Args:
            ssh_session (SshSession): An SSH session object.
            sudo_paswd (str): The sudo password for the SSH session.
        
        Attributes
            _ssh (SshSession): An SSH session object.
            result_fname (str, optional): The name of the result file.  
            _is_capturing (bool):  A boolean indicating whether tshark is currently capturing or not.  
    """

    def __init__(self, ssh_session: SshSession, sudo_paswd: str):
        self._ssh = ssh_session
        # TODO: clean log file
        self.result_fname = None
        self._is_capturing = False

    def _check_conneted(self):
        """
        Check if the environment is valid.

            Raises:
                ValueError: If the SSH session is not connected or if no docker image cincan/tshark is found.
        """
        if not self._ssh.is_connected():
            raise ValueError('SSH session not connected')

    def check_env(self):
        """
        Check if the environment is ready for running TShark.

            Raises:
                ValueError: If no docker image cincan/tshark is present.
        """
        self._check_conneted()
        output = self._ssh.command('docker images')
        if 'cincan/tshark' not in output:
            raise ValueError('No docker image cincan/tshark')

    def _create_command(self,
                        capture_number=None,
                        interface='any',
                        capture_filter=None,
                        display_filter=None,
                        verbose=False,
                        additional_options=None,
                        option=None):
        """
        Create a command for executing tshark in a docker container.

            Args:
                capture_number (int, optional): Number of packets to capture. Defaults to None.
                interface (str, optional): Interface to capture on. Defaults to 'any'.
                capture_filter (str, optional): Capture filter expression. Defaults to None.
                display_filter (str, optional): Display filter expression. Defaults to None. 
                verbose (bool, optional): add output of packet tree (Packet Details). Defaults to False. 
                option (str, optional): Specifying protocol-specific preferences. Defaults to None. 
            Returns: 
                str: Command for executing tshark in a docker container.
        """
        now = datetime.now().isoformat()
        self.result_fname = f'tshark_result_{now}.log'

        cmd = 'docker run -it --rm --cap-add NET_ADMIN --network host ' \
              'cincan/tshark -n '
        cmd += '' if capture_number is None else f'-c {capture_number} '
        cmd += '' if interface is None else f'-i "{interface}" '
        cmd += '' if capture_filter is None else f'-f "{capture_filter}" '
        cmd += '' if display_filter is None else f'-Y "{display_filter}" '
        cmd += '' if verbose is False else '-V '
        cmd += '' if additional_options is None else f'{additional_options} '
        cmd += '' if option is None else f"-o '{option}' "
        cmd += f'> {self.result_fname}'
        return cmd

    def start(self,
              capture_number=None,
              interface: str = 'any',
              capture_filter=None,
              display_filter=None,
              verbose=False,
              additional_options=None,
              option=None):
        """
        Start capturing packets on the remote host.

            Args:
                capture_number (int, optional): Number of packets to capture. Defaults to None.
                interface (str): The network interface to capture packets from. Defaults to 'any'.
                capture_filter (str): A capture filter to apply when capturing packets. Defaults to None. 
                display_filter (str): A display filter to apply when displaying packets. Defaults to None.
                verbose (bool, optional): add output of packet tree (Packet Details). Defaults to False. 
            Returns: 
                bool: True if capturing started successfully, False otherwise. 
        """
        self._check_conneted()
        if self._is_capturing:
            return False
        self._is_capturing = True

        cmd = self._create_command(capture_number=capture_number,
                                   interface=interface,
                                   capture_filter=capture_filter,
                                   display_filter=display_filter,
                                   verbose=verbose,
                                   additional_options=additional_options,
                                   option=option)
        self._ssh.command(cmd)
        return True

    def stop(self):
        """
        Stop the current capture process.

            Returns:
                bool: True if successfully stopped, False otherwise. 
        """
        self._check_conneted()
        if not self._is_capturing:
            return False
        self._ssh.sendcontrol('c')
        self._ssh.command('')  # wait prompt
        self._is_capturing = False
        return True

    def capture_by_number(self,
                          number: str,
                          timeout: str,
                          interface: str = 'any',
                          capture_filter: str = None,
                          display_filter: str = None,
                          additional_options:str = None):
        """
        Start a capture process with given parameters.

            Args: 
                number (str): Number of packets to be captured. 
                timeout (str): Timeout for the capture process in seconds. 
                interface (str): Interface to capture from. Default is 'any'. 
                capture_filter (str): Capture filter string for the capture process. Default is None. 
                display_filter (str): Display filter string for the captured packets. Default is None.  

            Returns: 
                bool: True if successfully started, False otherwise.  
        """
        self._check_conneted()
        if self._is_capturing:
            return False
        self._is_capturing = True

        cmd = self._create_command(capture_number=number,
                                   interface=interface,
                                   capture_filter=capture_filter,
                                   display_filter=display_filter,
                                   additional_options=additional_options)
        r = self._ssh.command(cmd, timeout=timeout)
        
        return True

    def retrieve(self):
        """
        Retrieve the captured packets from remote device as a string.

            Returns: 
                str: Captured packets as a string or None if failed to retrieve them.
        """
        self._check_conneted()
        return self._ssh.command(f'cat {self.result_fname}')
