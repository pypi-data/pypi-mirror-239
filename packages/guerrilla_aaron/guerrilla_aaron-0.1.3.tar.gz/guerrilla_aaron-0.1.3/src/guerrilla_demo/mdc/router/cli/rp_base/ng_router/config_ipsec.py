from mdc.router.cli.rp_base.ng_router import config, config_ipsec_phase1, config_ipsec_phase2
from mdc.router.cli.rp_base.ng_router.cli import PROMPT_CONFIG

class ConfigIpsec(config.Config):
    """
    Class for configuring IPSec.

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
        vpn_connection_name = self._args[0] if len(
            self._args) != 0 else None
        if vpn_connection_name is None:
            raise Exception(f"Input parameter is empty!")
        self._s.command_expect(f'ipsec {vpn_connection_name}')

    def getin(self):
        """
        Set the default prompts and get into the interface wan.

            Returns: 
                self: The instance of the object. 
        """
        self._set_default_prompts()
        self._getin()
        return self

    def set_vpn_connection(self,
                            remote_gateway: str = None,
                            interface: str = None,
                            startup_mode: str = None,
                            local_multi_network: str = None,
                            remote_multi_network: str = None,
                            dpd_action: str = None,
                            dpd_delay: str = None,
                            dpd_timeout: str = None,
                            identity: str = None):
        if remote_gateway:
            self._s.command_expect(f'remote-gateway {remote_gateway}')
        if interface:
            self._s.command_expect(f'interface {interface}')
        if startup_mode:
            self._s.command_expect(f'startup-mode {startup_mode}')
        if local_multi_network:
            self._s.command_expect(
                f'local-multi-network {local_multi_network}')
        if remote_multi_network:
            self._s.command_expect(
                f'remote-multi-network {remote_multi_network}')
        if identity:
            self._s.command_expect(f'identity {identity}')
        if dpd_action:
            self._s.command_expect(f'dpd-action {dpd_action}')
        if dpd_delay:
            self._s.command_expect(f'dpd-delay {dpd_delay}')
        if dpd_timeout:
            self._s.command_expect(f'dpd-timeout {dpd_timeout}')
        # quit to save
        self._s.command_expect(f'exit')
        return self

    def go_phase1(self, *args, **kwargs):
        """
        Configure an IPsec Phase 1.

            Args:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                object: An object of type rp_base_v2_0.ConfigIpsecPhase1.
        """
        return config_ipsec_phase1.ConfigIpsecPhase1(self._s, *args,
                                                **kwargs).getin()

    def go_phase2(self, *args, **kwargs):
        """
        Configure an IPsec Phase 2.

            Args:
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Returns:
                object: An object of type rp_base_v2_0.ConfigIpsecPhase2.
        """
        return config_ipsec_phase2.ConfigIpsecPhase2(self._s, *args,
                                                **kwargs).getin()
