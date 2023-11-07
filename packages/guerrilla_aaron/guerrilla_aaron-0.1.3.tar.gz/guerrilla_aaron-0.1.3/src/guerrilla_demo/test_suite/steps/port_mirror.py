import time
from behave import *

@when('set mirrored port and mirror port on "{device}"')
def step_impl(context, device):
    print(context.table[0])
    src="1/"+context.host_info[context.table[0]['mirrored']]['testbed']['port']
    dst="1/"+context.host_info[context.table[0]['mirror']]['testbed']['port']

    context.dut[device].go_config().set_port_mirror(src=src,dst=dst)


@when('"{host}" start capture packet')
def step_impl(context, host):
    context.tcpdump_pid = context.hosts[host].shellcmd.tcpdump(itf=context.host_info[host]['nic'], filter_type="arp")


@when('"{host}" arp "{device}"s {interface}')
def step_impl(context, host, device, interface):
    context.arp_ip = context.dut_info[device]["testbed"][f"{interface.lower()}_ip"]
    context.hosts[host].shellcmd.arp(count=4, ip=context.arp_ip)
    time.sleep(5)

@then('"{host1}" will receive arp packet sent from "{host2}"')
def step_impl(context, host1, host2):
    ret = context.hosts[host1].shellcmd.get_tcpdumpfile(context.tcpdump_pid)
    assert f"Request who-has {context.arp_ip}" in ret, f"{host1} did not receive arp packet sent from {host2}"
