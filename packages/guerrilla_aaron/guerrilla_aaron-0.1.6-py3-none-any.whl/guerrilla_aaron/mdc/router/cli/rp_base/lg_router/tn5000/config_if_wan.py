from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000 import config
from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000.cli import PROMPT_CONFIG

class ConfigIfWan(config.Config):
    """
    Class for configuring WAN interface.

        Args:
            session (Session): Session object to communicate with the device.
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
        self._s.command_expect(f'interface wan')

    def getin(self):
        self._set_default_prompts()
        self._getin()
        return self

    def set_wan_interface(self,
                            ip,
                            mask,
                            bind_vlan: str = None,
                            mac_address: str = None,
                            gateway: str = None):
        if gateway:
            self._s.command_expect(
                f'ip address static {ip} {mask} {gateway}')
        else:
            self._s.command_expect(f'ip address static {ip} {mask}')
        if bind_vlan:
            self._s.command_expect(f'bind vlan {bind_vlan}')
        if mac_address:
            self._s.command_expect(f'mac-address {mac_address}')
        return self

    def disable_wan_interface(self):
        self._s.command_expect(f'shutdown')
        return self

    def ip_address_static(self, ip, mask, gateway=''):
        self._s.command_expect(f'ip address static {ip} {mask} {gateway}')
        return self
        
    def ip_address_dhcp(self, bind_vlan):
        """
        Set a WAN interface with dhcp mode.

            Returns: 
                self: The object instance itself.  
        """
        self._s.command_expect(f'bind vlan {bind_vlan}')
        self._s.command_expect(f'ip address dhcp')
        return self
