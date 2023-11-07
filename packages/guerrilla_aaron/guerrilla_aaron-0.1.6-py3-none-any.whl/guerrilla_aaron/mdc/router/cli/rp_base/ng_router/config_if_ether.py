from guerrilla_aaron.mdc.router.cli.rp_base.ng_router import config
from guerrilla_aaron.mdc.router.cli.rp_base.ng_router.cli import PROMPT_CONFIG

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
        Get into the interface lan.
        """
        # default apply the first element as parameter
        mod_port = self._args[0] if len(self._args) != 0 else None
        if mod_port is None:
            raise Exception(f"Input parameter is empty!")
        self._s.command_expect(f'interface ethernet {mod_port}')

    def getin(self):
        """
        Set the default prompts and get into the interface wan.

            Returns: 
                self: The instance of the object. 
        """
        self._set_default_prompts()
        self._getin()
        return self

    def set_switchport(self, vlan_id, mode="access"):
        """
        Set the switchport to a specific VLAN ID and mode.

            Args:
                vlan_id (int): The VLAN ID to set the switchport to.
                mode (str, optional): The mode of the switchport. Defaults to "access".

            Returns:
                self: The instance of the class.
        """
        self._s.command_expect(f'switchport {mode} vlan {vlan_id}')
        return self

    def set_bridge_group(self):
        """
        Set the bridge group for the switchport.

            Returns:
                self: The instance of the class.
        """
        self._s.command_expect(f'bridge group')
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
