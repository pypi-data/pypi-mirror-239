import re
import os
import yaml
import time
import serial
import logging
import pexpect

from mdc import *
from pexpect import pxssh, TIMEOUT, EOF
from utils.debug_output import create_debug_output
from mdc.router.cli.common_func import telnet_login

lib_path = os.path.abspath(os.environ['PYTHONPATH'])
with open(f'{lib_path}/prompt.yaml') as f:
    PROMPTS = yaml.load(f, Loader=yaml.FullLoader)

class SshSession:
    """
    Class for managing SSH sessions.

        Args:
            host (str): Hostname of the server.
            port (int, optional): Port of the server. Defaults to 22.
            timeout (int, optional): Timeout for prompt waiting. Defaults to 2.

        Attributes:
            _ssh (pxssh): pxssh object for managing the session.
            _host (str): Hostname of the server.
            _port (int): Port of the server.
            _timeout (int): Timeout for prompt waiting.
    """

    def __init__(self, conf: dict, error_detector = None, auto_prompt_reset: bool = False):
        self._ssh = pxssh.pxssh(options={'StrictHostKeyChecking': 'no'})
        import sys
        self._ssh.logfile = sys.stdout.buffer  # debug
        self.conf = conf
        self._port = self.conf['port']
        self._host = self.conf['host']
        self._error_detector = error_detector
        self.auto_prompt_reset = auto_prompt_reset
        self._timeout = self.conf['timeout']
        self.reset_default_prompts()

    def is_connected(self):
        """
        Check if session is connected.
        """
        return self._ssh.isalive()

    def login(self, username: str, password: str):
        """
        Login to the server with given credentials.
        """
        try:
            self._ssh.login(self._host,
                            username,
                            password,
                            port=self._port,
                            login_timeout=120,
                            sync_original_prompt=False,
                            original_prompt=r"[#$>>]",
                            auto_prompt_reset=self.auto_prompt_reset)
        except pxssh.ExceptionPxssh as e:
            raise RuntimeError("can not login with SSH") from e

    def logout(self):
        """
        Logout from the server.
        """
        self._ssh.logout()

    def login_as_root(self):
            """
            Log in as root using the given session and sudo password.

                Args:
                    session (object): The session object to use for logging in.
                    sudo_paswd (str): The sudo password to use for logging in.
            """
            print('login_as_root')  # debug
            self._ssh.sendline('su')
            self._ssh.expect('Password')
            self._ssh.sendline(self.conf['credential']['password'])

    def logout_from_root(self):
        """
        Log out from root using the given session.

            Args: 
                session (object): The session object to use for logging out.
        """
        print('logout_from_root')  # debug
        self._ssh.sendline('exit')
        self._ssh.expect_exact('$')

    def sendcontrol(self, char: str):
        """
        Send control character to the server.
        """
        self._ssh.sendcontrol(char)

    def clear_buffer(self):
        """
        Clear buffer of the session. 
        """
        # ref https://github.com/pexpect/pexpect/issues/227
        self._ssh.expect_exact(self._ssh.buffer)

    def set_default_prompts(self, prompts: list):
        """
        Set the default prompts for the application.
        """
        self._prompts = prompts
    
    def reset_default_prompts(self):
        """
        Reset the default prompts for the application to all available prompts.
        """
        self._prompts = PROMPTS["ALL"]["MAIN"]

    def _check_session(self):
        """
        Check if session is opened. If not, raise ValueError.
        """
        if self._ssh is None:
            raise ValueError('session not opened')
        
    def close(self):
        """
        Close the connection
        """
        self._check_session()
        self._ssh.close()

    def command(self,
                cmd: str,
                parser=None,
                exact_prompts: list = None,
                timeout: int = None):
        """
        Send a command to the remote host and return the output.

            Args:
                cmd (str): The command to be executed.
                parser (function, optional): A function to parse the output of the command. Defaults to None. 
                exact_prompts (list, optional): List of expected prompts from the remote host after sending the command. Defaults to None. 
                timeout (int, optional): Timeout for waiting for a prompt from the remote host after sending the command. Defaults to None and uses self._timeout instead. 
                
            Returns: 
                str or function: Output of the command or result of parser if specified. Returns None if no prompt is matched within timeout period.
        """
        self.clear_buffer()
        to = timeout or self._timeout
        self._ssh.sendline(cmd)
        if exact_prompts is None:
            matched = self._ssh.prompt(timeout=to)
        else:
            try:
                self._ssh.expect_exact(exact_prompts, timeout=to)
                # self._ssh.expect_exact(exact_prompts, timeout=to)
            except (TIMEOUT, EOF):
                matched = False
            else:
                matched = True

        if not matched:
            print('can not match any prompt')
            # return None

        output = self._ssh.before.decode('utf-8')
        if parser is None:
            return output
        return parser(output)

    def command_expect(self,
                       command: str = None,
                       parser=None,
                       prompts: list = None,
                       timeout=None,
                       exact_str: bool = False):
        """
        Send a command to the session and expect a prompt. 
            Args: 
                command (str): The command to be sent to the session. 
                parser (function): A function to parse the output of the command. 
                prompts (list): A list of possible prompts that will be expected from the session. 
                timeout (int): Timeout for waiting for a prompt from the session. 
                exact_str (bool): Whether to expect an exact string or not. 

            Returns: 
                dict: A dictionary containing whether a prompt was matched, which pattern was matched and parsed data from output of command if parser is provided.
        """
        self.clear_buffer()
        if command is not None:
            _cmd = command + self.conf['terminator']
            self._ssh.send(_cmd)

        _prompts = prompts or self._prompts
        _prompts = [pexpect.EOF, pexpect.TIMEOUT] + _prompts

        _timeout = timeout or self.conf['timeout']

        if exact_str:
            idx = self._ssh.expect_exact(_prompts, timeout=_timeout)
        else:
            idx = self._ssh.expect(_prompts, timeout=_timeout)

        # strip first line because it is user-entered command
        # outputs[0] will be user-entered command
        # outputs[1] will be the return value of user-entered command
        outputs = self._ssh.before.decode('utf-8')
        outputs = outputs.split('\n', 1)
        # # debug section

        # print('\n-----------session.before-----------', f'cmd: "{command}"')
        # print(self._ssh.before)
        # print('\n------------------------------------')

        # # sometimes it won't return the correct data because the data has been split to session.after
        # # so maybe check what is in self._ssh.after

        # print('\n-----------session.after-----------', f'cmd: "{command}"')
        # print(self._ssh.after)
        # print('\n------------------------------------')
        output = ''
        if len(outputs) == 2:
            output = outputs[1]
        if self._error_detector is not None:
            self._error_detector(output)
            if isinstance(self._ssh.after,str):
                self._error_detector(self._ssh.after)

        return {
            'matched': idx > 1,
            'pattern': _prompts[idx],
            'data': output if parser is None else parser(output)
        }

class TelnetSession:
    """
    Constructs a CLI session object.

    Args:
        args (dict): Dictionary containing the following fields: 
        con_type (str): Connect type.
        host (str): Host's ip or domain name.
        port (str): Host's telnet port.
        prompts (list of strs): Prompts for check if connects.
        encode (str): Encode method.
        terminator (str): Line terminator.
        timout (int): Timeout for session. 

        error_detector (function, optional): Error detector function to be used in the session, defaults to None. 
        logfile (file, optional): Log file to be used in the session, defaults to None. 
    """

    def __init__(self, args: dict, error_detector=None, debug_output: bool = False):
        logging.info(f'args: {args}')
        if not set(args.keys()) >= {
                'con_type', 'host', 'port', 'prompts', 'encode', 'terminator',
                'timeout'
        }:
            raise ValueError('missing argument fields')
        self._args = args
        self._prompts = None
        self._session = None
        self._debug_output = debug_output
        self._error_detector = error_detector
        self._con_type = self._args["con_type"]
        if self._con_type not in ('ssh', 'telnet'):
            raise ValueError('bad con_type')
        self.reset_default_prompts()

    def set_default_prompts(self, prompts: list):
        """
        Set the default prompts for the application.
        """
        self._prompts = prompts

    def get_default_prompts(self):
        """
        Get the default prompts for the application.
        """
        return self._prompts

    def reset_default_prompts(self):
        """
        Reset the default prompts for the application to all available prompts.
        """
        self._prompts = PROMPTS["ALL"]["MAIN"]
        # self._prompts = self._args['prompts']

    def open(self) -> bool:
        """
        Open a connection to a remote host.

            Args:
                username (str): The username to use for authentication.
                password (str): The password to use for authentication.
                
            Returns: 
                bool: True if the connection was successful, False otherwise. 
        """
        self._session = pexpect.spawn(
            f'{self._args["con_type"]} \
            {self._args["host"]} {self._args["port"]}',
            timeout=self._args["timeout"],
            encoding=self._args["encode"],
        )

        self.reset_default_prompts()
        if self._debug_output:
            logfile = create_debug_output(self._debug_output, 'cli_session_edrg9010',
                                                self._con_type, self._args["host"], 
                                                self._args["port"])
            self._session.logfile = logfile

    def _router_telnet_login(self, username: str, password: str,
                             login_prompt: str):
        """
        Log into the router via telnet.

        Args:
            username (str): The username of the router.
            password (str): The password of the router.
            login_prompt (str, optional): The login prompt of the router. If not specified, all prompts will be used. 
        """
        # disable error detector tmeporarily because login would have ^]
        func_hold = self._error_detector
        self._error_detector = None
        if login_prompt is None:
            telnet_login(self, username, password, PROMPTS["ALL"]["MAIN"], PROMPTS["ALL"]["CONFIG"])
        else:
            telnet_login(self, username, password, PROMPTS["ALL"]["MAIN"], PROMPTS["ALL"]["CONFIG"], login_prompt)
        self._error_detector = func_hold

    # FIXME: arg "telnet_login_prompt" is a debt of fix TAS-25/27
    def login(self, credential: dict, telnet_login_prompt: str = None):
        """
        Log in to the router using the provided credentials.

        Args:
            credential (dict): Dictionary containing username and password.
            telnet_login_prompt (str, optional): Prompt used for telnet login. Defaults to None.
        """
        self._check_session()

        try:
            username = credential['username']
            password = credential['password']
        except KeyError as e:
            raise ValueError('Bad credential format') from e

        self._router_telnet_login(username, password, telnet_login_prompt)

    def logout(self):
        """
        Log out of the current session. 
        If the connection type is SSH, log out using the SSH session. 
        Otherwise, send an 'exit' command to the remote host. 

        """
        if self._con_type == 'ssh':
            self._session.close()
        else:
            self.command_expect('exit')

    def _check_session(self):
        """
        Check if session is opened. If not, raise ValueError.
        """
        if self._session is None:
            raise ValueError('session not opened')

    def clear_buffer(self):
        """
        Clear buffer of the session. 
        """
        # ref https://github.com/pexpect/pexpect/issues/227
        s = self._session
        s.expect_exact(s.buffer)

    def command_expect(self,
                       command: str = None,
                       parser=None,
                       prompts: list = None,
                       timeout=None,
                       exact_str: bool = False):
        """
        Send a command to the session and expect a prompt. 
            Args: 
                command (str): The command to be sent to the session. 
                parser (function): A function to parse the output of the command. 
                prompts (list): A list of possible prompts that will be expected from the session. 
                timeout (int): Timeout for waiting for a prompt from the session. 
                exact_str (bool): Whether to expect an exact string or not. 

            Returns: 
                dict: A dictionary containing whether a prompt was matched, which pattern was matched and parsed data from output of command if parser is provided.
        """
        self._check_session()

        if command is not None:
            _cmd = command + self._args['terminator']
            self._session.send(_cmd)

        _prompts = prompts or self._prompts
        _prompts = [pexpect.EOF, pexpect.TIMEOUT] + _prompts

        _timeout = timeout or self._args['timeout']

        if exact_str:
            idx = self._session.expect_exact(_prompts, timeout=_timeout)
        else:
            idx = self._session.expect(_prompts, timeout=_timeout)

        # strip first line because it is user-entered command
        # outputs[0] will be user-entered command
        # outputs[1] will be the return value of user-entered command
        outputs = self._session.before.split('\n', 1)

        # # debug section

        # print('\n-----------session.before-----------', f'cmd: "{command}"')
        # print(self._session.before)
        # print('\n------------------------------------')

        # # sometimes it won't return the correct data because the data has been split to session.after
        # # so maybe check what is in self._session.after

        # print('\n-----------session.after-----------', f'cmd: "{command}"')
        # print(self._session.after)
        # print('\n------------------------------------')
        output = ''
        if len(outputs) == 2:
            output = outputs[1]

        if self._error_detector is not None:
            self._error_detector(output)
            if isinstance(self._session.after,str):
                self._error_detector(self._session.after)

        return {
            'matched': idx > 1,
            'pattern': _prompts[idx],
            'data': output if parser is None else parser(output)
        }

    def command(self, command: str):
        """
        Commands to the host.

            Args:
                command: str, the text to command
        """
        self._check_session()

        self._session.send(command + self._args["terminator"])
        logging.info(command)

    def expect(self, prompts: list) -> dict:
        """
        Expect the specific response. The first two match are EOF & timeout.
        Return a dict collects the raw context and the matched prompt.

            Args:
                prompts: list of string,  the list for expect string.

            Returns:
                dict, format as
                {
                    "context": the raw response text from device,
                    "match_prompt": the prompt matched in the response context,
                    it could be EOF or TIMEOUT
                }
        """
        self._check_session()

        _prompts = [pexpect.EOF, pexpect.TIMEOUT] + prompts
        index = self._session.expect(_prompts)
        logging.debug(self._session.before)

        return {
            "context": self._session.before,
            "match_prompt": _prompts[index]
        }

    def close(self):
        """
        Close the connection
        """
        self._check_session()

        self._session.close()

    def sendcontrol(self, char: str):
        """
        Send control character to the remote host.

            Args: 
                char (str): The control character to send.
        """
        self._session.sendcontrol(char)

class SerialSession:
    """
    Constructs a CLI session object.

    Args:
        args (dict): Dictionary containing the following fields: 
        con_type (str): Connect type.
        host (str): Host's ip or domain name.
        port (str): Host's telnet port.
        prompts (list of strs): Prompts for check if connects.
        encode (str): Encode method.
        terminator (str): Line terminator.
        timout (int): Timeout for session.
        serial_port (str): Port number.
        baudrate (int): Serial port speed.

        error_detector (function, optional): Error detector function to be used in the session, defaults to None. 
        logfile (file, optional): Log file to be used in the session, defaults to None. 
    """

    def __init__(self, args: dict, error_detector=None, debug_output: bool = False):
        logging.info(f'args: {args}')
        if set(args.keys()) != {
                'con_type', 'host', 'port', 'prompts', 'encode', 'terminator',
                'timeout', 'serial_port', 'baudrate'
        }:
            raise ValueError('missing argument fields')
        if args["serial_port"] == None:
            raise ValueError('missing serial_port value')
        self._args = args
        self._prompts = None
        self._session = None
        self._debug_output = debug_output
        self._error_detector = error_detector
        self._con_type = self._args["con_type"]
        self.serial_port = self._args["serial_port"]
        self.baudrate = self._args["baudrate"]
        self.reset_default_prompts()

    def set_default_prompts(self, prompts: list):
        """
        Set the default prompts for the application.
        """
        self._prompts = prompts

    def get_default_prompts(self):
        """
        Get the default prompts for the application.
        """
        return self._prompts

    def reset_default_prompts(self):
        """
        Reset the default prompts for the application to all available prompts.
        """
        self._prompts = PROMPTS["ALL"]["MAIN"]
        # self._prompts = self._args['prompts']

    def open(self) -> bool:
        """
        Open a connection to a remote host.

            Returns: 
                bool: True if the connection was successful, False otherwise. 
        """
        self._session = serial.Serial(self.serial_port, baudrate=self.baudrate, timeout=1)

        self.reset_default_prompts()
        # if self._debug_output:
        #     logfile = create_debug_output(self._debug_output, 'cli_session_edrg9010',
        #                                         self._con_type, self._args["host"], 
        #                                         self._args["port"])
        #     self._session.logfile = logfile

    def login(self, credential: dict, telnet_login_prompt: str = None):
        """
        Log in to the router using the provided credentials.

        Args:
            credential (dict): Dictionary containing username and password.
            telnet_login_prompt (str, optional): Prompt used for telnet login. Defaults to None.
        """
        self._check_session()

        try:
            username = credential['username']
            password = credential['password']
        except KeyError as e:
            raise ValueError('Bad credential format') from e

        assert self._session.isOpen()
        self._session.reset_input_buffer()

        quick_timeout = 2

        # if login session existed, send enter to let prompt appear
        # print('try to get main prompt') #debug
        ret = self.command_expect('', prompts=PROMPTS["ALL"]["MAIN"], timeout=quick_timeout)
        # consume prompts to make buffer clean
        # ret = session.command_expect(None, prompts=promtps, timeout=quick_timeout)
        if ret['matched']:
            return

        # print('try to get config prompt') #debug
        # if login session is config prompt, try to back to main prompt
        ret = self.command_expect('', prompts=PROMPTS["ALL"]["CONFIG"], timeout=quick_timeout)
        if ret['matched']:
            # print('config mode') #debug
            is_main_prompt = False
            for i in range(120):
                # print('try to login') #debug
                time.sleep(1)
                is_main_prompt = self.command_expect('exit', prompts=PROMPTS["ALL"]["MAIN"], timeout=quick_timeout)['matched']
                if is_main_prompt:
                    break
                # print('exit to main prompt') #debug
            return

        self.command_expect('', prompts=["login: "])
        self.command_expect(username, prompts=["Password: "])
        ret = self.command_expect(password)
        if not ret['matched']:
            raise ValueError(f'cannot find prompt after password: {ret}')


    def logout(self):
        """
        Log out of the current session. 
        If the connection type is SSH, log out using the SSH session. 
        Otherwise, send an 'exit' command to the remote host. 

        """
        if self._con_type == 'ssh':
            self._session.logout()
        else:
            self.command_expect('exit')

    def _check_session(self):
        """
        Check if session is opened. If not, raise ValueError.
        """
        if self._session is None:
            raise ValueError('session not opened')

    def clear_buffer(self):
        """
        Clear buffer of the session.
        Clear both the input and output buffers of a serial port. 
        It discards any received but unread data from the input buffer and any unsent data from the output buffer. 
        Calling flush() ensures that all pending data is cleared before proceeding. 
        """
        s = self._session
        s.flush()

    def command_expect(self,
                       command: str = None,
                       parser=None,
                       prompts: list = None,
                       timeout=5,
                       exact_str: bool = False):
        """
        Send a command to the session and expect a prompt. 
            Args: 
                command (str): The command to be sent to the session. 
                parser (function): A function to parse the output of the command. 
                prompts (list): A list of possible prompts that will be expected from the session. 
                timeout (int): Timeout for waiting for a prompt from the session. 
                exact_str (bool): Whether to expect an exact string or not. 

            Returns: 
                dict: A dictionary containing whether a prompt was matched, which pattern was matched and parsed data from output of command if parser is provided.
        """
        prompts = prompts or self._prompts
        # print("command: ", command, prompts)
        print("command: ", command)
        if not isinstance(timeout, int):
            timeout = 5

        self._check_session()
        # print(f"*write: {command}")
        self._session.reset_input_buffer()
        self._session.write(f"{command}\n".encode())
        response = ""
        start_time = time.time()
        idx = -1

        while True:
            response += self._session.read(self._session.in_waiting or 1).decode()
            if exact_str:
                idx = next((i for i, prompt in enumerate(prompts) if response.endswith(prompt)), -1)
            else:
                idx = next((i for i, prompt in enumerate(prompts) if re.search(prompt, response)), -1)

            if idx >= 0:
                break

            if time.time() - start_time > timeout:
                break

        if f'{command}\r' == response.split('\n',1)[0]:
            output = response.split('\n',1)[1]
        else:
            output = response

        # print("*response: ",response,"end*")

        if self._error_detector is not None:
            self._error_detector(output)

        ret= {
            'matched': idx >= 0,
            'pattern': prompts[idx] if idx >= 0 else None,
            'data': output if parser is None else parser(output)
        }
        print(ret)
        return ret

    def command(self, command: str):
        self.command_expect(command)
    #     """
    #     Commands to the host.

    #         Args:
    #             command: str, the text to command
    #     """
    #     self._check_session()

    #     self._session.send(command + self._args["terminator"])
    #     logging.info(command)


    def close(self):
        """
        Close the connection
        """
        self._check_session()
        self._session.close()

    def sendcontrol(self, letter: str):
        """
        Send control character to the remote host.

            Args: 
                char (str): The control character to send.
        """
        ascii_value = ord(letter.upper())
        ctrl_ascii_value = ascii_value & 0b00011111
        ctrl_char = bytes([ctrl_ascii_value])
        self._session.write(ctrl_char)