from mdc.router.cli.rp_base.lg_router.tn5000 import config
from mdc.router.cli.rp_base.lg_router.tn5000.cli import PROMPT_CONFIG

class ConfigIfEthernet(config.Config):
    """
    Class for configuring Ethernet interfaces.

        Args:
            session (object): A valid session object.
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.

        Attributes:
            _s (Session): A Session object used to communicate with the device.
            _args (list): A list of arguments passed to the function.
            _kwargs (dict): A dictionary of keyword arguments passed to the function.
    """

    def __init__(self, session, *args, **kwargs):
        super().__init__(session)
        self._args = args
        self._kwargs = kwargs

    def _set_default_prompts(self):
        self._s.set_default_prompts([PROMPT_CONFIG])

    # Reserve flexibility for function override
    def _getin(self):
        # default apply the first element as parameter
        mod_port = self._args[0] if len(self._args) != 0 else None
        if mod_port is None:
            raise Exception(f"Input parameter is empty!")
        self._s.command_expect(f'interface ethernet {mod_port}')

    def getin(self):
        self._set_default_prompts()
        self._getin()
        return self

    def set_switchport(self, vlan_id, mode="access"):
        ret = self._s.command_expect(f'switchport {mode} vlan {vlan_id}')
        return self

    def set_bridge_group(self, group: int = None):
        self._s.command_expect(f'bridge group {group}')
        return self

    def set_port_status(self, flag: str = 'enable'):
        """
        Set the port status.

            Args:
                flag: A parameter to decide port status

            Returns:
                self: The instance of the class.
        """
        if flag == 'enable':
            self._s.command_expect(f'no shutdown')
        elif flag == 'disable':
            self._s.command_expect(f'shutdown')
        else:
            raise ValueError(f'input invalid status: {flag}')
        return self
