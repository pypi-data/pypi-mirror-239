from mdc.router.cli.rp_base.ng_router import config
from mdc.router.cli.rp_base.ng_router.cli import PROMPT_CONFIG

class ConfigSessionControl(config.Config):
    """
        Class for configuring Session Control.

            ******** TBD ********
            Args:
                session (object): A valid session object.
                *args: Variable length argument list.
                **kwargs: Arbitrary keyword arguments.

            Attributes:
                _s (Session): A Session object used to communicate with the device.
                _args (list): A list of arguments passed to the function.
                _kwargs (dict): A dictionary of keyword arguments passed to the function.

            ******** /TBD ********
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
            Get into the session control.
            """
        self._s.command_expect(f'session-control')

    def getin(self):
        """
            Set the default prompts and get into the session control.

                Returns: 
                    self: The instance of the object. 
            """
        self._set_default_prompts()
        self._getin()
        return self

    def set_session_ctrl(self,
                         name: str = None,
                         enable: bool = None,
                         disable: str = None,
                         logging: str = None,
                         policy_action: str = None,
                         dip: str = None,
                         dport: str = None,
                         ttl_tcp_conn: str = None,
                         concur_tcp_conn: str = None):
        """
            Set Session Control policy on the device.

                Args:
                    name (str): Policy Name. 
                    enable (bool): Enable the Policy. 
                    disable (str): Disable the policy. 
                    logging (str): Enable or disable logging for this policy. 
                    policy_action (str): Allow or deny action for this policy. 
                    dip (str): Matching IP Address and Subnet Object as Destination IP. 
                    dport (str): Matching User-defined Service Object as Destination Port. 
                    ttl_tcp_conn(str):  Total TCP Connections Limitation.
                    concur_tcp_conn(str): Concurrent TCP Requests Limitation.

                Returns:   
                    self: The instance of the object.   
            """
        if name:
            self._s.command_expect(f'name {name}')
        if enable:
            self._s.command_expect('enable')
        if logging == "enable":
            self._s.command_expect('logging flash')  # left to be complete
        if policy_action in ["allow", "deny"]:
            if policy_action == 'allow':
                self._s.command_expect(f"action {'monitor'}")
            else:
                self._s.command_expect(f"action {'drop'}")
        if dip:
            self._s.command_expect(f"dst-ip {dip}")
        if dport:
            self._s.command_expect(f"dst-port {dport}")
        if ttl_tcp_conn:
            self._s.command_expect(f"total-tcp-conn {int(ttl_tcp_conn)}")
        if concur_tcp_conn:
            self._s.command_expect(
                f"concurrent-tcp-conn {int(concur_tcp_conn)}")
        if disable in ["no"]:
            pass  # left to be complete
        return self
