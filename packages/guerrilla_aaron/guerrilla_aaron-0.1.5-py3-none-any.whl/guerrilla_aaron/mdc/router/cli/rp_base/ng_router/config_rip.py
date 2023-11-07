from mdc.router.cli.rp_base.ng_router import config
from mdc.router.cli.rp_base.ng_router.cli import PROMPT_CONFIG

class ConfigRip(config.Config):
    """
    Class for configuring Rip.

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
        self._s.command_expect(f'router rip')

    def getin(self):
        """
        Set the default prompts and get into the interface wan.

            Returns: 
                self: The instance of the object. 
        """
        self._set_default_prompts()
        self._getin()
        return self

    def set_rip(self, network: list = None, version: str = "2", redistribute: str = None ):
        """
         Set RIP settings for the given network version and redistribute. This is useful for testing purposes and to ensure that you don't accidentally have a race condition in your database that is the user's responsibility.
         
            Args:
                network: The network to set the RIP for.
                version: The RIP version to set. If not specified the default is used.
                redistribute: The redistribute option to set. If not specified the default is used.
            
            Returns: 
                The command self for chaining.
        """
        
        # configure network if network is set
        if network:
            for iface in network:
                self._s.command_expect(f'network {iface}')
        # configure version if configure is set
        if version:
            self._s.command_expect(f'version {version}')
        # configure redistribute if redistribute is set
        if redistribute:
            self._s.command_expect(f'redistribute {redistribute}')
        return self