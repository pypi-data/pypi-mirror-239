from guerrilla_aaron.mdc.router.cli.rp_base.ng_router import cli, main, config, config_brg, config_nat, config_dhcp, config_ospf, \
    config_if_lan, config_if_wan, config_if_vlan, config_if_ether, \
    config_ipsec, config_ipsec_phase1, config_ipsec_phase2, \
    config_l2_filter, config_l3_policy, \
    config_obj_addr, config_obj_serv, config_obj_net_serv, config_obj_indust_app_serv, \
    config_vrrp, config_session_ctrl, config_rstp, config_rip

class Base:

    class Cli(cli.Cli):
        pass
    class Main(main.Main):
        pass
    class Config(config.Config):
        pass
    class ConfigIfLan(config_if_lan.ConfigIfLan):
        pass
    class ConfigIfWan(config_if_wan.ConfigIfWan):
        pass
    class ConfigIfVlan(config_if_vlan.ConfigIfVlan):
        pass
    class ConfigIfEthernet(config_if_ether.ConfigIfEthernet):
        pass
    class ConfigBrg(config_brg.ConfigBrg):
        pass
    class ConfigL2filter(config_l2_filter.ConfigL2filter):
        pass
    class ConfigIpsec(config_ipsec.ConfigIpsec):
        pass
    class ConfigIpsecPhase1(config_ipsec_phase1.ConfigIpsecPhase1):
        pass
    class ConfigIpsecPhase2(config_ipsec_phase2.ConfigIpsecPhase2):
        pass
    class ConfigL37Policy(config_l3_policy.ConfigL37Policy):
        pass
    class ConfigSessionControl(config_session_ctrl.ConfigSessionControl):
        pass
    class ConfigObjectAddr(config_obj_addr.ConfigObjectAddr):
        pass
    class ConfigObjectServ(config_obj_serv.ConfigObjectServ):
        pass
    class ConfigObjectNetServ(config_obj_net_serv.ConfigObjectNetServ):
        pass
    class ConfigObjectIndustrialAppServ(config_obj_indust_app_serv.ConfigObjectIndustrialAppServ):
        pass
    class ConfigNat(config_nat.ConfigNat):
        pass
    class ConfigDhcp(config_dhcp.ConfigDhcp):
        pass
    class ConfigOspf(config_ospf.ConfigOspf):
        pass
    class ConfigVrrp(config_vrrp.ConfigVrrp):
        pass
    class ConfigRstp(config_rstp.ConfigRstp):
        pass
    class ConfigRip(config_rip.ConfigRip):
        pass