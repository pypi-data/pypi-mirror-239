from mdc.router.cli.rp_base.lg_router.tn5000 import config
from mdc.router.cli.rp_base.lg_router.tn5000.cli import PROMPT_CONFIG

class ConfigL2filter(config.Config):
    """
    Class for configuring L2 filter.

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
        policy_index = self._args[0] if len(self._args) != 0 else None
        if policy_index is None:
            raise Exception(f"Input parameter is empty!")
        self._s.command_expect(f'l2-filter {policy_index}')

    def getin(self):
        self._set_default_prompts()
        self._getin()
        return self

    def action(self, action):
        action_list = ["accept", "drop"]

        if action in action_list:
            self._s.command_expect(f'action {action}')
        else:
            raise ValueError('action can be either accept or drop')

        return self

    def protocol(self, protocol="all"):
        self._s.command_expect(f'protocol {protocol}')

        return self

    def ether_type(self, ether_type):
        self._s.command_expect(f'ether-type {ether_type}')
        return self

    def src_mac(self, src_mac):
        self._s.command_expect(f'src-mac {src_mac}')
        return self

    def dst_mac(self, dst_mac):
        self._s.command_expect(f'dst-mac {dst_mac}')
        return self

    def interface(self, if_from="all", if_to="all"):
        self._s.command_expect(f'interface {if_from} {if_to}')
        return self

    def exit(self):
        ret = self._s.command_expect('exit',
                                        prompts=[PROMPT_CONFIG],
                                        timeout=2)
        return self

