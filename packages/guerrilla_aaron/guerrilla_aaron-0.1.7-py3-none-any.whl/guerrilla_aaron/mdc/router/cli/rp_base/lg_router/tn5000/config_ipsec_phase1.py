from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000 import config
from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000.cli import PROMPT_CONFIG

class ConfigIpsecPhase1(config.Config):
    """
    Class for configuring IPSecPhase1.

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
        # Auxiliary method under ConfigIPSec so super init is not required
        self._s = session
        self._args = args
        self._kwargs = kwargs

    def _set_default_prompts(self):
        self._s.set_default_prompts([PROMPT_CONFIG])

    def _getin(self):
        self._s.command_expect(f'phase1')

    def getin(self):
        self._set_default_prompts()
        self._getin()
        return self

