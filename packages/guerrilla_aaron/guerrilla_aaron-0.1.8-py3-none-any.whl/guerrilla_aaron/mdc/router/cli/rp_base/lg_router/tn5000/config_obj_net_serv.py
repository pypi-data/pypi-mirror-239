from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000 import config
from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000.cli import PROMPT_CONFIG

class ConfigObjectNetServ(config.Config):
    """
    Class for configuring Network Service Object.

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
        Get into the config-obj-net-serv prompt.
        """
        self._s.command_expect(f'object network-service')

    def getin(self):
        """
        Set the default prompts and get into the config-obj-net-serv prompt.

            Returns: 
                self: The instance of the object. 
        """
        self._set_default_prompts()
        self._getin()
        return self

    def create_object(self, name: str = None, service: list = None):
        """
        Create an object with the given name and service(s).

            Args:
                name (str, optional): The name of the object to create.
                service (list, optional): The service(s) of the object to create.
                
            Returns:
                self: The instance of the object. 
        """
        services = [
            "Remote-Access", "Remote-Desktop", "Email", "File-Transfer",
            "Web-Access", "Network-Service", "Authentication",
            "VOIP-and-Streaming", "SQL-Server"
        ]
        if name:
            self._s.command_expect(f'name {name}')
        if service:
            for i in service:
                if i in services:
                    self._s.command_expect(f'select {i}')
                else:
                    raise ValueError(f'input invalid service: {i}')

        # quit to save
        self._s.command_expect(f'exit')
        return self
