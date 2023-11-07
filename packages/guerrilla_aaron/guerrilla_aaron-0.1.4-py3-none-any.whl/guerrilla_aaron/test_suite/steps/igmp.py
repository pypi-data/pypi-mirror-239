import time
from behave import *
from steps import common, interface, login

@when(u'{action} igmp-snooping {version} with vlan {vid} on "{device}"')
def step_impl(context, action, version, vid, device):
    cfg = context.dut[device].go_config()
    if action == 'enable':
        cfg.IgmpSnooping(cfg.get_session()).set_igmp_snooping_vlan(action = action, 
                                                                vid = vid)
        cfg.IgmpSnooping(cfg.get_session()).set_igmp_snooping_querier(action = action, 
                                                                    vid = vid)
    elif action == 'disable':
        cfg.IgmpSnooping(cfg.get_session()).set_igmp_snooping_vlan(action = action, 
                                                                vid = vid)
    else:
        raise ValueError(f'input invalid action: {action}')


@when(u'set igmp-snooping query interval to {interval} on "{device}"')
def step_impl(context, interval, device):
    cfg = context.dut[device].go_config()
    cfg.IgmpSnooping(cfg.get_session()).set_igmp_snooping_interval(interval)
    

@when(u'send igmp {igmp_type} with following format from "{host}" to "{device}"')
def step_impl(context, host, device, igmp_type):
    igmp = {
        "query":{
            "sip": context.host_info[host]['testbed']['lan_host'],
            "dip": context.table[0]['dip'],
            "type": "IGMP(type=0x11)",
            "igmp_group_addr": context.table[0]['igmp_group_addr']
        },
        "join":{
            "sip": context.host_info[host]['testbed']['lan_host'],
            "dip": context.table[0]['dip'],
            "type": "IGMP(type=0x16)",
            "igmp_group_addr": context.table[0]['igmp_group_addr']
        },
        "leave":{
            "sip": context.host_info[host]['testbed']['lan_host'],
            "dip": context.table[0]['dip'],
            "type": "IGMP(type=0x17)",
            "igmp_group_addr": context.table[0]['igmp_group_addr']
        }
    }
    padding_n = "22"
    count = "1"
    iface = context.host_info[host]['nic']

    # fill igmp scapy script with args
    script = context.hosts[host].scapy.generate_igmp_scapy_script(igmp[igmp_type]["sip"], igmp[igmp_type]["dip"], 
                                                                padding_n, igmp[igmp_type]["type"], igmp[igmp_type]["igmp_group_addr"],
                                                                count, iface)
    from datetime import datetime
    import os

    # write the scapy script to file
    scapy_file_name = datetime.now().isoformat().replace(":", "_")[:19]
    with open(f'../lib/atb/service/scapy_template/{scapy_file_name}', "w") as script_file:
        script_content = script_file.write(script)

    # scp the file to remote host with scapy service
    os.system('sshpass -p "{0}" scp {1} {2}@{3}:~/'.format(context.host_info[host]['session']['credential']['password'],
                                                            f"../lib/atb/service/scapy_template/{scapy_file_name}",
                                                            context.host_info[host]['session']['credential']['username'],
                                                            context.host_info[host]['session']['host']))
    context.hosts[host].scapy.do_script(scapy_file_name)
    # Clean up
    os.system(f'rm ../lib/atb/service/scapy_template/{scapy_file_name}')
    

@then(u'igmp group should be {action} on "{device}"')
def step_impl(context, action, device):
    time.sleep(5)
    ret = context.dut[device].main().show_ip_igmp()
    flag = False
    for item in ret:
        flag = True if context.table[0]['igmp_group_addr'] == item['group'].replace(' ', '') else False
        if flag: break
    if action == 'added':
        assert flag, \
        f'\nexpect: {context.table[0]["igmp_group_addr"]}\nactual: {ret}'
    elif action == 'removed':
        assert not flag, \
        f'\nexpect: {context.table[0]["igmp_group_addr"]}\nactual: {ret}'
    else:
        raise ValueError(f'input wrong action: {action}')
    

@then(u'querier will be changed from "{device_1}" to "{device_2}"')
def step_impl(context, device_1, device_2):
    # skip the initial query packet
    time.sleep(5)
    if "DUT" in device_2:
        context.hosts[device_1].tshark.start(
            interface=context.host_info[device_1]["nic"],
            capture_filter='igmp')
        time.sleep(60)
        context.hosts[device_1].tshark.stop()
        capture_pkt = context.hosts[device_1].tshark.retrieve()
        querier_mac = f'{context.dut_info[device_2]["testbed"]["lan_ip"]} → 224.0.0.1'
        assert capture_pkt.count(querier_mac) >= 3, \
            f'querier does not change to {device_2}:\ncapture_pkt: {capture_pkt}'

    elif "DUT" in device_1:
        capture_pkt = context.hosts[device_2].tshark.start(
            interface=context.host_info[device_2]["nic"],
            capture_filter='igmp')
        time.sleep(60)
        context.hosts[device_2].tshark.stop()
        capture_pkt = context.hosts[device_2].tshark.retrieve()
        querier_mac = f'{context.dut_info[device_1]["testbed"]["lan_ip"]} → 224.0.0.1'
        assert capture_pkt.count(querier_mac) == 0, \
            f'querier does not change to {device_2}\ncapture_pkt: {capture_pkt}'
    else:
        raise ValueError(f'its only supported between HOST and DUT')

@when(u'wait for active time')
def step_impl(context):
    query_interval = context.table[0]["query_interval"]
    active_time = 2 * int(query_interval) + 10
    time.sleep(active_time)


@when(u'{action} global igmp-snooping on "{device}"')
def step_impl(context, action, device):
    cfg = context.dut[device].go_config()
    if action == 'enable':
        cfg.IgmpSnooping(cfg.get_session()).set_global_igmp_snooping(action)
    elif action == 'disable':
        cfg.IgmpSnooping(cfg.get_session()).set_global_igmp_snooping(action)
    else:
        raise ValueError(f'input invalid action: {action}')