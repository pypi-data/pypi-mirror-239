from mdc.router.cli.md_tn5916.tn5916_v3 import tn5916_v3_0

class tn5916_v3_0_27(tn5916_v3_0):
    class ConfigIfEthernet(tn5916_v3_0.ConfigIfEthernet):
        def set_bridge_group(self, group: int = None):
                self._s.command_expect(f'bridge group')
                return self
