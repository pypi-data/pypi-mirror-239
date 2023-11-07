from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000 import config
from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000.cli import PROMPT_CONFIG

class ConfigRstp(config.Config):
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
         Get input from the device. This is a no - op if the device is not connected
        """
        self._s.command_expect(f'redundancy')

    def getin(self):
        """
         Set prompts to getin. This is a shortcut for _set_default_prompts ( self. _default_prompts )
         
            Returns: 
                self for daisychaining ( self )
        """
        self._set_default_prompts()
        self._getin()
        return self
    def set_rstp_rule(self,
                      priority: str = None,
                      hello_time: str = None,
                      fwd_delay: str = None,
                      max_age: str = None,
                      ):     
        """
        Set RSTP rule. This is a function that allows to set the spanning tree of a project based on the values passed to it
        
            Args:
                priority: priority of the rule in percent
                hellotime: time to wait before sending a message
                forwarddelay: time to wait before sending a message
                maxage: maximum age of the rule in seconds ( 0 - 9 )
            
            Returns: 
                self for daisychaining ( self )
        """
        # if priority is given, set the spanning tree priority
        if priority:
            self._s.command_expect(f'spanning-tree priority {priority}')
        # if hellotime is given, set the spanning tree hellotime
        if hello_time:
            self._s.command_expect(f'spanning-tree hello-time {hello_time}')
        # if forwarddelay is given, set the spanning tree forwarddelay
        if fwd_delay:
            self._s.command_expect(f'spanning-tree forward-delay {fwd_delay}')
        # if maxage is given, set the spanning tree maxage
        if max_age:
            self._s.command_expect(f'spanning-tree max-age {max_age}')
        return self
