import os
import re
import json
import time

from datetime import datetime
from guerrilla_aaron.session import SshSession

client_config_file = '~/raddb/clients.conf'
users_config_file = '~/raddb/mods-config/files/authorize'

class RadiusService:
    """
    Class for autheticate via RADIUS server.

        Args:
            ssh_session (SshSession): SSH session object.
            sudo_paswd (str): Password for sudo command.
        
         Attributes:
            _ssh (SshSession): An SSH session object.
    """

    def __init__(self, ssh_session: SshSession, sudo_paswd: str):
        self._ssh = ssh_session
        self._sudo_pwd = sudo_paswd
        self._base_image = 'freeradius/freeradius-server'
        self._container_name = 'radius-server'


    def _check_conneted(self):
        if not self._ssh.is_connected():
            raise ValueError('SSH session not connected')


    def check_env(self):
        """
        Checks if the SSH session is connected and if the docker image exists.
            (Docker images version fix in v3.2)
            
        """
        self._check_conneted()
        check_images = f'docker images | grep {self._base_image} > check_images.log'
        self._ssh.command(check_images)
        output = self._ssh.command('cat check_images.log')
        if 'freeradius/freeradius-server' not in output:
            print(f'Ready to download image: {self._base_image}')
            self._ssh.command('docker pull freeradius/freeradius-server:latest-3.2', 
                              exact_prompts=['Downloaded newer image for freeradius/freeradius-server:latest-3.2'], 
                              timeout=120)


    def add_client(self,
                    client_name: str = None,
                    ipaddr: str = '192.168.127.0',
                    netmask: str = '24', 
                    secret: str = 'testing123', 
                    msg: str = 'no', 
                    nastype: str = 'other'):
        if client_name is None:
            raise ValueError(f'client_name is required.')
        
        client_config = f'client {client_name} {{\\n'
        client_config += f'\\tipaddr = {ipaddr}/{netmask}\\n'
        client_config += f'\\tproto = *\\n'
        client_config += f'\\tsecret = {secret}\n'
        client_config += f'\\trequire_message_authenticator = {msg}\\n'
        client_config += f'\\tnastype = {nastype}\\n}}'

        self._ssh.command(f'mkdir -p ~/raddb/mods-config/files')
        self._ssh.command(f'echo -e "{client_config}" >> {client_config_file}')

    
    def add_users(self,
                   username: str = None,
                   password: str = None,
                   service_type: str = 'Shell-User'):   # Shell-User = Admin; Login = User
        user_config = f'{username}\\tCleartext-Password := "{password}"\n'
        user_config += f'\\tService-Type = {service_type}\n'
        
        self._ssh.command(f'mkdir -p ~/raddb/mods-config/files')        
        self._ssh.command(f'echo -e \'{user_config}\' >> {users_config_file}')
        
        
    def build_local_image(self):
        dockerfile_config = f'FROM freeradius/freeradius-server:latest\\nCOPY raddb/ /etc/raddb/'
        self._ssh.command(f'echo -e "{dockerfile_config}" > ~/Dockerfile')
        
        # build image with custom config
        self._ssh.command(f'docker build -t {self._container_name}-image -f Dockerfile .')


    def start(self):
        """
        Starts custom freeradius container on the remote machine.

            Raises: 
                ValueError: If SSH session is not connected. 
        """
        self._check_conneted()
        cmd = f'docker run --rm -d --name {self._container_name} \
                -p 1812-1813:1812-1813/udp {self._container_name}-image'
        
        self._ssh.command(cmd)
        time.sleep(5)
        self._ssh.command('')  # wait prompt
    

    def stop(self):
        """
        Stop the container and clean up the environment.
             - stop container
             - remove custom freeradius image
             - remove radius local config file   
        """
        self._check_conneted()

        stop_cmd = f'docker stop {self._container_name}'
        self._ssh.command(stop_cmd)
        self._ssh.command('')  # wait prompt

        rmi_cmd = f'docker rmi {self._container_name}-image'
        self._ssh.command(rmi_cmd)

        rm_cmd = f'rm -r Dockerfile raddb'
        self._ssh.command(rm_cmd)
