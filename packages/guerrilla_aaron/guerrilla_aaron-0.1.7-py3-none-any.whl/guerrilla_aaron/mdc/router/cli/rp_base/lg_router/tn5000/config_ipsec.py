from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000 import config, config_ipsec_phase1, config_ipsec_phase2
from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000.cli import PROMPT_CONFIG

class ConfigIpsec(config.Config):
    """
    Class for configuring IPSec.

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

    # Reserve flexibility for function override
    def _getin(self):
        # default apply the first element as parameter
        vpn_connection_name = self._args[0] if len(
            self._args) != 0 else None
        if vpn_connection_name is None:
            raise Exception(f"Input parameter is empty!")
        self._s.command_expect(f'ipsec {vpn_connection_name}')

    def getin(self):
        self._set_default_prompts()
        self._getin()
        return self

    def go_phase1(self, *args, **kwargs):
        return config_ipsec_phase1.ConfigIpsecPhase1(
            self._s, *args, **kwargs).getin()

    def go_phase2(self, *args, **kwargs):
        return config_ipsec_phase2.ConfigIpsecPhase2(
            self._s, *args, **kwargs).getin()
