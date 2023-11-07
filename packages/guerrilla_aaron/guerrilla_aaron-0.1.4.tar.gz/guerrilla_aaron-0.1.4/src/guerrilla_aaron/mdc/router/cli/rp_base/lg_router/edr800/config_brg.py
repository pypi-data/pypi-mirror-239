from mdc.router.cli.rp_base.lg_router.edr800 import config
from mdc.router.cli.rp_base.lg_router.edr800.cli import PROMPT_CONFIG

class ConfigBrg(config.Config):
    """
    Class for configuring Bridge interfaces.

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
        self._s.command_expect(f'interface bridge')

    def getin(self):
        self._set_default_prompts()
        self._getin()
        return self

    def set_brg_interface(self, name=None, ip=None, mask=None):
        if name:
            self._s.command_expect(f'name {name}')
        if ip and mask:
            self._s.command_expect(f'ip address {ip} {mask}')
        return self

    def disable_brg_interface(self):
        self._s.command_expect(f'shutdown')
        return self
