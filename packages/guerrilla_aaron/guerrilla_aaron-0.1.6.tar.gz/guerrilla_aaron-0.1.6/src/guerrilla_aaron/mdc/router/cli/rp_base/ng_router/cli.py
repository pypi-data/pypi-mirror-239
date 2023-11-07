from session import PROMPTS
PROMPT_MAIN = PROMPTS["NRP"]["MAIN"]
PROMPT_CONFIG = PROMPTS["NRP"]["CONFIG"]
PROMPT_LOGIN = PROMPTS["NRP"]["LOGIN"]
ALL_PROMPTS = PROMPTS["ALL"]["ALL"]
ALL_PROMPTS_MAIN = PROMPTS["ALL"]["MAIN"]
ALL_PROMPTS_CONFIG = PROMPTS["ALL"]["CONFIG"]

class Cli:
    """
    Class for CLI operations.
        
        Args:
            session (obj): Session object.

        Attributes:
            _s (session): An instance of the Session class.
    """

    def __init__(self, session: object):
        self._s = session

    def __chk_prompt(self, match_prompt: str):
        """
        Check if the current prompt is the same as match_prompt.

            Args:
                match_prompt (str): The prompt to be matched.

            Returns:
                bool: True if the current prompt is matched with match_prompt, False otherwise.
        """
        try_prompt = 2
        matched_prompt = 0
        for _ in range(try_prompt):
            ret = self._s.command_expect('', prompts=ALL_PROMPTS, timeout=2)
            print(ret)
            #check DUT is not in a logged out state
            if PROMPT_LOGIN in ret['data']:
                self._s.close()
                raise Exception(f"DUT logout!! Fail to back to main.\nret: {ret}")
            # print('ret["pattern"]: ', ret['pattern'])
            # print('type of ret["pattern"]: ', type(ret['pattern']))
            # print(isinstance(ret['pattern'], type))
            if ret['pattern'] == match_prompt or isinstance(
                    ret['pattern'], type):
                matched_prompt += 1
        return True if (matched_prompt > 0) else False

    def _back_to_main(self):
        """
        Exit until we get back to main prompt.

            Raises: 
                Exception: If exit too much.
        """
        self._s.clear_buffer()
        #try to get prompt        
        #check if already at main prompt
        rt = self.__chk_prompt(PROMPT_MAIN)
        if rt is True:
            return
        # exit until we get back to main prompt
        retry = 0
        retry_limit = 10
        while (rt is False) and (retry < retry_limit):
            rt = self._s.command_expect('exit',
                                        prompts=ALL_PROMPTS,
                                        timeout=2)
            if rt['pattern'] == PROMPT_MAIN:
                return
            rt = self.__chk_prompt(PROMPT_MAIN)
            if rt is False:
                retry += 1
        if (retry == retry_limit):
            raise Exception("exit too much.")

    def command(self, cmd: str, timeout: int = None):
        """
        Execute a command and return back to main prompt. 

            Args: 
                cmd (str): The command to be executed. 
                timeout (int, optional): Timeout for executing command in seconds. Defaults to None. 

            Raises: 
                ValueError: If cannot get next prompt in time when do command.  
        """
        ret = self._s.command_expect(cmd, timeout=timeout)
        if not ret['matched']:
            raise ValueError(
                f'cannot get next prompt in time when do command: {cmd}')
        return self

    def command_read(self,
                        cmd: str,
                        timeout: int = None,
                        parser: str = None):
        """
        Execute a command and read the output until the next prompt is matched.

            Args:
                cmd (str): The command to execute.
                timeout (int, optional): The maximum time in seconds to wait for the next prompt. Defaults to None.
                parser (str, optional): The parser to use when matching the next prompt. Defaults to None.
                
            Raises:
                ValueError: If the next prompt cannot be matched in time when executing the command. 
                
            Returns: 
                str: The output of the command execution.
        """
        ret = self._s.command_expect(cmd, parser=parser, timeout=timeout)
        if not ret['matched']:
            raise ValueError(
                f'cannot get next prompt in time when do command_read: {cmd}'
            )
        return ret['data']
