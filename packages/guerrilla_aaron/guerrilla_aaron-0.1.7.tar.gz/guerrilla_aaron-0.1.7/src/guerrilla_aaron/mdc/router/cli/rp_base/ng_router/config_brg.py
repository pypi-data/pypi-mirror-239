from guerrilla_aaron.mdc.router.cli.rp_base.ng_router import config
from guerrilla_aaron.mdc.router.cli.rp_base.ng_router.cli import PROMPT_CONFIG

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
        Get into the interface lan.
        """
        self._s.command_expect(f'interface bridge')

    def getin(self):
        """
        Set the default prompts and get into the interface wan.

            Returns: 
                self: The instance of the object. 
        """
        self._set_default_prompts()
        self._getin()
        return self

    def set_brg_interface(self, name=None, ip=None, mask=None):
        """
        Set bridge interface parameters.

            Args:
                self (object): Instance of the class.
                name (str): Name of the bridge interface.
                ip (str): IP address of the bridge interface.
                mask (str): Subnet mask of the bridge interface.

            Returns:
                object: Instance of the class. 
        """
        if name:
            self._s.command_expect(f'name {name}')
        if ip and mask:
            self._s.command_expect(f'ip address {ip} {mask}')
        return self

    def disable_brg_interface(self):
        """
        Disable bridge interface.

            Returns: 
                object: Instance of the class. 
        """
        self._s.command_expect(f'shutdown')
        return self
