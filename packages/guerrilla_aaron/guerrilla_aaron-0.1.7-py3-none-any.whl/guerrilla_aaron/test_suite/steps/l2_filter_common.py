import re
import sys
import time

from guerrilla_aaron.host import *
from behave import *
from guerrilla_aaron.steps import common, interface, login


@given('starts tshark sniffer on "{host}"')
@when('starts tshark sniffer on "{host}"')
def step_impl(context, host):
    if context.table:
        context.hosts[host].tshark.start(interface=context.table[0]['iface'], \
                                         capture_filter=context.table[0]['filter'], \
                                         display_filter=context.table[0]['display'])
    else:
        context.hosts[host].tshark.start(interface=context.host_info[host]['nic'])


@when('"{host_send}" send {count} ICMP ping to "{host_recv}"')
def step_impl(context, host_send, count, host_recv):
    context.hosts[host_send].shellcmd.remove_arp_entry(
        dev = context.host_info[host_send]['nic'], \
        ip = context.host_info[host_recv]['testbed']['cur_host'], \
    )
    context.hosts[host_send].hping3.send( \
        tcpudp_flags=['icmp'], \
        host = context.host_info[host_recv]['testbed']['cur_host'], \
        count = count,
        interval = "100000")
    time.sleep(2)


@when('"{host_send}" send {count} ARP probe to "{host_recv}"')
def step_impl(context, host_send, count, host_recv):
    arp_scapy_syntax = f"Ether(\
        dst=\"{context.host_info[host_recv]['testbed']['mac_address']}\", \
        src=\"{context.host_info[host_send]['testbed']['mac_address']}\", \
        type=0x806)"

    context.hosts[host_send].scapy.send(scapy_syntax=arp_scapy_syntax,
                                        dev=context.host_info[host_send]['nic'],
                                        count=int(count))
    time.sleep(2)


@then('"{host_recv}" shall receive {count} ICMP request from "{host_send}"')
def step_impl(context, host_recv, count, host_send):
    context.hosts[host_recv].tshark.stop()

    ret = context.hosts[host_recv].tshark.retrieve()
    print('receive packets: ', ret)

    if len(ret) == 0:
        raise ValueError('packet receiving fails')

    ret_lines = ret.split('\n')

    destip_count = {}
    # parse and get dest IP counts
    for a in ret_lines:
        # skip if not ICMP request
        if a.find("Echo (ping) request") == -1:
            continue

        arr = a.lstrip(' ').split(' ')

        # skip unexpected format
        if arr[3] != '→':
            raise ValueError(f'unexpected tshark format {a}')

        if arr[4] in destip_count:
            destip_count[arr[4]] += 1
        else:
            destip_count[arr[4]] = 1

    # compare dest ip count
    host_recv_ip = context.host_info[host_recv]['testbed']['cur_host']

    if host_recv_ip not in destip_count:
        recv_packet_count = 0
    else:
        recv_packet_count = destip_count[host_recv_ip]

    assert int(recv_packet_count) == int(
        count
    ), f'{host_recv} expect to receive {count} packets but receive {recv_packet_count}'


@then('"{host_recv}" shall receive {count} ARP probe from "{host_send}"')
def step_impl(context, host_recv, count, host_send):
    context.hosts[host_recv].tshark.stop()

    ret = context.hosts[host_recv].tshark.retrieve()

    if len(ret) == 0:
        raise ValueError('packet receiving fails')

    pkt_count = 0

    ret_lines = ret.split('\n')
    for a in ret_lines:
        # skip if not ICMP request
        if a.find("ARP") == -1:
            continue

        arr = a.lstrip(' ').split(' ')

        # skip unexpected format
        if arr[3] != '→':
            raise ValueError(f'unexpected tshark format {a}')

        # Match Source and Destination MAC Address
        if arr[2] == context.host_info[host_send]['testbed'][
                'mac_address'] and arr[4] == context.host_info[host_recv][
                    'testbed']['mac_address']:
            pkt_count += 1

    assert pkt_count == int(
        count
    ), f'{host_recv} expect to receive {count} packets but receive {pkt_count}'


@given('l2-policy install on "{dut}"')
def step_impl(context, dut):
    if context.table[0]['src_mac'] == "all":
        src_mac = "00:00:00:00:00:00"
    elif context.table[0]['src_mac'].find('\'s') != -1:
        host_name = context.table[0]['src_mac'].split('\'')[0]
        src_mac = context.host_info[host_name]["testbed"]["mac_address"]
    else:
        src_mac = context.table[0]['src_mac']

    if context.table[0]['dst_mac'] == "all":
        dst_mac = "00:00:00:00:00:00"
    elif context.table[0]['dst_mac'].find('\'s') != -1:
        host_name = context.table[0]['dst_mac'].split('\'')[0]
        dst_mac = context.host_info[host_name]["testbed"]["mac_address"]
    else:
        dst_mac = context.table[0]['dst_mac']

    if context.table[0]['ethertype'] == "all":
        context.dut[dut].go_config_l2filter(1).\
            action(context.table[0]['action']).\
            protocol("all").\
            src_mac(src_mac).\
            dst_mac(dst_mac).\
            exit()
    else:
        context.dut[dut].go_config_l2filter(1).\
            action(context.table[0]['action']).\
            protocol("manual").\
            ether_type(context.table[0]['ethertype']).\
            src_mac(src_mac).\
            dst_mac(dst_mac).\
            exit()


@when('change "{host}" MAC address, which is different from the original one')
def step_impl(context, host):
    orig_mac = context.host_info[host]["testbed"]["mac_address"]
    orig_mac_arr = orig_mac.split(":")
    another_mac = ""

    # "+1" to current MAC address (wrap around if needed)
    for i in range(0, 6):
        if i != 0:
            another_mac += ":"
        if i == 5:
            another_mac += f'{(int(orig_mac_arr[i], 16)+1)%256:0{2}x}'
        else:
            another_mac += orig_mac_arr[i]

    use_fixture(changeHostMacAndRestore, context, host, another_mac)


@fixture
def changeHostMacAndRestore(context, host_name, mac_address):
    try:
        print("MAC Address Change !!!!!")
        context.hosts[host_name].shellcmd.set_mac_addr(
            dev=context.host_info[host_name]['nic'], mac=mac_address)
        yield
    finally:
        print("MAC Address Restore !!!!!")
        context.hosts[host_name].shellcmd.set_mac_addr(
            dev=context.host_info[host_name]['nic'],
            mac=context.host_info[host_name]["testbed"]["mac_address"])
