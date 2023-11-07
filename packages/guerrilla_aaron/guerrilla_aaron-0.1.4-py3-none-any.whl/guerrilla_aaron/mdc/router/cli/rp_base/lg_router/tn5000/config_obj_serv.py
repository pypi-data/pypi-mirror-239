from mdc.router.cli.rp_base.lg_router.tn5000 import config
from mdc.router.cli.rp_base.lg_router.tn5000.cli import PROMPT_CONFIG

class ConfigObjectServ(config.Config):
    """
    Class for configuring User-defined Service Object.

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

    # Reserve flexibility for function override
    def _getin(self):
        """
        Get into the config-obj-serv prompt.
        """
        # default apply the first element as parameter
        service = self._args[0] if len(self._args) != 0 else None
        if service is None:
            raise Exception(f"Input parameter is empty!")
        self._s.command_expect(f'object service {service}')

    def getin(self):
        """
        Set the default prompts and get into the config-obj-serv prompt.

            Returns: 
                self: The instance of the object. 
        """
        self._set_default_prompts()
        self._getin()
        return self

    def set_object_serv(self,
                        name: str,
                        port: str = None,
                        icmp_type: str = None,
                        icmp_code: str = None,
                        ipproto: str = None):
        """
        Create an object with the given name and IP address.

            Args:
                name (str, optional): The name of the object to create.
                port (str, optional): The port of the object to create.
                
            Returns:
                self: The instance of the object. 
        """
        if name:
            self._s.command_expect(f'name {name}')
        if port:
            self._s.command_expect(f'port {port}')
        if icmp_type:
            self._s.command_expect(f'icmp-type {icmp_type}')
        if icmp_code:
            self._s.command_expect(f'icmp-code {icmp_code}')
        if ipproto:
            self._s.command_expect(f'ipproto {ipproto}')

        # quit to save
        self._s.command_expect(f'exit')
        return self
