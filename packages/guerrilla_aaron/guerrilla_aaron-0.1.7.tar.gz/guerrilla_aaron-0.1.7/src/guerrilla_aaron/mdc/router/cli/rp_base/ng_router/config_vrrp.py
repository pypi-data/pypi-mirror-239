from guerrilla_aaron.mdc.router.cli.rp_base.ng_router import config
from guerrilla_aaron.mdc.router.cli.rp_base.ng_router.cli import PROMPT_CONFIG

class ConfigVrrp(config.Config):
    def __init__(self, session: object, *args, **kwargs):
        """
         Initialize the instance. This is called by the : class : ` Session ` when it is created.
         
            Args:
                session: The session to use for the request / response
        """
        super().__init__(session)
        self._args = args
        self._kwargs = kwargs

    def _set_default_prompts(self):
        """
         Set the default prompts for this service. This is called by __init__ and should not be called by user code
        """
        self._s.set_default_prompts([PROMPT_CONFIG])

    # Reserve flexibility for function override
    def _getin(self):
        """
         Get in vrrp index from command line. @param self : class object. @return None
        """
        # default apply the first element as parameter
        vrrp_index = self._args[0] if len(self._args) != 0 else None
        # Check if vrrp_index is not None.
        if vrrp_index is None:
            raise Exception(f"Need vrrp index!")
        self._s.command_expect(f'vrrp {vrrp_index}')

    def getin(self):
        """
         Set prompts to getin. This is a shortcut for _set_default_prompts ( self. _default_prompts )
         
         
            Returns: 
                self for daisychaining ( self )
        """
        self._set_default_prompts()
        self._getin()
        return self

    def set_vrrp_rule(self,
                      status: str = None,
                      vrid: str = None,
                      vip: str = None,
                      priority: str = None,
                      preempt_mode: str = None,
                      preempt_delay: str = None,
                      accept_mode: str = None,
                      interface: str = None,
                      adver_interval: str = None,
                      adver_interval_ver: str = "v3"
                      ):
        """
        Set VRRP rule. This is a helper method to allow you to set a rule in the configuration file.
        
            Args:
                status: The status of the rule. Valid values are enabled disabled and un - enabled.
                vrid: The ID of the Virtual Router to set the rule to.
                vip: The IP address of the Virtual Router to set the rule to.
                priority: The priority of the rule. Valid values are 1 - 4.
                preempt_mode: The preempt mode of the rule. Valid values are enabled and disabled.
                accept_mode: The accept mode of the rule. Valid values are enabled and disabled.
                interface: The interface for the rule. Valid values are " eth0 " " eth1 " and " ethernet ".
                adver_interval: The advertisement interval in seconds. Default is 1 second.
                adver_interval_ver: The advertising interval version in seconds. Default is v3.
            
            Returns: 
                self for daisychaining ( self )
        """
                      
        # expects vrid to be passed to the command
        if vrid:
            self._s.command_expect(f'vrid {vrid}')
        # expect virtual ip if vip is given
        if vip:
            self._s.command_expect(f'virtual-ip {vip}')
        # Expects the command to expect priority
        if priority:
            self._s.command_expect(f'priority {priority}')
        # Enable or disable preempting the command.
        if preempt_mode:
            # Enable or disable preempting the command
            if preempt_mode == "enable":
                if preempt_delay:
                    self._s.command_expect(f'preempt delay {preempt_delay}')
                else:
                    self._s.command_expect(f'preempt')
            elif preempt_mode == "disable":
                self._s.command_expect(f'no preempt')
            else:
                raise ValueError(f"Input invalid preempt status: {preempt_mode}")
        # accept_mode is one of enable disable or enable
        if accept_mode:
            # Accept mode enable disable or enable
            if accept_mode == "enable":
                self._s.command_expect(f'accept')
            elif accept_mode == "disable":
                self._s.command_expect(f'no accept')
            else:
                raise ValueError(f"Input invalid accept status: {accept_mode}")
        # expect interface interface interface interface.
        if interface:
            self._s.command_expect(f'interface {interface}')
        # expects the command to be called at the adver interval
        if adver_interval:
            self._s.command_expect(f'adver-interval v{adver_interval_ver} {adver_interval}')
        # Enable or disable the command.
        if status:
            # Enable or disable the command.
            if status == "enable":
                self._s.command_expect(f'vrrp')
            elif status == "disable":
                self._s.command_expect(f'no vrrp')
            else:
                raise ValueError(f"Input invalid status: {status}")
        return self
