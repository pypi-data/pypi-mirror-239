from guerrilla_aaron.mdc.router.cli.rp_base.ng_router import config, config_if_wan, config_if_lan
from guerrilla_aaron.mdc.router.cli.rp_base.ng_router.cli import PROMPT_CONFIG

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
        self._session = session
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
        if area_id:
            self._s.command_expect(f'area {area_id}')
        return self
    
    def set_ospf_redistribute(self, redistribute: str = None):
        if redistribute:
            self._s.command_expect(f'redistribute {redistribute}')
        return self

    def set_ospf_intf(self, 
                      intf: str, 
                      area_id: str, 
                      priority: int = 1,
                      hello_interval: int = 10, 
                      dead_interval: int = 40):
        if intf.lower() == "wan":
            config_wan = config_if_wan.ConfigIfWan(self._session)
            config_wan.getin()
        elif intf.lower() == "lan":
            config_lan = config_if_lan.ConfigIfLan(self._session)
            config_lan.getin()
        else:
            raise ValueError(f"input invalid {intf}")
        
        if area_id:
            self._s.command_expect(f'ip ospf area {area_id}')
        if priority:
            self._s.command_expect(f'ip ospf priority {priority}')
        if hello_interval:
            self._s.command_expect(f'ip ospf hello-interval {hello_interval}')
        if dead_interval:
            self._s.command_expect(f'ip ospf dead-interval {dead_interval}')