from session import SshSession
from utils.decorator import root_access_required

class TftpService:
    """
    A class to manage tftp server.

        Attributes:
            _ssh (SshSession): An instance of SshSession.
            _sudo_pwd (str): Password for sudo user.
    """

    def __init__(self, ssh_session: SshSession, sudo_paswd: str):
        self._ssh = ssh_session
        self._sudo_pwd = sudo_paswd

    @root_access_required
    def check_env(self):
        """
        Check the environment of tftp server.
        Prints 'TftpServer: check_env' and logs in as root with given password to show status of tftpd-hpa service and log out from root afterwards. Asserts that the service is active. 
        """
        if not self._ssh.is_connected():
            raise ValueError('SSH session not connected')
        ret = self._ssh.command(
            'systemctl status tftpd-hpa.service | grep Active', timeout=5)
        # print(f'ret: {ret}')  # debug
        assert 'active' in ret, f'tftp server is not actived: {ret}'

