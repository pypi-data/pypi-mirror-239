import time
import re
from session import SshSession
from utils.decorator import root_access_required

class MailServerService:
    """
    A class for managing a mail server using Docker Compose.

        Attributes:
            _ssh (SshSession): An SSH session object for connecting to the server.
            _dir (str): The directory where the mail server files are stored.
            _sudo_pwd (str): The password for sudo access.
            _hostname (str): The hostname of the mail server.
            _mutt (MuttService): A MuttService object for managing the Mutt email client.
            DMS_GITHUB_URL (str): The URL for the Docker Mail Server GitHub repository.

        Methods:
            __init__(self, ssh_session: SshSession, sudo_paswd: str): Initializes the MailServerService object.
            _check_conneted(self): Checks if the SSH session is connected.
            check_env(self): Checks the environment for the mail server and creates necessary files and directories if they don't exist.
            start(self): Starts the mail server by running docker-compose up command and waits for the mailserver to be up-to-date.
            clean_up(self, service): Cleans up the specified service.
            _make_compose_file(self): Downloads the compose.yaml file from the DMS_GITHUB_URL and extracts the hostname from it.
            _make_env_file(self): Downloads the mailserver.env file from the DMS GitHub URL and saves it to the current directory.
            add_mailserver_account(self, user, paswd): Adds a new email account to the mail server.
            set_mailserver(self): Sets the mail server by removing $myhostname to prevent hostname conflict.
            set_mutt_service(self, ip, user="mutt", paswd="adminmoxa"): Sets up and starts the Mutt email client service.
    """
    def __init__(self, ssh_session: SshSession, sudo_paswd: str):
        self._ssh = ssh_session
        self._dir = "$HOME/mailserver"
        self._sudo_pwd = sudo_paswd
        self._hostname = "mail.example.com"
        self._mutt = MuttService(self._ssh, self._sudo_pwd)
        self.DMS_GITHUB_URL="https://raw.githubusercontent.com/docker-mailserver/docker-mailserver/master"

    def _check_conneted(self):
        """
        Check if the environment is valid.

            Raises:
                ConnectionError: If the SSH session is not connected or if no docker image cincan/tshark is found.
        """
        if not self._ssh.is_connected():
            raise ConnectionError('SSH session not connected')
        
    @root_access_required
    def check_env(self):
        """
        Checks the environment for the mail server and creates necessary files and directories if they don't exist.
        Also installs docker-compose if it's not already installed.
        """
        self._check_conneted()
        self._ssh.command(f'cd $HOME')
        output = self._ssh.command('ls')
        if "mailserver" not in output:
            self._ssh.command(f'mkdir {self._dir}')
        self._ssh.command(f'cd {self._dir}')
        output = self._ssh.command('ls')
        if "compose.yaml" not in output:
            self._make_compose_file()
        if "mailserver.env" not in output:
            self._make_env_file()
        output = self._ssh.command(f'command -v docker-compose')
        if "/docker-compose" not in output:
            self._ssh.command("N")
            self._ssh.command('curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose',
                                exact_prompts=['100'],
                                timeout=300)
            self._ssh.command('chmod +x /usr/local/bin/docker-compose')

    @root_access_required
    def start(self):
        """
        Starts the mail server by running docker-compose up command and waits for the mailserver to be up-to-date.
        """
        self._ssh.command(f'cd {self._dir}')
        self._ssh.command(f'docker-compose up -d', 
                            exact_prompts=['done', 'mailserver is up-to-date'], 
                            timeout=300)
        time.sleep(5)

    @root_access_required
    def clean_up(self, service):
        """
        Cleans up the specified service.

            Args:
                service (str): The name of the service to clean up. Can be "mail_server" or "mutt".

            Raises:
                ValueError: If the specified service is not "mail_server" or "mutt".
        """
        if service == "mail_server":
            self._ssh.command(f'cd {self._dir}')
            self._ssh.command(f'docker-compose down', 
                            exact_prompts=['Removing network mailserver_default'], 
                            timeout=300)
            self._ssh.command(f'rm -r {self._dir}')
        elif service == "mutt":
            self._mutt.clean_up()
        else:
            raise ValueError(f"Unknown service: {service}")
        
    def _make_compose_file(self):
        """
        Downloads the compose.yaml file from the DMS_GITHUB_URL and extracts the hostname from it.
        """
        self._ssh.command(f'cd {self._dir}')
        self._ssh.command(f'wget "{self.DMS_GITHUB_URL}/compose.yaml"',
                  exact_prompts=['100%'],
                  timeout=300)
                  
        output = self._ssh.command("cat compose.yaml")
        match = re.search(r"hostname:\s*(\S+)", output)
        self._hostname = match.group(1)

    def _make_env_file(self):
        """
        Downloads the mailserver.env file from the DMS GitHub URL and saves it to the current directory.
        """
        self._ssh.command(f'wget "{self.DMS_GITHUB_URL}/mailserver.env"',
                            exact_prompts=['100%'],
                            timeout=300)
    
    def add_mailserver_account(self, user, paswd):
        """
        Adds a new email account to the mail server.

            Args:
                user (str): The username for the new email account.
                paswd (str): The password for the new email account.
        """
        self._ssh.command(f'''docker exec -it mailserver bash -c "setup email add {user}@{self._hostname} {paswd}"''')
    
    def set_mailserver(self):
        """
        Sets the mail server by removing $myhostname to prevent hostname conflict.
        """
        # remove $myhostname to prevent hostname conflict
        self._ssh.command(f'''docker exec -it mailserver bash -c "postconf -e 'mydestination = localhost.\$mydomain, localhost'"''')

    def set_mutt_service(self, ip, user="mutt", paswd="adminmoxa"):
        """
        Sets up and starts the Mutt email client service.

            Args:
                ip (str): The IP address of the local host.
                user (str): The username for the Mutt email client. Default is "mutt".
                paswd (str): The password for the Mutt email client. Default is "adminmoxa".
        """
        self._mutt.check_env()
        self._mutt.make_muttrc_conf(hostname=self._hostname, user=user, paswd=paswd)
        self._mutt.set_local_hosts(ip=ip, hostname=self._hostname)
        self._mutt.start()
        time.sleep(10)

    @root_access_required
    def set_local_hosts(self, ip):
        """
        Sets the local hosts file on the mail server to include the given IP address and hostname.

            Args:
                ip (str): the IP address to add to the hosts file
        """
        output = self._ssh.command(f"cat /etc/hosts")
        if self._hostname not in output:
            self._ssh.command(f"echo '{ip}  {self._hostname}' >> /etc/hosts")

    @root_access_required
    def get_email(self):
        """
        Retrieves the latest email from the mail server.

            Returns:
                str: The contents of the latest email.
        """
        dir = "/var/mail/mail.example.com/mutt/new"
        output = self._ssh.command(f'docker exec -it mailserver bash -c "ls {dir}"')
        tmp = re.search(r"'(\S+)'", output).group(1)
        output = self._ssh.command(f'docker exec -it mailserver bash -c "cat {dir}/{tmp}"')

        return output
    
class MuttService:
    """
    A class representing a Mutt service.

        Attributes:
            _ssh (SshSession): The SSH session to use for executing commands.
            _sudo_pwd (str): The password for sudo access.

        Methods:
            __init__(self, ssh_session: SshSession, sudo_paswd: str): Initializes a new instance of the MuttService class.
            start(self): Starts the Mutt service.
            check_env(self): Checks if the environment is set up correctly for the Mutt service.
            make_muttrc_conf(self, hostname, user, paswd): Creates a new muttrc configuration file with the specified parameters.
            set_local_hosts(self, ip, hostname): Sets the local hosts file to include the specified IP and hostname.
            clean_up(self): Cleans up the Mutt service.
    """
    def __init__(self, ssh_session: SshSession, sudo_paswd: str):
        self._ssh = ssh_session
        self._sudo_pwd = sudo_paswd

    @root_access_required
    def start(self):
        """
        Starts the Mutt service.
        """
        self._ssh.command('docker exec -dit mutt sh -c "mutt"')

    def check_env(self):
        """
        Checks if the environment is set up correctly for the Mutt service.
        """
        output = self._ssh.command('docker ps -a')
        if "mutt" not in output:
            output = self._ssh.command('docker images | grep alpine')
            if "alpine" not in output:
                self._ssh.command('docker run -dit --name mutt alpine:latest /bin/sh',
                                exact_prompts=['Downloaded'],
                                timeout=120)
            else:
                self._ssh.command('docker run -dit --name mutt alpine:latest /bin/sh')
            time.sleep(3)
            self._ssh.command('docker exec -it mutt apk update',
                            exact_prompts=['OK:'],
                            timeout=120)
            time.sleep(3)
            self._ssh.command('docker exec -it mutt apk add mutt',
                            exact_prompts=['OK:'],
                            timeout=120)
            time.sleep(3)
        else:
             self._ssh.command('docker start mutt',
                            exact_prompts=['\nmutt'],
                            timeout=120)

    def make_muttrc_conf(self, hostname, user, paswd):
        """
        Creates a new muttrc configuration file with the specified parameters.

            Args:
                hostname (str): The hostname of the mail server.
                user (str): The username to use for authentication.
                paswd (str): The password to use for authentication.
        """
        config_content = f"""
set hostname="{hostname}"
set from="{user}@{hostname}"
set realname="{user}"
set imap_user="{user}@{hostname}"
set imap_pass="{paswd}"
set folder="imap://{hostname}:143"
set spoolfile="imap://{hostname}:143/INBOX"
set smtp_url="smtp://{user}@{hostname}@{hostname}:25/"
set smtp_pass="{paswd}"
unset ssl_starttls
unset ssl_force_tls
"""
        escaped_content = config_content.strip().replace("\n", "\\n")
        # 使用printf命令將配置内容寫入~/.muttrc文件
        command = f'''docker exec -it mutt sh -c "printf '{escaped_content}' > ~/.muttrc"'''
        self._ssh.command(command)

    def set_local_hosts(self, ip, hostname):
        """
        Sets the local hosts file to include the specified IP and hostname.

            Args:
                ip (str): The IP address to add to the hosts file.
                hostname (str): The hostname to add to the hosts file.
        """
        output = self._ssh.command(f'''docker exec -it mutt sh -c "cat /etc/hosts"''')
        if hostname not in output:
            self._ssh.command(f'''docker exec -it mutt sh -c "echo '{ip}  {hostname}' >> /etc/hosts"''')
    
    def clean_up(self):
        """
        Cleans up the Mutt service.
        """
        output = self._ssh.command(f'''docker ps | grep mutt''')
        if "mutt" in output:
            self._ssh.command(f'''docker stop mutt && docker rm mutt''', exact_prompts=['\nmutt'], timeout=120)