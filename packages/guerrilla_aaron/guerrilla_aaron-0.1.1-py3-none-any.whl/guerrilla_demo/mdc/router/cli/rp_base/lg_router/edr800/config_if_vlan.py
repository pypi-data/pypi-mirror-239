from mdc.router.cli.rp_base.lg_router.edr800 import config
from mdc.router.cli.rp_base.lg_router.edr800.cli import PROMPT_CONFIG

class ConfigIfVlan(config.Config):
    """
    Class for configuring a VLAN interface.

        Args:
            session (Session): An instance of a Session object.
            *args (list): A list of arguments to be passed to the function.
            **kwargs (dict): A dictionary of keyword arguments to be passed to the function.

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
        vlan_id = self._args[0] if len(self._args) != 0 else None
        if vlan_id is None:
            raise Exception(f"Input parameter is empty!")
        self._s.command_expect(f'interface vlan {vlan_id}')

    def getin(self):
        self._set_default_prompts()
        self._getin()
        return self

    def set_ip(self, ip, mask):
        self._s.command_expect(f'ip address {ip} {mask}')
        return self

    def set_name(self, name):
        self._s.command_expect(f'name {name}')
        return self
