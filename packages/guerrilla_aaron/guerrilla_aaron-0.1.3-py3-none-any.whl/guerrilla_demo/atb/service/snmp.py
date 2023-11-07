from utils.decorator import root_access_required
from session import SshSession
import time


class SnmpService:
    """
    A class to manage tftp server.

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
            ValueError: If SSH session is  not connected.
        """
        if not self._ssh.is_connected():
            raise ValueError('SSH session not connected')

    @root_access_required
    def check_env(self):
        """
        Check the environment for the current SSH connection.

        Raises:
            ValueError: If the SNMP tool is not found.
        """
        self._check_conneted()

        ret = self._ssh.command('snmpwalk --version', timeout=5)
        if 'not found' in ret:
            ret = self._ssh.command('apt install -y snmp', timeout=120)
            assert 'fail' not in ret.lower(), f'snmp install failed.'

        ret = self._ssh.command('snmpget --version', timeout=5)
        if 'not found' in ret:
            self._ssh.command('apt install -y snmp', timeout=120)
            assert 'fail' not in ret.lower(), f'snmp install failed.'

    def get_snmp(self,
                 oid: str,
                 version: str,
                 username: str = 'admin',
                 priv_method: str = None,
                 community: str = 'public',
                 security: str = 'authPriv',
                 auth_key: str = 'auth_key',
                 priv_key: str = 'priv_key',
                 auth_type: str = 'no-auth',
                 agent_id: str = '192.168.127.254'):
        """
        Send SNMP get request to the specific SNMP agent.

            Attributes:
                oid (str): The Object Identifier (OID) to retrieve.
                version (str): SNMP version to use. Options: '1', '2c', '3'.
                username (str): SNMP username. Default is 'admin'.
                priv_method (str): SNMPv3 privacy protocol. Options: 'des', 'aes'. Default is None.
                community (str): SNMP community string. Options: 'public', 'private'. Default is 'public'.
                security (str): SNMPv3 security level. Options: 'authPriv', 'authNoPriv', 'NoAuthNoPriv'. Default is 'authPriv'.
                auth_key (str): SNMPv3 authentication key.  Default is 'auth_key'.
                priv_key (str): SNMPv3 privacy key. Default is 'priv_key'.
                auth_type (str): SNMPv3 authentication type. Options: 'md5', 'sha'. Default is 'no-auth'.
                agent_id (str): IP address of the SNMP agent. Default is '192.168.127.254'.
        
            Example:
                v1, v2c cmd: snmpwalk -v 1 -c public 192.168.127.254 1.3.6.1.2.1.1.5.0
                v3 cmd: snmpwalk -v 3 -l authPriv -u admin -a MD5 -A auth_key -x DES -X priv_key 192.168.127.254 1.3.6.1.2.1.1.5.0
        """
        cmd = 'snmpwalk '

        ## for SNMPv1, SNMPv2c
        if version == '1' or version == '2c':
            print(f'SNMP version {version}')
            cmd += f'-v {version} '
            cmd += f'-c {community} '

        ## for SNMPv3
        if version == '3':
            print('SNMP version 3')
            cmd += f'-v 3 '
            cmd += f'-l {security} '
            cmd += f'-u {username} '
            if auth_type != 'no-auth':
                cmd += f'-a {auth_type.upper()} -A {auth_key} '
                if priv_method:
                    cmd += f'-x {priv_method.upper()} -X {priv_key} '

        cmd += f'{agent_id} {oid}'
        time.sleep(5)

        ret = self._ssh.command(cmd)

        return ret

    def set_snmp(self,
                 oid: str,
                 version: str,
                 new_info: str,
                 username: str = 'admin',
                 priv_method: str = None,
                 community: str = 'public',
                 security: str = 'authPriv',
                 auth_key: str = 'auth_key',
                 priv_key: str = 'priv_key',
                 auth_type: str = 'no-auth',
                 agent_id: str = '192.168.127.254'):
        """
        Send SNMP set request to the specific SNMP agent.

            Attributes:
                oid (str): The Object Identifier (OID) to retrieve.
                version (str): SNMP version to use. Options: '1', '2c', '3'.
                new_info (str): New information related to changes in the OID.
                username (str): SNMP username. Default is 'admin'.
                priv_method (str): SNMPv3 privacy protocol. Options: 'des', 'aes'. Default is None.
                community (str): SNMP community string. Options: 'public', 'private'. Default is 'public'.
                security (str): SNMPv3 security level. Options: 'authPriv', 'authNoPriv', 'NoAuthNoPriv'. Default is 'authPriv'.
                auth_key (str): SNMPv3 authentication key.  Default is 'auth_key'.
                priv_key (str): SNMPv3 privacy key. Default is 'priv_key'.
                auth_type (str): SNMPv3 authentication type. Options: 'md5', 'sha'. Default is 'no-auth'.
                agent_id (str): IP address of the SNMP agent. Default is '192.168.127.254'.
                
            Example:
                v1, v2c cmd: snmpset -v 1 -c private 192.168.127.254 1.3.6.1.2.1.1.5.0 s "snmp_check"
                v3 cmd: snmpset -v 3 -l authPriv -u admin -a MD5 -A auth_key -x DES -X priv_key 192.168.127.254 1.3.6.1.2.1.1.5.0 s "snmp_check"
        """
        cmd = 'snmpset '

        ## for SNMPv1, SNMPv2c
        if version == '1' or version == '2c':
            print(f'SNMP version {version}')
            cmd += f'-v {version} '
            cmd += f'-c {community} '

        ## for SNMPv3
        if version == '3':
            print('SNMP version 3')
            cmd += f'-v 3 '
            cmd += f'-l {security} '
            cmd += f'-u {username} '
            if auth_type != 'no-auth':
                cmd += f'-a {auth_type.upper()} -A {auth_key} '
                if priv_method:
                    cmd += f'-x {priv_method.upper()} -X {priv_key} '

        cmd += f'{agent_id} {oid} s "{new_info}"'

        ret = self._ssh.command(cmd)

        time.sleep(10)

        return ret

    @root_access_required
    def start_snmptrapd(self):
        ret = self._ssh.command('dpkg -l | grep snmptrapd', timeout=5)

        if 'Net-SNMP notification receiver' not in ret.strip(''):
            ret = self._ssh.command('apt install -y snmptrapd', timeout=120)
            assert 'fail' not in ret.lower(), f'snmptrapd install failed.'

        ret = self._ssh.command('systemctl start snmptrapd', timeout=5)

        if 'Failed to start' in ret:
            raise ValueError(ret)
