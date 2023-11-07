from mdc.router.cli.rp_base.ng_router import config
from mdc.router.cli.rp_base.ng_router.cli import PROMPT_CONFIG

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

    def __init__(self, session: object, *args, **kwargs):
        super().__init__(session)
        self._args = args
        self._kwargs = kwargs

    def _set_default_prompts(self):
        """
        Set the default prompts.
        """
        self._s.set_default_prompts([PROMPT_CONFIG])

    # Reserve flexibility for function override
    def _getin(self):
        """
        Get into the interface wan.
        """
        # default apply the first element as parameter
        vlan_id = self._args[0] if len(self._args) != 0 else None
        if vlan_id is None:
            raise Exception(f"Input parameter is empty!")
        self._s.command_expect(f'interface vlan {vlan_id}')

    def getin(self):
        """
        Set the default prompts and get into the interface wan.

            Returns: 
                self: The instance of the object. 
        """
        self._set_default_prompts()
        self._getin()
        return self

    def set_ip(self, ip: str, mask: str):
        """
        Set the IP address and mask of the device.

            Args:
                ip (str): The IP address to set.
                mask (str): The subnet mask to set.

            Returns:
                self: The same object with the new IP address and mask set.
        """
        self._s.command_expect(f'ip address {ip} {mask}')
        return self

    def set_name(self, name):
        """
        Set the name of the device.

            Args:
                name (str): The name to set for the device.

            Returns: 
                self: The same object with the new name set. 
        """
        self._s.command_expect(f'name {name}')
        return self
