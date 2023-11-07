import re
import time
import random
from behave import *
from steps import common, interface, login

@when(u'send {pkt_count} rstp packet with the content of the table from "{host}" to "{device}"')
def step_impl(context, pkt_count, host, device):
    padding_n = 8
    dmac = "01:80:c2:00:00:00"
    brid = context.table[0]['brid']
    max_age = context.table[0]['max_age']
    iface = context.host_info[host]['nic']
    path_cost = context.table[0]['path_cost']
    fwd_delay = context.table[0]['fwd_delay']
    hello_time = context.table[0]['hello_time']
    smac = context.host_info[host]['testbed']['mac_address']
    script = context.hosts[host].scapy.generate_rstp_scapy_script(smac=smac,
                                                                  dmac=dmac,
                                                                  brid=brid,
                                                                  iface=iface,
                                                                  max_age=max_age,
                                                                  path_cost=path_cost, 
                                                                  fwd_delay=fwd_delay,
                                                                  hello_time=hello_time,
                                                                  padding_n = padding_n)
    from datetime import datetime
    import os

    # write the scapy script to file
    scapy_file_name = datetime.now().isoformat().replace(":", "_")[:19]
    with open(f'../lib/atb/service/scapy_template/{scapy_file_name}', "w") as script_file:
        script_content = script_file.write(script)
    
    os.system('sshpass -p "{0}" scp {1} {2}@{3}:~/'.format(context.host_info[host]['session']['credential']['password'],
                                                            f"../lib/atb/service/scapy_template/{scapy_file_name}",
                                                            context.host_info[host]['session']['credential']['username'],
                                                            context.host_info[host]['session']['host']))
    # Clean up
    for _ in range(int(pkt_count)):
        context.hosts[host].scapy.do_script(scapy_file_name)
    context.hosts[host].scapy.clean_up()
    os.system(f'rm ../lib/atb/service/scapy_template/{scapy_file_name}')

@when(u'{action} spanning tree on "{device}" with following table')
def step_impl(context, device, action):
    priority = context.table[0]["brid"]
    hello_time = context.table[0]["hello_time"]
    fwd_delay = context.table[0]["fwd_delay"]
    max_age = context.table[0]["max_age"]
    context.dut[device].go_config_rstp().set_rstp_rule(priority,
                                                       hello_time,
                                                       fwd_delay,
                                                       max_age)
    cfg = context.dut[device].go_config()
    cfg.Rstp(cfg.get_session()).set_rstp_status(action)

@when(u'{action} spanning tree on port {port} of "{device}" with following table')
def step_impl(context, action, port, device):
    edge_port = True if context.table[0]["edge_port"] == "enable" else False
    priority = context.table[0]["pid"]
    cost = context.table[0]["path_cost"]
    cfg = context.dut[device].go_config()
    cfg.Rstp(cfg.get_session()).set_rstp_port(port,
                                              action = action,
                                              edge_port = edge_port,
                                              priority = priority,
                                              cost = cost)

@then(u'rstp status should be "{status}" on "{device}"')
def step_impl(context, status, device):
    flag = False
    for _ in range(10):
        ret = context.dut[device].main().show_rstp()
        if ret[0]["role"] == status:
            flag = True
            break
        time.sleep(1)
    assert flag, f"rstp status is not: {status}"

@then(u'"{host}" shall receive {expect_pkt_num} hello packet in {wait_time} sec')
def step_impl(context, host, expect_pkt_num, wait_time):
    context.hosts[host].tshark.start(interface=context.host_info[host]["nic"], capture_filter='stp')
    time.sleep(int(wait_time))
    context.hosts[host].tshark.stop()
    ret = context.hosts[host].tshark.retrieve()
    pkt_num = ret.count("STP")
    assert int(pkt_num) >= int(expect_pkt_num), f"expect received packet number: {expect_pkt_num}, but {pkt_num}\nRaw: {ret}"

@then(u'"{host}" shall receive rstp packet with the content of the table')
def step_impl(context, host):
    expect_info = {"brid": "Bridge Priority",
                   "hello_time": "Hello Time",
                   "fwd_delay": "Forward Delay",
                   "max_age": "Max Age"}[context.table.headings[0]]
    context.hosts[host].tshark.start(interface=context.host_info[host]["nic"], capture_filter='stp', additional_options=f"-V | grep '{expect_info}'")
    time.sleep(5)
    context.hosts[host].tshark.stop()
    ret = context.hosts[host].tshark.retrieve()
    expect_value = context.table[0][context.table.headings[0]]
    actual_value = re.findall(rf"{expect_info}: (\d+)", ret)

    assert all(element == expect_value for element in actual_value), \
        f"expect {expect_info}: {expect_value}, but {actual_value}"