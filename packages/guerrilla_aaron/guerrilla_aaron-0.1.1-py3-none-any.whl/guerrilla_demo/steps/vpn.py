from behave import *

@when('set IPSec tunnel on "{device}"')
def step_impl(context, device):
    context.dut[device].go_config_ipsec(context.table[0]['vpn_name']).set_vpn_connection(
                                remote_gateway=context.table[0]["remote-gateway"], 
                                interface="WAN", 
                                startup_mode=context.table[0]["startup-mode"],
                                local_multi_network=context.table[0]["local-multi-network"], 
                                remote_multi_network=context.table[0]["remote-multi-network"],
                                dpd_action=context.table[0]["dpd-action"], 
                                dpd_delay=context.table[0]["dpd-delay"], 
                                dpd_timeout=context.table[0]["dpd-timeout"],
                                identity=context.table[0]["identity"])

    context.dut[device].go_config_ipsec(context.table[0]['vpn_name']).go_phase1().set_key_exchange(
                                ike_mode=context.table[0]["ike-mode"],
                                ike_version=context.table[0]["ike-version"],
                                auth_mode_psk=context.table[0]["auth-mode psk"],
                                encryption=context.table[0]["encryption"],
                                hash_algo="sha256",
                                dh_group="2048",
                                life_time=context.table[0]["life-time"])


    context.dut[device].go_config_ipsec(context.table[0]['vpn_name']).go_phase2().set_data_exchange(
                                pfs=context.table[0]["pfs"], 
                                encryption=context.table[0]["encryption"], 
                                hash_algo="sha256", 
                                life_time=context.table[0]["life-time"])


