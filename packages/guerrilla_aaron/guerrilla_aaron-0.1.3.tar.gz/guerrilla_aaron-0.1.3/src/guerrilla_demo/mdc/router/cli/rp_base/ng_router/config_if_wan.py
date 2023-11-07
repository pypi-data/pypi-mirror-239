from mdc.router.cli.rp_base.ng_router import config
from mdc.router.cli.rp_base.ng_router.cli import PROMPT_CONFIG

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

    def __init__(self, session: object, *args, **kwargs):
        super().__init__(session)
        self._args = args
        self._kwargs = kwargs

    def _set_default_prompts(self):
        """
        Set the default prompts.
        """
        self._s.set_default_prompts([PROMPT_CONFIG])

    def _getin(self):
        """
        Get into the interface wan.
        """
        self._s.command_expect(f'interface wan')

    def getin(self):
        """
        Set the default prompts and get into the interface wan.

            Returns: 
                self: The instance of the object. 
        """
        self._set_default_prompts()
        self._getin()
        return self

    def set_wan_interface(self,
                            ip: str,
                            mask: str,
                            bind_vlan: str = None,
                            mac_address: str = None,
                            gateway: str = None):
        """
        Set the WAN interface with given IP address and subnet mask.

            Args:
                ip (str): IP address of the WAN interface.
                mask (str): Subnet mask of the WAN interface.
                bind_vlan (str, optional): VLAN to bind to the WAN interface. Defaults to None.
                mac_address (str, optional): MAC address of the WAN interface. Defaults to None.

            Returns:
                self: The object instance itself.
        """
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
        """
        Disable the WAN interface.

            Returns: 
                self: The object instance itself. 
        """
        self._s.command_expect(f'shutdown')
        return self

    def ip_address_static(self, ip: str, mask: str, gateway: str = ''):
        """
        Set a static IP address for the WAN interface with given subnet mask and gateway (optional).

            Args: 
                ip (str): IP address of the WAN interface. 
                mask (str): Subnet mask of the WAN interface. 
                gateway (str, optional): Gateway for the WAN interface. Defaults to ''.

            Returns: 
                self: The object instance itself.  
        """
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

    def set_pptp(self, ip, username, pwd):
        self._s.command_expect(f'ip pptp {ip} {username} {pwd}')
        return self

    def set_dns(self,
                dns_server_1: str = '8.8.8.8',
                dns_server_2: str = '10.123.200.11',
                dns_server_3: str = '10.123.200.12'):

        self._s.command_expect(
            f'ip name-server {dns_server_1} {dns_server_2} {dns_server_3}')
        return self
