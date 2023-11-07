from mdc.router.cli.rp_base.lg_router.tn5000 import config
from mdc.router.cli.rp_base.lg_router.tn5000.cli import PROMPT_CONFIG

class ConfigOspf(config.Config):
    """
    Class for configuring Ospf.

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
        Get into the router configuration mode.
        """
        # default apply the first element as parameter
        routerId = self._args[0] if len(self._args) != 0 else None
        if routerId is None:
            raise Exception(f"Input parameter is empty!")
        self._s.command_expect(f'router ospf {routerId}')

    def getin(self):
        """
        Set the default prompts and get into the interface wan.

            Returns: 
                self: The instance of the object. 
        """
        self._set_default_prompts()
        self._getin()
        return self

    def set_ospf_area(self, area_id: str):
        self._s.command_expect(f'area {area_id}')
        return self
