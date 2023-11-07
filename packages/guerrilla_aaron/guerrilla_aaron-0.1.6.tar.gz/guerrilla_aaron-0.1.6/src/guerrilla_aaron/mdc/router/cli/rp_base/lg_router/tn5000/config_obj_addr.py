from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000 import config
from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000.cli import PROMPT_CONFIG

class ConfigObjectAddr(config.Config):
    """
    Class for configuring IP Address and Subnet Object.

        Args:
            session (object): The session object.
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
        self._s.command_expect(f'object address')

    def getin(self):
        """
        Set the default prompts and get into the interface wan.

            Returns: 
                self: The instance of the object. 
        """
        self._set_default_prompts()
        self._getin()
        return self

    def create_object(self, name: str = None, ip_addr: str = None):
        """
        Create an object with the given name and IP address.

            Args:
                name (str, optional): The name of the object to create.
                ip_addr (str, optional): The IP address of the object to create.
                
            Returns:
                self: The instance of the object. 
        """
        if name:
            self._s.command_expect(f'name {name}')
        if ip_addr:
            self._s.command_expect(f'ip-addr {ip_addr}')
        return self
