from typing import Any

from mdc.router.cli.md_tn5916.tn5916_v3 import tn5916_v3_0
from mdc.router.cli.md_tn5916.tn5916_v3_0_27 import tn5916_v3_0_27
from mdc.router.cli.md_edr810.edr810_v5 import edr810_v5_0
from mdc.router.cli.md_edr8010.edr8010_v3 import edr8010_v3_0
from mdc.router.cli.md_edrg9010.edrg9010_v2 import edrg9010_v2_0
from mdc.router.cli.md_edrg9010.edrg9010_v3 import edrg9010_v3_0
# from mdc.router.cli.md_oncellg4302.oncellg4302_v3 import oncellg4302_v3_0

class Router:
    
    def __init__(self, session, model):
        print(f'You are using Router {model} lib')
        self._s = session
        self._model = eval(model)
        self._model_name = model

    # ==== Router API portion ==== #
    def close(self):
        self._s.close()

    def main(self):
        return self._model.Main(self._s, self._model)

    def go_config(self):
        return self._model.Config(self._s)

    def go_config_if_lan(self, *args, **kwargs):
        return self._model.ConfigIfLan(self._s, *args, **kwargs).getin()

    def go_config_if_wan(self, *args, **kwargs):
        return self._model.ConfigIfWan(self._s, *args, **kwargs).getin()

    def go_config_if_vlan(self, *args, **kwargs):
        return self._model.ConfigIfVlan(self._s, *args, **kwargs).getin()

    def go_config_if_ethernet(self, *args, **kwargs):
        return self._model.ConfigIfEthernet(self._s, *args, **kwargs).getin()

    def go_config_bridge(self, *args, **kwargs):
        return self._model.ConfigBrg(self._s, *args, **kwargs).getin()

    def go_config_l2filter(self, *args, **kwargs):
        return self._model.ConfigL2filter(self._s, *args, **kwargs).getin()

    def go_config_ipsec(self, *args, **kwargs):
        return self._model.ConfigIpsec(self._s, *args, **kwargs).getin()

    def go_config_object_addr(self, *args, **kwargs):
        return self._model.ConfigObjectAddr(self._s, *args, **kwargs).getin()

    def go_config_object_serv(self, *args, **kwargs):
        return self._model.ConfigObjectServ(self._s, *args, **kwargs).getin()

    def go_config_object_net_serv(self, *args, **kwargs):
        return self._model.ConfigObjectNetServ(self._s, *args, **kwargs).getin()

    def go_config_object_industrial_app_serv(self, *args, **kwargs):
        return self._model.ConfigObjectIndustrialAppServ(self._s, *args, **kwargs).getin()

    def go_config_l37policy(self, *args, **kwargs):
        return self._model.ConfigL37Policy(self._s, *args, **kwargs).getin()
    
    def go_config_session_ctrl(self, *args, **kwargs):
        return self._model.ConfigSessionControl(self._s, *args, **kwargs).getin()

    def go_config_nat(self, *args, **kwargs):
        return self._model.ConfigNat(self._s, *args, **kwargs).getin()

    def go_config_dhcp(self, *args, **kwargs):
        return self._model.ConfigDhcp(self._s, *args, **kwargs).getin()

    def go_config_firewall(self, *args, **kwargs):
        return self._model.ConfigFirewall(self._s, *args, **kwargs).getin()

    def go_config_ospf(self, *args, **kwargs):
        return self._model.ConfigOspf(self._s, *args, **kwargs).getin()

    def go_config_vrrp(self, *args, **kwargs):
        return self._model.ConfigVrrp(self._s, *args, **kwargs).getin()

    def go_config_rstp(self, *args, **kwargs):
        return self._model.ConfigRstp(self._s, *args, **kwargs).getin()
    
    def go_config_rip(self, *args, **kwargs):
        return self._model.ConfigRip(self._s, *args, **kwargs).getin()