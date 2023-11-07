from mdc.router.cli.rp_base.ng_router import config
from mdc.router.cli.rp_base.ng_router.cli import PROMPT_CONFIG

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

    def __init__(self, session: object, *args, **kwargs):
        super().__init__(session)
        self._args = args
        self._kwargs = kwargs

    def _set_default_prompts(self):
        """
        Set the default prompts for the session.
        """
        self._s.set_default_prompts([PROMPT_CONFIG])

    def _getin(self):
        """
        Get into the interface lan.
        """
        self._s.command_expect('interface lan')

    def getin(self):
        """
        Get into the interface lan and set the default prompts for the session.

            Returns: 
                object: The object instance. 
        """
        self._set_default_prompts()
        self._getin()
        return self

    def name(self, name: str):
        """
        Set a name for an interface or a VLAN group in a switch configuration file. 

            Args: 
                name (str): Name of an interface or a VLAN group to be set in switch configuration file.  

            Returns: 
                object: The object instance with updated parameters/attributes as per given name argument value.  
        """
        self._s.command_expect(f'name {name}')
        return self

    def set_lan_interface(self,
                            name: str = None,
                            ip: str = None,
                            mask: str = None,
                            bind_vlan: str = None,
                            mac_address: str = None):
        """
        Set the LAN interface of the device.

            Args:
                name (str): The name of the interface.
                ip (str): The IP address of the interface.
                mask (str): The subnet mask of the interface.
                bind_vlan (str): The VLAN to bind to the interface.
                mac_address (str): The MAC address of the interface.

            Returns:
                self: The object itself for method chaining. 
        """
        if name:
            self._s.command_expect(f'name {name}')
        if ip and mask:
            self._s.command_expect(f'ip address static {ip} {mask}')
        if bind_vlan:
            self._s.command_expect(f'bind vlan {bind_vlan}')
        if mac_address:
            self._s.command_expect(f'mac-address {mac_address}')
        return self

    def ip_address_static(self, ip: str, mask: str):
        """
        Set a static IP address on the device's LAN interface.

            Args: 
                ip (str): The IP address to set on the LAN interface. 
                mask (str): The subnet mask for the IP address being set on the LAN interface. 

            Returns: 
                self: The object itself for method chaining. 
        """
        self._s.command_expect(f'ip address static {ip} {mask}')
        return self

    def set_ospf(self, area_id: str = None, auth: dict = None):
        if area_id:
            self._s.command_expect(f'ip ospf area {area_id}')
        if auth:
            if auth['type'] == 'simple':
                self._s.command_expect(
                    f'ip ospf auth simple auth-key {auth["key"]}')
            elif auth['type'] == 'md5':
                self._s.command_expect(
                    f'ip ospf auth md5 {auth["key_id"]} auth-key {auth["key"]}'
                )
            else:
                raise ValueError(
                    f'input invalid authentication information: {auth}')
        return self
