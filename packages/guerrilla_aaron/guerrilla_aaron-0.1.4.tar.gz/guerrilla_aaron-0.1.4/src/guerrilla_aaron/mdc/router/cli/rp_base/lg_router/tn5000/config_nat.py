from mdc.router.cli.rp_base.lg_router.tn5000 import config
from mdc.router.cli.rp_base.lg_router.tn5000.cli import PROMPT_CONFIG

class ConfigNat(config.Config):
    """
    Class for configuring NAT service.

        Args:
            session (object): The session object.
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

    def _getin(self):
        self._s.command_expect(f'')

    def getin(self):
        self._set_default_prompts()
        self._getin()
        return self

    # 1-1
    def set_one2one_rule(self, ipaddr_in, if_out, ipaddr_out, vrrp=None):
        cmd = f"ip nat static inside {ipaddr_in} outside {if_out} {ipaddr_out}"
        if vrrp:
            cmd += " redundancy {vrrp}"
        self._s.command_expect(cmd)

    # pat
    def set_port_forward_rule(self, protocol, ipaddr_in, port_in, if_out,
                                port_out):
        cmd = "ip nat static "
        if protocol in ["tcp", "udp", "all"]:
            cmd += f"{protocol} inside {ipaddr_in} {port_in} outside {if_out} {port_out}"
        else:
            raise ValueError(f"Input invalid protocol {protocol}!")
        self._s.command_expect(cmd)

    # n-1
    def set_dynamic_rule(self, ipaddr_start, ipaddr_end, if_out):
        cmd = f"ip nat dynamic inside {ipaddr_start} {ipaddr_end} outside {if_out}"
        self._s.command_expect(cmd)
