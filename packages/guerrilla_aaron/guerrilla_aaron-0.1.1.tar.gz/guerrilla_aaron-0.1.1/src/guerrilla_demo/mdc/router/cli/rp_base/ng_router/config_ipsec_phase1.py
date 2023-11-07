from mdc.router.cli.rp_base.ng_router import config
from mdc.router.cli.rp_base.ng_router.cli import PROMPT_CONFIG

class ConfigIpsecPhase1(config.Config):
    """
    Class for configuring IPSecPhase1.

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
        # Auxiliary method under ConfigIPSec so super init is not required
        self._s = session
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
        self._s.command_expect(f'phase1')

    def getin(self):
        """
        Set the default prompts and get into the interface wan.

            Returns: 
                self: The instance of the object. 
        """
        self._set_default_prompts()
        self._getin()
        return self

    def set_key_exchange(self,
                            ike_mode: str = None,
                            ike_version: str = None,
                            auth_mode_psk: str = None,
                            encryption: str = None,
                            hash_algo: str = None,
                            dh_group: str = None,
                            life_time: str = None):
        if ike_mode:
            self._s.command_expect(f'ike-mode {ike_mode}')
        if ike_version:
            self._s.command_expect(f'ike-version {ike_version}')
        if auth_mode_psk:
            self._s.command_expect(f'auth-mode psk {auth_mode_psk}')
        if encryption:
            self._s.command_expect(f'encryption {encryption}')
        if hash_algo:
            self._s.command_expect(f'hash {hash_algo}')
        if dh_group:
            self._s.command_expect(f'dh-group {dh_group}')
        if life_time:
            self._s.command_expect(f'life-time {life_time}')
        # quit to save
        self._s.command_expect(f'exit')
        return self
