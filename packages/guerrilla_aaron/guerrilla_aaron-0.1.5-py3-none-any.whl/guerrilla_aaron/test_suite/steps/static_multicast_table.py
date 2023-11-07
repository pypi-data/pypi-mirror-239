import re
import sys
import time
import random

from host import *
from behave import *
from steps import common, interface, login


@when(u'set "{device}" a static multicast table with {mac} and "{port_name}"')
def step_impl(context, device, mac, port_name):
    context.mac = mac.replace('-', ':')
    port = context.dut_info[device]['testbed'][port_name]
    vlan = context.table[0]['Vlan'] if context.table else None
    context.dut[device].go_config().set_static_multicast_table(
        mac=context.mac, port=port, vlan=vlan)
    time.sleep(10)


@then(u'the following rule should be on "{device}"\'s static multicast table')
def step_impl(context, device):
    mac_table = context.dut[device].main().show_mac_address_table()
    port = context.dut_info[device]['testbed'][context.table[0]['Port']]
    flag = False

    for entry in mac_table:
        if entry['type'] == context.table[0]['Type'] and \
            entry['mac'] == context.table[0]['MAC'].upper() and \
            entry['port'] == f'1/{port}':
            flag = True
            break
    assert flag, f'expect: [mac: {context.table[0]["MAC"].upper()},type: {context.table[0]["Type"]}, port: 1/{port}] , actual: {mac_table}'

@when(
    u'send {pkt_count} layer 2 multicast packet from "{host_send}" to {mac}'
)
def step_impl(context, pkt_count, host_send, mac):
    # fill multicast scapy script with args
    dst_mac = mac.replace('-', ':')
    src_mac = context.host_info[host_send]['testbed']['mac_address']
    dst_nic = context.host_info[host_send]["nic"]
    script = context.hosts[host_send].scapy.generate_multicast_scapy_script(
        dst_mac, src_mac, dst_nic, pkt_count)

    from datetime import datetime
    import os

    # write the scapy script to file
    scapy_file_name = datetime.now().isoformat().replace(":", "_")[:19]
    with open(f'../lib/atb/service/scapy_template/{scapy_file_name}',
              "w") as script_file:
        script_content = script_file.write(script)

    # scp the file to remote host with scapy service
    os.system('sshpass -p "{0}" scp {1} {2}@{3}:~/'.format(
        context.host_info[host_send]['session']['credential']['password'],
        f"../lib/atb/service/scapy_template/{scapy_file_name}",
        context.host_info[host_send]['session']['credential']['username'],
        context.host_info[host_send]['session']['host']))

    context.hosts[host_send].scapy.do_script(scapy_file_name)
    # Clean up
    os.system(f'rm ../lib/atb/service/scapy_template/{scapy_file_name}')


@then(
    u'"{host_recv}" shall "{result}" to receive layer 2 multicast packets from "{host_send}"'
)
def step_impl(context, host_recv, result, host_send):
    time.sleep(5)
    context.hosts[host_recv].tshark.stop()
    ret = context.hosts[host_recv].tshark.retrieve()

    if len(ret) == 0:
        raise ValueError('packet receiving fails')

    pkt_count = 0
    ret_lines = ret.split('\n')
    for a in ret_lines:
        arr = re.split(r'\s+', a.lstrip())
        # skip if not tshark packet
        if arr[0].isdigit() == False or len(arr) < 5:
            continue
        if arr[3] != '→':
            raise ValueError(f'unexpected tshark format {a}')

        # Match Source and Destination IP Address
        if arr[2] == context.host_info[host_send]['testbed'][
                'mac_address'] and arr[4] == context.mac:
            pkt_count += 1

    if result == 'fail':
        assert pkt_count == 0, f'{host_recv} expect to receive no packets but receive {pkt_count}'
    elif result == 'success':
        assert pkt_count > 0, f'{host_recv} expect to receive packets but receive {pkt_count}'
