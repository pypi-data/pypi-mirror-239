import os
import re
import json

from datetime import datetime
from guerrilla_aaron.session import SshSession


class CaService:
    """
    Class for handling certificate authority related operations.

        Args:
            ssh_session (SshSession): SSH session object.
            sudo_paswd (str): sudo password.
        
         Attributes:
            _ssh (SshSession): An SSH session object.

        Tip:
            1. Create CA certificate
            2. Create Server certificate signing request (CSR)
            3. Sign the Server Request using CA certificate
    """
    def __init__(self, ssh_session: SshSession, sudo_paswd: str):
        self._ssh = ssh_session
        self._sudo_pwd = sudo_paswd

    def check_env(self):
        if not self._ssh.is_connected():
            raise ValueError('SSH session not connected')

        ret = self._ssh.command('openssl version', timeout=5)
        assert 'not found' not in ret, \
                f'Command "openssl" not found'


    def prepare_env(self):
        self._ssh.command('mkdir cert', timeout=5)
    

    def generate_root_ca(self, 
                         rsa: str = "4096"):
        """
        Generate a self-signed X.509 certificate (also known as a self-signed certificate).

            Tip:
                openssl req: Certificate requests and related operations.
                -x509: Specifies that a self-signed certificate will be created instead of a certificate signing request (CSR).
                -newkey rsa:4096: Generates a new RSA private key with a key size of 4096 bits.
                -keyout root/root.pem: Output file where the private key will be stored.
                -out root/root.crt: Specifies the output file where the self-signed certificate will be stored.
                -days 3650: Setup the validity period of the certificate to 3650 days.
                -nodes: Specifies that the private key should not be encrypted with a passphrase. 
                        (It allows for automated processes since no password will be required when using the key.)
                -subj: Setup the subject (or distinguished name) of the certificate. 
                        C=Country code; ST=State or province name; L=Locality or city name; 
                        O=Organization name; OU=Organizational unit name; CN=Common Name
        """ 
        cmd = 'openssl req -x509 '
        cmd += f'-newkey rsa:{rsa} '
        cmd += '-keyout cert/root.pem -out cert/root.crt '
        cmd += '-days 3650 '
        cmd += '-nodes '
        cmd += '-subj "/C=TW/ST=Taipei/L=Taipei/O=Dp3/OU=Sec5/CN=Dp3_Sec5_localhost"'
        
        self._ssh.command(cmd, timeout=5)

    
    def generate_server_csr(self, 
                            rsa: str = "2048",
                            cn: str = "192.168.127.254"):
        """
        Generate a certificate signing request (CSR) for a server.

            Args:
                rsa (str): key size
                cn (str): Common Name (should be host name)
        """
        file_name = f'server_{datetime.now().isoformat().replace(":", "_")[:19]}'
        
        cmd = 'openssl req '
        cmd += f'-newkey rsa:{rsa} '
        cmd += f'-keyout cert/{file_name}.pem -out cert/{file_name}.csr '
        cmd += '-days 3650 '
        cmd += '-nodes '
        cmd += f'-subj "/CN={cn}"'

        self._ssh.command(cmd, timeout=5)

    
    def sign_cert(self, 
                 server_csr: str = "192.168.127.254.csr",
                 root_cert: str = "root.crt",
                 root_penkey: str = "root.pem",
                 server_cert: str = "test.crt"):
        """
        Generating a signed certificate (server_cert.crt),
            using the private key of the root certificate (CA) to sign the certificate request (CSR), 

            Args:
                server_csr (str): The input file for credential requests.
                root_cert (str): The root certificate (CA) file.
                root_penkey (str): The private key file of the root certificate (CA).
                server_cert (str): The output file for signed certificates.
        """
        cmd = 'openssl x509 -req '
        cmd += f'-in {server_csr} -CA cert/{root_cert} -CAkey cert/{root_penkey} -CAcreateserial '
        cmd += f'-out cert/{server_cert} '
        cmd += '-days 3650'

        ret = self._ssh.command(cmd, timeout=5)

    
    def check_secure_connection(self, 
                                cert: str = "cert/root.crt",
                                pem_key: str = "cert/root.pem",
                                ip: str = "192.168.127.254"):
        """
        Check if a secure connection can be established using the generated certificate.

            Args:
                cert (str): Specifies the path to a CA certificate used to verify certificates presented by the server.
                pem_key (str): Specifies the path to the client's private key file.
                ip (str): Target ip. Defaults to "192.168.127.254".
        """
        cmd = f'curl -vvI --cacert {cert} --key {pem_key} https://{ip}'
        ret = self._ssh.command(cmd, timeout=5)

        if 'SSL certificate verify ok.' not in ret:
            return False

        return True


    def clean_up(self, 
                 username: str = 'autotwo'):
        """
        Clean up the environment.
        """
        self._ssh.command(f'ssh-keygen -f "/home/{username}/.ssh/known_hosts" -R "192.168.127.254"', timeout=2)
        self._ssh.command('ssh admin@192.168.127.254')
        self._ssh.sendcontrol('C')

    
    def rm_file(self):
        """
        Remove generated files.
        """
        self._ssh.command("rm -r cert *.csr", timeout=5)