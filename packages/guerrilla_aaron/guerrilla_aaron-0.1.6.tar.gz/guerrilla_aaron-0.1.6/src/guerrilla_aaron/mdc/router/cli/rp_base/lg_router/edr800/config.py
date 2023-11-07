from utils.input_chk import chk_valid_ip
from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.edr800 import cli
from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.edr800.cli import PROMPT_CONFIG

class Config(cli.Cli):
    """
    Class for configuring a device through the command line interface.

        Args:
            session (Session): A Session object used to communicate with the device.

        Attributes:
            _s (Session): A Session object used to communicate with the device.
    """

    def __init__(self, session):
        super().__init__(session)
        # back to main
        self._back_to_main()
        # jumpt to config terminal
        self.getin_cfg()

    def get_session(self):
        return self._s

    def _set_default_prompts_cfg(self):
        self._s.set_default_prompts([PROMPT_CONFIG])

    def _getin_cfg(self):
        self._s.command_expect('configure terminal')

    # function override is allowed
    def getin_cfg(self):
        self._set_default_prompts_cfg()
        self._getin_cfg()
        return self

    def set_fast_bootup(self, global_toggle=None):
        if global_toggle:
            if global_toggle == "enable":
                self.command(f"fast-bootup")
            elif global_toggle == "disable":
                self.command(f"no fast-bootup")
            else:
                raise ValueError(
                    f'input invalid global_toggle: {global_toggle}')
