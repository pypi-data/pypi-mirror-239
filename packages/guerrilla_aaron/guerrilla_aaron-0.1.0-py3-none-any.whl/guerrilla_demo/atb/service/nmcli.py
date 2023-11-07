from session import SshSession
from utils.decorator import root_access_required


class NetworkManagerService:
    """
    A class to manage NetworkManager server.

        Attributes:
            _ssh (SshSession): An instance of SshSession.
            _sudo_pwd (str): Password for sudo user.
    """

    def __init__(self, ssh_session: SshSession, sudo_paswd: str):

        self._ssh = ssh_session
        self._sudo_pwd = sudo_paswd

    def _check_conneted(self):
        """
        Check if SSH session is connected.

        Raises:
            ValueError: If SSH session is not connected.
        """
        if not self._ssh.is_connected():
            raise ValueError('SSH session not connected')

    def check_env(self):
        """
        Check the environment for the current SSH connection.

        Raises:
            ValueError: If the NetworkManage tool is not found.
        """
        self._check_conneted()

        ret = self._ssh.command('nmcli --version', timeout=5)
        assert 'not found' not in ret, \
                f'Command "nmcli" not found'

    @root_access_required
    def intf_setting(self, managed: bool = True):
        """
        Configure interface management status.

            Attributes:
                managed (bool): If managed is set to false, all interfaces listed in /etc/network/interfaces will be ignored.
        """
        self._check_conneted()

        if managed:
            cmd = "sed -i 's/managed=false/managed=true/g' /etc/NetworkManager/NetworkManager.conf"
        else:
            cmd = "sed -i 's/managed=true/managed=false/g' /etc/NetworkManager/NetworkManager.conf"

        self._ssh.command(cmd)

        ## restart
        cmd = 'systemctl restart NetworkManager'
        self._ssh.command(cmd, timeout=5)

    @root_access_required
    def create_connection(self,
                          con_type: str,
                          con_name: str = None,
                          vpn_type: str = None,
                          user: str = None,
                          password: str = None,
                          gateway: str = '192.168.128.254'):
        """
        Activate the network connection. It will take about 5 sec.

            Attributes:
                con_type (str): Connection type.
                                Type could be: ethernet, wifi, vpn, ppp, bridge, vlan, ...
                con_name (str): Connection name. Defaults to None.
                vpn_type (str): The type of VPN connection. Defaults to None.
                user (str): Username of the connection. Defaults to None.
                password (str): Password of the connection. Defaults to None.
                gateway (str): Connection gateway. Default to 192.168.128.254

            Raises: 
                Exception: If connection fails to create.
        """
        self._check_conneted()

        cmd = 'nmcli connection add '
        cmd += f'type {con_type} '
        cmd += f'con-name "{con_name}" '

        if vpn_type:
            cmd += f'vpn-type "{vpn_type}" '

        cmd += f'vpn.data "gateway={gateway}, user={user}" '
        cmd += f'vpn.secrets "password={password}" '

        ret = self._ssh.command(cmd, timeout=10)

        if 'successfully added' not in ret:
            raise ValueError(f'Connection create fail, {ret}')

    @root_access_required
    def activate_connection(self, con_name: str, ifname: str = 'eth1'):
        """
        Activate the network connection.

            Attributes:
                con_name (str): Connection to be Activated.

            Raises: 
                Exception: If connection fails to activate.
        """
        self._check_conneted()

        cmd = f'nmcli connection up {con_name} '
        cmd += f'ifname {ifname}'

        ret = self._ssh.command(cmd, timeout=15)

        if 'successfully activated' not in ret and 'already active' not in ret:
            raise ValueError(f'Connection activate fail, {ret}')

    @root_access_required
    def deactivated_connection(self, con_name: str):
        """
        Deactivate the network connection.

            Attributes:
                con_name (str): Connection to be deactivated.

            Raises: 
                Exception: If connection fails to deactivate.
        """
        self._check_conneted()

        cmd = f'nmcli connection down {con_name}'

        ret = self._ssh.command(cmd, timeout=10)

        if 'successfully deactivated' not in ret:
            raise ValueError(f'Connection deactivate fail, {ret}')

    @root_access_required
    def delete_connection(self, con_name: str):
        """
        Delete the network connection.

            Attributes:
                con_name (str): Connection to be deleted.

            Raises: 
                Exception: If connection fails to delete.
        """
        self._check_conneted()

        cmd = f'nmcli connection delete {con_name}'

        ret = self._ssh.command(cmd, timeout=10)

        if 'successfully deleted' not in ret:
            raise ValueError(f'Connection delete fail, {ret}')

    def show_connection(self):
        """
        Show all the network connection.
        """
        self._check_conneted()

        self._ssh.command('nmcli connection show', timeout=5)
