import re
import json
import time

from datetime import datetime
from session import SshSession

class UICtrlService:
    """
    This class provides methods to control the DUT UI service on a remote device through SSH connection.

        Args:
            ssh_session (SshSession): An active SSH session to the remote host.
            sudo_paswd (str): The sudo password for the remote host.
        
        Attributes:
            _ssh (SshSession): An instance of SshSession class to establish SSH connection with the remote device.
            image_name (str): The name of the image used for running the DUT UI service.
            image_tag (str): The tag of the image used for running the DUT UI service.
            container_name (str): The name of the container running the DUT UI service. 
            command_curl (str): The command used to run curl in a docker container. 
            command_dut_ui (str): The command used to run dut-ui in a docker container. 
            sudo_password (str): The password used for sudo authentication when running commands in a docker container.
    """

    def __init__(self, ssh_session: SshSession, sudo_paswd: str):
        self._ssh = ssh_session
        self.image_name = "nbg-jenkins.moxa.com:5000/sqa/auto-test-atb-dut-service"
        self.image_tag = "v1.0.0"
        self.container_name = ""

        self.command_curl = f"docker run -it --rm {self.image_name}:{self.image_tag} curl "

    def _check_conneted(self):
        """
        Check if the SSH session is connected.

            Raises:
                ValueError: If the SSH session is not connected.
        """
        if not self._ssh.is_connected():
            raise ValueError('SSH session not connected')

    def check_env(self):
        """
        Check the environment for the given image name.

            Raises:
                ValueError: If no docker image with the given name is found. 
        """
        self._check_conneted()
        output = self._ssh.command('docker images')
        if self.image_name not in output:
            raise ValueError(f'No docker image {self.image_name}')

    def cli_init(self):
        """
        Run a docker container with the given image name and tag. 
        The container name is generated using the current datetime in ISO format.  
        """
        self.container_name = "dut_ui_"
        self.container_name += datetime.now().isoformat().replace(":", "_")[:19]
        ret = self._ssh.command(
            f"docker run -dit --name {self.container_name} {self.image_name}:{self.image_tag} /bin/bash"
        )
        print(ret)

    def cli_destroy(self):
        """
        Removes the container created for the testcase, once the testcase is finished.
        """
        self._ssh.command(f"docker rm -f {self.container_name}")
        self.container_name = ""
        time.sleep(3)

    def cli_cmd(self,
                cmd,
                detach: bool = False,
                destroy_after_cmd: bool = False):
        """
        Run a command in the CLI container.

            Args:
                cmd (str): The command to be run in the CLI container.
                detach (bool, optional): If True, run the command in detached mode. Defaults to False.
                destroy_after_cmd (bool, optional): If True, destroy the CLI container after running the command. Defaults to False.
                
            Returns:
                str: The output of the command run in the CLI container.
        """
        if self.container_name == "":
            self.cli_init()
        if detach:
            ret = self._ssh.command(
                f"docker exec -dit {self.container_name} {cmd}")
        else:
            ret = self._ssh.command(
                f"docker exec -it {self.container_name} {cmd}")

        if destroy_after_cmd:
            self.cli_destroy()

        return ret

    def web_get(self,
                uri: str = None,
                jwt: str = None,
                ip: str = "192.168.127.254",
                web_https: bool = True,
                filename: str = None):
        """
        Executes a command to get data from a web server.

            Args:
                uri (str): The URI of the web server. Required parameter.
                jwt (str): The JWT token used for authentication. Required parameter. 
                ip (str): The IP address of the web server. Defaults to "192.168.127.254". 
                web_https (bool): Flag indicating if HTTPS should be used for communication with the web server or not. Defaults to True (HTTPS).

            Returns:
                str: The response from the web server in JSON format or None if an error occurs during execution of the command. 
        """
        if uri is None:
            raise ValueError(f'uri is required.')

        if jwt is None:
            raise ValueError(f'jwt is required.')

        web_command = self.command_curl
        web_command += "-s -k -w \"\\n\" "
        web_command += f"-H \"Authorization: {jwt}\" "
        if web_https:
            web_command += f"https://{ip}/{uri} "
        else:
            web_command += f"http://{ip}/{uri} "
        web_command += '' if filename is None else f'> {filename}'
            
        ret_raw = self._ssh.command(web_command, timeout=5)

        matches = re.findall(r'{.*}', ret_raw)
        if matches:
            return re.findall(r'{.*}', ret_raw)
        else:
            return ret_raw


    def web_post(self,
                 uri: str = None,
                 data_dict: dict = None,
                 jwt: str = None,
                 ip: str = "192.168.127.254",
                 web_https: bool = True):
        """
        Send a web POST request to the given URI.

            Args:
                uri (str): The URI to send the request to. Required.
                data_dict (dict): A dictionary of data to be sent in the body of the request. Optional.
                jwt (str): The JWT token used for authentication. Required.
                ip (str): The IP address of the server to send the request to. Defaults to "192.168.127.254". Optional. 
                web_https (bool): Whether or not to use HTTPS for the request, defaults to True. Optional. 
                
            Returns: 
                str: The response from the server, or None if an error occurred during sending the request. 
        """
        if uri is None:
            raise ValueError(f'uri is required.')

        if jwt is None:
            raise ValueError(f'jwt is required.')

        web_command = self.command_curl
        web_command += "-s -k -w \"\\n\" -H \"Content-Type: application/json\" -X POST "
        web_command += f"-H \"Authorization: {jwt}\" "
        if web_https:
            web_command += f"https://{ip}/{uri} "
        else:
            web_command += f"http://{ip}/{uri} "
        if data_dict is not None:
            web_command += f"-d '{json.dumps(data_dict)}' "

        # print('web_post_command: ', web_command)
        ret_raw = self._ssh.command(web_command, timeout=5)
        # print('web_post_ret_raw: ', ret_raw)

        return re.findall(r'{.*}', ret_raw)


    def web_get_jwt(self,
                    username: str = "",
                    password: str = "",
                    ip: str = "192.168.127.254",
                    web_https: bool = True):
        """
        Retrieve JWT from web API using curl command.

            Args:
                username (str): Username for authentication. Default is an empty string.
                password (str): Password for authentication. Default is an empty string.
                ip (str): IP address of the server. Default is "192.168.127.254".
                web_https (bool): Whether to use https or not when connecting to the server. Default is True. 
                
            Returns:
                str: JWT token if successful, None otherwise. 
        """
        web_command = self.command_curl
        web_command += "-s -k -w \"\\n\" -H \"Content-Type: application/json\" -X POST "
        if web_https:
            web_command += f"https://{ip}/api/v1/auth/login "
        else:
            web_command += f"http://{ip}/api/v1/auth/login "
        web_command += f"-d '{{\"username\": \"{username}\", \"password\": \"{password}\"}}' "

        # print('web_jwt_command: ', web_command)
        ret_raw = self._ssh.command(web_command, timeout=5)
        # print('web_get_jwt_ret_raw: ', ret_raw)

        res_text = re.findall(r'{.*}', ret_raw)
        # # print('web_get_jwt_res_text: ', res_text)
        # print('res_text: ', res_text)
        res_json = json.loads(res_text[1])
        # # print('web_get_jwt_res_json: ', res_json)
        if "access_token" not in res_json:
            print("API response:", ret_raw)
            print(f'Fail to retrieve JWT from API response')
            return None

        jwt = res_json["access_token"]
        # print('jwt: ', jwt)
        return jwt


    def web_post_multipart(self,
                 uri: str = None,
                 form_name: str = None,
                 form_filename: str = None,
                 jwt: str = None,
                 ip: str = "192.168.127.254"):
        """
        Send a multipart POST request to post a file along with some parameters.

            Args:
                uri (str): The URI to send the request to. Required.
                form_name: The type of the upload file. Required
                form_filename: The name of the upload file. Required
                jwt (str): The JWT token used for authentication. Required.
                ip (str): The IP address of the server to send the request to. Defaults to "192.168.127.254". Optional. 
                
            Returns: 
                str: The response from the server, or None if an error occurred during sending the request. 
        """
        web_command = "curl -s -k -w \"\\n\" -X POST "
        web_command += f"--location 'https://{ip}/{uri}' "
        web_command += f"-H \"Authorization: {jwt}\" -H \"content-type: multipart/form-data\" "
        web_command += f"--form 'name=\"{form_name}\"' "
        web_command += f"--form 'filename=@\"{form_filename}\"'"

        print(f'=======web = {web_command}')
        ret_raw = self._ssh.command(web_command, timeout=5)
        print(f'=======ret = {ret_raw}')

        return re.findall(r'{.*}', ret_raw)
