import os
import time

from host import *
from behave import *


@when('"{host_send}" send {count} ICMP response to "{host_recv}" through "{device}"')
def step_impl(context, host_send, count, host_recv, device):
    os.system('sshpass -p "{0}" scp {1} {2}@{3}:~/'.format(context.host_info[host_send]['session']['credential']['password'],
                                                            "../lib/replay_pkts/icmp_reply.pcapng",
                                                            context.host_info[host_send]['session']['credential']['username'],
                                                            context.host_info[host_send]['session']['host']))
    dut_mac = context.dut[device].main().show_system()[0].pop("mac_address")
    context.hosts[host_send].tcp_tool.rewrite(infile="icmp_reply.pcapng", outfile="icmp_reply.pcap",
                                                sip=context.host_info[host_send]["testbed"]["cur_host"],
                                                dip=context.host_info[host_recv]["testbed"]["cur_host"], 
                                                smac=context.host_info[host_send]["testbed"]["mac_address"],
                                                dmac=dut_mac)
    context.hosts[host_send].tcp_tool.send(sendfile="icmp_reply.pcap", number=count)
    time.sleep(5)


@then('"{host_recv}" shall receive {count} ICMP reponse from "{host_send}"')
def step_impl(context, host_recv, count, host_send):
    context.hosts[host_recv].tshark.stop()

    ret = context.hosts[host_recv].tshark.retrieve()

    if len(ret) == 0:
        raise ValueError('packet receiving fails')

    ret_lines = ret.split('\n')

    destip_count = {}
    # parse and get dest IP counts
    for a in ret_lines:
        # skip if not ICMP
        if a.find("ICMP") == -1:
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


@when('malformed packets is "{action}" on "{device}"')
def step_impl(context, action, device):
    context.dut[device].go_config().set_malformed_packet_status(status=action)


@when('malformed packets logging is "{action}" on "{device}"')
def step_impl(context, action, device):
    context.dut[device].go_config().set_malformed_packet_log(status=action, dst={"flash"})


@then('malformed event log shall not be recorded on "{device}"')
def step_impl(context, device):
    r = context.dut[device].main().show_logging_event_log_malformed()
    # print(r)
    assert len(r) == 0, f'expect no record but {len(r)} log was/were recorded'


@then('{count} malformed event log shall be recorded on "{device}"')
def step_impl(context, count, device):
    r = context.dut[device].main().show_logging_event_log_malformed()
    assert len(r) == int(count), f'expect {count} record but {len(r)} log was/were recorded'