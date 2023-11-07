import time
import random

from behave import *
from mdc.router.cli.rp_base.ng_router.base import Base
from mdc.router.cli.rp_base.lg_router.tn5000.base import Base as tn5000
from steps import common, interface, login

@when(u'send {pkt_count} vrrp packet with the content of the table from "{host}" to "{device}"')
def step_impl(context, pkt_count, host, device):
    ip_address = context.table[0]["addr_list"]
    padding_n = 14
    script = context.hosts[host].scapy.generate_vrrp_scapy_script(padding_n=padding_n,
                                                                  smac=context.host_info[host]["testbed"]["mac_address"],
                                                                  dmac="01:00:5e:00:00:12",
                                                                  sip=context.host_info[host]["testbed"]["cur_host"],
                                                                  dip="224.0.0.18",
                                                                  version=3,
                                                                  priority=context.table[0]["priority"],
                                                                  ip_address=ip_address,
                                                                  iface=context.host_info[host]["nic"]
                                                                  )
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
    os.system(f'rm ../lib/atb/service/scapy_template/{scapy_file_name}')

@when(u'set up vrrp on the "{device}" with the content of the table')
def step_imple(context, device):
    version = context.table[0]["version"]
    status = context.table[0]["status"]
    vrid = context.table[0]["vrid"]
    vip = context.table[0]["vip"]
    priority = context.table[0]["priority"]
    preempt_mode = context.table[0]["preempt_mode"]
    preempt_delay = context.table[0]["preempt_delay"]
    accept_mode = context.table[0]["accept_mode"]
    interface = context.table[0]["interface"]
    adver_interval = context.table[0]["adver_interval"]
    if issubclass(context.dut[device]._model, tn5000):
        context.adver_interval = int(adver_interval) / 100
    else:
        context.adver_interval = int(adver_interval) / 1000
    context.dut[device].go_config_vrrp(1).set_vrrp_rule(status = status,
                                                     vrid = vrid,
                                                     vip = vip,
                                                     priority = priority,
                                                     preempt_mode = preempt_mode,
                                                     preempt_delay = preempt_delay,
                                                     accept_mode = accept_mode,
                                                     interface = interface,
                                                     adver_interval = adver_interval,
                                                     adver_interval_ver = version
                                                     )
    context.dut[device].go_config().set_global_vrrp(version = version, status = status)


@then(u'vrrp status should be "{status}" on "{device}"')
def step_imple(context, status, device):
    flag = False
    for _ in range(int(context.adver_interval)):
        ret = context.dut[device].main().show_vrrp()
        if status in ret[0]["vrrp_status"]:
            flag = True
            break
        time.sleep(1)
    assert flag, f'vrrp do not change -> expect: {status} but {ret[0]["vrrp_status"]}'

@when(u'wait for {num} advertisement interval')
def step_imple(context, num):
    time.sleep(int(num) * int(context.adver_interval))