from mdc.router.cli.rp_base.ng_router.base import Base
from mdc.router.cli.rp_base.ng_router.cli import PROMPT_MAIN

class edr8010_v3_0(Base):

    class Main(Base.Main):

        def set_backdoor(self,
                         account='ieisecureedr_moxasupport',
                         password='83dafc480d466ee0'):
            cmd_args = [
                ('moxasupport 1234', [PROMPT_MAIN]),
                ('exit', [r'login']),
                (account, [r'Password']),
                (password, [r'#']),
            ]
            for args in cmd_args:
                r = self._s.command_expect(args[0], prompts=args[1])
                if not r['matched']:
                    print(f"return = {r}, command = {args[0]}")
                    raise Exception("failed to setup backdoor")
            return self

        def clear_ssh_telnet_limit(self):
            '''
            This step may require modification for future usage.
            Due to the DUT's limit on the number of SSH and Telnet sessions, 
            we need to clear the limitation before logging in and out multiple times.
            '''
            self.set_backdoor()
            self._s.command_expect('iptables -F PortScan', prompts=['#'])
            self._s.command_expect('exit', prompts=['login'])
            # disable ctrl-t mode for serial control
            self.login()
