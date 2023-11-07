from guerrilla_aaron.mdc.router.cli.rp_base.ng_router import config
from guerrilla_aaron.mdc.router.cli.rp_base.ng_router.cli import PROMPT_CONFIG

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
        policy_index = self._args[0] if len(self._args) != 0 else None
        if policy_index is None:
            raise Exception(f"Input parameter is empty!")
        self._s.command_expect(f'l2-filter {policy_index}')

    def getin(self):
        """
        Set the default prompts and get into the interface wan.

            Returns: 
                self: The instance of the object. 
        """
        self._set_default_prompts()
        self._getin()
        return self

    def action(self, action: str):
        """
        Set the action of the rule.

            Args:
                action (str): The action of the rule. Can be either "accept" or "drop". 
            
            Returns: 
                self: The instance of the object. 
        """
        action_list = ["accept", "drop"]

        if action in action_list:
            self._s.command_expect(f'action {action}')
        else:
            raise ValueError('action can be either accept or drop')

        return self

    def protocol(self, protocol: str = "all"):
        """
        Set the protocol of the rule. 

            Args: 
                protocol (str): The protocol of the rule. Default is "all". 

            Returns: 
                self: The instance of the object. 
        """
        self._s.command_expect(f'protocol {protocol}')

        return self

    def ether_type(self, ether_type: str):
        """
        Set the ether type of the rule. 

            Args: 
                ether_type (str): The ether type of the rule.  

            Returns: 
                self: The instance of the object.
        """
        self._s.command_expect(f'ether-type {ether_type}')
        return self

    def src_mac(self, src_mac: str):
        """
        Set source mac address of the rule.  

            Args:  
                src_mac (str): Source mac address to set for this rule.  

            Returns:  
                self: The instance of the object.
        """
        self._s.command_expect(f'src-mac {src_mac}')
        return self

    def dst_mac(self, dst_mac: str):
        """
        Set the destination MAC address of the rule.

            Args:
                dst_mac (str): The destination MAC address.

            Returns:
                self: The instance of the object.
        """
        self._s.command_expect(f'dst-mac {dst_mac}')
        return self

    def interface(self, if_from: str = "all", if_to: str = "all"):
        """
        Set the interfaces of the rule.

            Args:
                if_from (str, optional): The starting interface. Defaults to "all".
                if_to (str, optional): The ending interface. Defaults to "all".

            Returns:
                self: The instance of the object. 
        """
        self._s.command_expect(f'interface {if_from} {if_to}')
        return self

    def exit(self):
        """
        Exit the rule setting

                Returns:
                self: The instance of the object. 
        """
        ret = self._s.command_expect('exit',
                                        prompts=[PROMPT_CONFIG],
                                        timeout=2)
        return self
