from mdc.router.cli.rp_base.lg_router.tn5000 import config
from mdc.router.cli.rp_base.lg_router.tn5000.cli import PROMPT_CONFIG

class ConfigFirewall(config.Config):
    """
    Class for configuring L37 Policy.

        Args:
            session (object): A valid session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Attributes:
            _s (Session): A Session object used to communicate with the device.
            _args (list): A list of arguments passed to the function.
            _kwargs (dict): A dictionary of keyword arguments passed to the function.
    """
    def __init__(self, session, *args, **kwargs):
        super().__init__(session)
        self._args = args
        self._kwargs = kwargs

    def _set_default_prompts(self):
        self._s.set_default_prompts([PROMPT_CONFIG])

    def _getin(self):
        index = self._args[0] if len(self._args) != 0 else None
        if index is None:
            raise Exception(f"Input parameter is empty!")
        self._s.command_expect(f'firewall {index}')

    def getin(self):
        self._set_default_prompts()
        self._getin()
        return self

    def set_firewall_policy(self,
                            action=None,
                            mode=None,
                            protocol=None,
                            itf=None,
                            sip=None,
                            dip=None,
                            sport=None,
                            dport=None,
                            smac=None,
                            enable_log=None,
                            disable_log=None):
        """
        :type itf: dict
        :type enable_log: list
        :type disable_log: list
        """
        if action in ["accept", "drop"]:
            self._s.command_expect(f"action {action}")
        if mode in ["ip", "mac"]:
            self._s.command_expect(f"mode {mode}")
        if protocol:
            self._s.command_expect(f"protocol {protocol}")
        if itf:
            self._s.command_expect(f'interface {itf["in"]} {itf["out"]}')
        if sip:
            self._s.command_expect(f"src-ip single {sip}")
        if dip:
            self._s.command_expect(f"dst-ip single {dip}")
        if sport:
            self._s.command_expect(f"src-port {sport}")
        if dport:
            self._s.command_expect(f"dst-port {dport}")
        if smac:
            self._s.command_expect(f"src-mac {smac}")
        log_item = ["flash", "syslog", "trap"]
        if isinstance(enable_log, list):
            for i in enable_log:
                if i in log_item:
                    self._s.command_expect(f"logging {i}")
                else:
                    raise ValueError(f'input invalid item: {i}')
        if isinstance(disable_log, list):
            for i in disable_log:
                if i in log_item:
                    self._s.command_expect(f"no logging {i}")
                else:
                    raise ValueError(f'input invalid item: {i}')

        self._s.command_expect("exit")
