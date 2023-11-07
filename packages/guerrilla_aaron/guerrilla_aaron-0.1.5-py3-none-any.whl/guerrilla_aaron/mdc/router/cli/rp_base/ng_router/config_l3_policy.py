from mdc.router.cli.rp_base.ng_router import config
from mdc.router.cli.rp_base.ng_router.cli import PROMPT_CONFIG

class ConfigL37Policy(config.Config):
    """
    Class for configuring L37 Policy.

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

    def _getin(self):
        """
        Get into the interface lan.
        """
        self._s.command_expect(f'l3l7-policy')

    def getin(self):
        """
        Set the default prompts and get into the interface wan.

            Returns: 
                self: The instance of the object. 
        """
        self._set_default_prompts()
        self._getin()
        return self

    def set_l37_policy(self,
                        name=None,
                        enable=None,
                        disable=None,
                        logging=None,
                        itf=None,
                        policy_action=None,
                        mode=None,
                        sip=None,
                        dip=None,
                        sport=None,
                        dport=None,
                        smac=None,
                        dmac=None):
        """
        Set L37 policy on the device.

            Args:
                name (str): Name of the policy. 
                enable (bool): Enable the policy. 
                disable (str): Disable the policy. 
                logging (str): Enable or disable logging for this policy. 
                itf (dict): Interface in and out for the policy. 
                policy_action (str): Allow or deny action for this policy. 
                mode (str): Mode of this policy, ip, ip-mac or mac. 
                sip (str): Source IP address for this policy. 
                dip (str): Destination IP address for this policy. 
                sport (str): Source port for this policy. 
                dport (str): Destination port for this policy. 
                smac (str): Source MAC address for this policy. 
                dmac (str): Destination MAC address for this policy.  

            Returns:   
                self: The instance of the object.   
        """
        if itf["in"] == 'BRG':
            itf["in"] = 'BRG_LAN'
        if itf["out"] == 'BRG':
            itf["out"] = 'BRG_LAN'
        if name:
            self._s.command_expect(f'name {name}')
        if enable == True:
            self._s.command_expect('enable')
        if logging == "enable":
            self._s.command_expect('logging')  # left to be complete
        if itf:
            self._s.command_expect(f'interface {itf["in"]} {itf["out"]}')
        if policy_action in ["allow", "deny"]:
            self._s.command_expect(f"action {policy_action}")
        if mode in ["ip", "ip-mac", "mac"]:
            self._s.command_expect(f"mode {mode}")
        if sip:
            self._s.command_expect(f"src-ip {sip}")
        if dip:
            self._s.command_expect(f"dst-ip {dip}")
        if sport:
            self._s.command_expect(f"src-port {sport}")
        if dport:
            self._s.command_expect(f"dst-port {dport}")
        if smac:
            self._s.command_expect(f"src-mac {smac}")
        if dmac:
            self._s.command_expect(f"dst-mac {dmac}")
        if disable in ["no"]:
            pass  # left to be complete
        return self
