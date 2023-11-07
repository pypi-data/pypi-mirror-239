from datetime import datetime
from guerrilla_aaron.session import SshSession
from guerrilla_aaron.utils.decorator import root_access_required

class SyslogService:
    """
    Class for controlling the Syslog Server.

        Args:
            ssh_session (SshSession): SSH session object.
            sudo_paswd (str): Password for sudo command.

        Attributes:
            result_fname (str): File name of the result log file.
            _sudo_pwd (str): Password for sudo command.
            _ssh (SshSession): SSH session object.
    """

    def __init__(self, ssh_session: SshSession, sudo_paswd: str):
        self._ssh = ssh_session
        # TODO: clean log file
        self.result_fname = None
        self._sudo_pwd = sudo_paswd

    def _check_conneted(self):
        """
        Checks if SSH session is connected.

            Raises:
                ValueError: If SSH session is not connected.
        """
        if not self._ssh.is_connected():
            raise ValueError('SSH session not connected')

    def check_env(self):
        """
        Checks if the environment is ready for syslog-ng container to be started.

        Checks if the SSH session is connected and if the docker image balabit/syslog-ng exists in the environment.
            
            Raises:
                ValueError: If SSH session is not connected or docker image balabit/syslog-ng does not exist in the environment. 
        """
        self._check_conneted()
        output = self._ssh.command('docker images')
        if 'balabit/syslog-ng' not in output:
            raise ValueError('No docker image balabit/syslog-ng')

    @root_access_required
    def start(self):
        """
        Starts syslog-ng container on the remote machine.

        Creates a directory and a messages file, logs in as root, and runs a docker command to start the syslog-ng container on the remote machine. 

            Raises: 
                ValueError: If SSH session is not connected. 
        """
        self._check_conneted()
        _now = datetime.now().isoformat()
        self._container_name = 'syslog'
        self.dir_name = 'syslog'
        self._ssh.command(f'mkdir //{self.dir_name}')
        self._ssh.command(f'echo "" > //{self.dir_name}/messages')
        cmd = f'docker run -it --rm -d --name={self._container_name}'\
            f' -p 514:514/udp -v //{self.dir_name}:/var/log/'\
            ' -p 601:601 balabit/syslog-ng:latest'

        self._ssh.command(cmd)

    def stop(self):
        """
        Stop the container.
        """
        self._check_conneted()

        cmd = f'docker stop {self._container_name}'
        self._ssh.command(cmd)
        self._ssh.command('')  # wait prompt

    def read_message(self):
        """
        Reads the messages from the container.

            Returns: 
                str: The messages from the container.
        """
        self._check_conneted()
        cmd = f'docker exec -it {self._container_name} bash -c ' \
            '"cat /var/log/messages"'
        return self._ssh.command(cmd)

