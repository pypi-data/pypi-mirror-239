from mdc.router.cli.rp_base.lg_router.tn5000 import config
from mdc.router.cli.rp_base.lg_router.tn5000.cli import PROMPT_CONFIG

class ConfigIfLan(config.Config):
    """
    Class for configuring LAN interface.

        Args:
            session (Session): Session object to use for communication with the device.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Attributes:
            _s (Session): A Session object used to communicate with the device.
            _args (tuple): Tuple of positional arguments.
            _kwargs (dict): Dictionary of keyword arguments. 
    """

    def __init__(self, session, *args, **kwargs):
        super().__init__(session)
        self._args = args
        self._kwargs = kwargs

    def _set_default_prompts(self):
        self._s.set_default_prompts([PROMPT_CONFIG])

    def _getin(self):
        self._s.command_expect('interface lan')

    def getin(self):
        self._set_default_prompts()
        self._getin()
        return self

    def name(self, name):
        self._s.command_expect(f'name {name}')
        return self

    def set_lan_interface(self,
                            name=None,
                            ip=None,
                            mask=None,
                            bind_vlan=None,
                            mac_address=None):
        if name:
            self._s.command_expect(f'name {name}')
        if ip and mask:
            self._s.command_expect(f'ip address static {ip} {mask}')
        if bind_vlan:
            self._s.command_expect(f'bind vlan {bind_vlan}')
        if mac_address:
            self._s.command_expect(f'mac-address {mac_address}')
        return self

    def ip_address_static(self, ip, mask):
        self._s.command_expect(f'ip address static {ip} {mask}')
        return self
