import time
import re
from behave import *
import os


@when('{action} LLDP on "{device}"')
def step_impl(context, action, device):
    """
    action: enable/disable
    """
    context.dut[device].go_config().set_lldp_status(action=action)


@when('set transmission freqency of LLDP updates to {trans_freq} sec on "{device}"')
def step_impl(context, trans_freq, device):
    context.dut[device].go_config().set_lldp_transmission_freq(trans_freq)
    context.lldp_ttl = int(trans_freq)
    context.dut[device].main().save()


@when('starts tshark sniffer on "{host}" for LLDP packet')
def step_impl(context, host):
    context.hosts[host].tshark.start(interface=context.host_info[host]['nic'],
                                     display_filter="lldp",
                                     capture_number=1,
                                     verbose=True)


@then('"{host}" {result} receive LLDP packet from "{device}" within {wait_time} sec')
def step_impl(context, host, result, device, wait_time):
    time.sleep(int(wait_time))
    context.hosts[host].tshark.stop()
    ret = context.hosts[host].tshark.retrieve()
    # print("ret1: ", ret, "end")
    ret = context.hosts[host].tshark.retrieve()
    # print("ret2: ", ret, "end")

    check_packets_captured_pattern = r"Frame \d+:"
    chassis_pattern = r"Chassis Subtype = MAC address, Id: (\S+)"
    port_pattern = r"Port Subtype = Interface name, Id: (\d+)"
    ttl_pattern = r"Time To Live = (\d+) sec"

    if result == "shall not":
        assert bool(re.search(check_packets_captured_pattern, ret)) == False, 'lldp packet captured'

    elif result == "shall":
        assert bool(re.search(check_packets_captured_pattern, ret)), 'no lldp packet captured'

        chassis_match = re.search(chassis_pattern, ret)
        if chassis_match:
            print(chassis_match.group(1))
            assert chassis_match.group(1).lower() == context.dut_info[device]["mac_address"].lower(), \
                f'the lldp packet chassis id: {chassis_match.group(1)} is not the same as the DUT mac address: {context.dut_info[device]["mac_address"]}'

        port_match = re.search(port_pattern, ret)
        if port_match:
            assert port_match.group(1) == context.host_info[host]["testbed"]["port"], \
                f'the lldp packet port id: {port_match.group(1)} is not the same as the host port: {context.host_info[host]["testbed"]["port"]}'

        ttl_match = re.search(ttl_pattern, ret)
        if ttl_match:
            assert int(ttl_match.group(1)) == context.lldp_ttl*4, \
                f'the lldp packet Time To Live: {ttl_match.group(1)} is not the same as the (DUT transmission interval)*4: {context.lldp_ttl}'


@when('"{host}" send {count} LLDP packet with extentions and following values')
def step_impl(context, host, count):
    os.system('sshpass -p "{0}" scp {1} {2}@{3}:~/'.format(context.host_info[host]['session']['credential']['password'],
                                                            "../lib/replay_pkts/lldp_with_extention.pcapng",
                                                            context.host_info[host]['session']['credential']['username'],
                                                            context.host_info[host]['session']['host']))

    context.hosts[host].tcp_tool.rewrite(infile="lldp_with_extention.pcapng", outfile="lldp_out.pcap")
    context.hosts[host].tcp_tool.send(sendfile="lldp_out.pcap", number=count)
    time.sleep(5)
    context.lldp_dut_port = context.host_info[host]["testbed"]["port"]
    context.lldp_neighbor_id = context.table[0]['Chasis_id']
    context.lldp_neighbor_port = context.table[0]['Port_id']


@then('the LLDP table on "{device}" should contain an entry with corresponding port, neighbor id, and neighbor port')
def step_impl(context, device):
    ret = context.dut[device].main().show_lldp_table()
    print(ret)
    found_item = None
    for item in ret:
        if item["port"] == context.lldp_dut_port and \
            item["neighbor_id"] == context.lldp_neighbor_id and \
            item["neighbor_port"] == context.lldp_neighbor_port:
            found_item = item
            break

    if found_item:
        print("Found the packet")
    else:
        assert False, f"Packet not found. The table is as following: {ret}"