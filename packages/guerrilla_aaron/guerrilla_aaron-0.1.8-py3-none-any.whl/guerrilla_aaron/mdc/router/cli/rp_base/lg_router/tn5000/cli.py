from guerrilla_aaron.session import PROMPTS
PROMPT_MAIN = PROMPTS["TN5916"]["MAIN"]
PROMPT_CONFIG = PROMPTS["TN5916"]["CONFIG"]
PROMPT_LOGIN = PROMPTS["TN5916"]["LOGIN"]
ALL_PROMPTS = PROMPTS["ALL"]["ALL"]
ALL_PROMPTS_MAIN = PROMPTS["ALL"]["MAIN"]
ALL_PROMPTS_CONFIG = PROMPTS["ALL"]["CONFIG"]

class Cli:


    def __init__(self, session):
        self._s = session

    def __chk_prompt(self, match_prompt):
        try_prompt = 2
        matched_prompt = 0
        for _ in range(try_prompt):
            ret = self._s.command_expect('', prompts=ALL_PROMPTS, timeout=2)
            #check DUT is not in a logged out state
            if PROMPT_LOGIN in ret['data']:
                self._s.close()
                raise Exception(f"DUT logout!! Fail to back to main.\nret: {ret}")
            if ret['pattern'] == match_prompt:
                matched_prompt += 1
        return True if (matched_prompt > 0) else False

    def _back_to_main(self):
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

    def command(self, cmd, timeout=None):
        ret = self._s.command_expect(cmd, timeout=timeout)
        if not ret['matched']:
            raise ValueError(
                f'cannot get next prompt in time when do command: {cmd}')
        return self

    def command_read(self, cmd, timeout=None, parser=None):
            ret = self._s.command_expect(cmd, parser=parser, timeout=timeout)
            if not ret['matched']:
                raise ValueError(
                    f'cannot get next prompt in time when do command_read: {cmd}'
                )
            return ret['data']
