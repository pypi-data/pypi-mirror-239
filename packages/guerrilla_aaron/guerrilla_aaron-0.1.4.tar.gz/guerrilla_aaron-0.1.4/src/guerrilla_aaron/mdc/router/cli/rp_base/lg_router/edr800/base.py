from mdc.router.cli.rp_base.lg_router.edr800 import cli, main, config, config_brg,\
    config_if_lan, config_if_wan, config_if_vlan, config_if_ether

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