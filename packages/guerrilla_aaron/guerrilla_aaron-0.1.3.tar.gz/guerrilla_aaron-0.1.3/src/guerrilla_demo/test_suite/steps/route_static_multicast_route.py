import os
import time

from behave import *

@given('enable static multicast route on "{device}"')
def step_impl(context, device):
    cfg = context.dut[device].go_config()
    cfg.MulticastRoute(cfg.get_session()).set_global_multicast_route(mode="static")


@given('set a static multicast route rule on "{device}"')
def step_impl(context, device):
    cfg = context.dut[device].go_config()
    cfg.MulticastRoute(cfg.get_session()).set_static_multicast_route_rule(action="add",
                                                                       group_addr=context.table[0]["dst_ip"],
                                                                       src_addr=context.table[0]["src_ip"],
                                                                       in_itf=context.table[0]["in_iface"],
                                                                       out_itf=context.table[0]["out_iface"])
    context.dut[device].main().save()


@when('"{host_send}" send {count} multicast packet with destination ip "{dst_ip}"')
def step_impl(context, host_send, count, dst_ip):
    os.system('sshpass -p "{0}" scp {1} {2}@{3}:~/'.format(context.host_info[host_send]['session']['credential']['password'],
                                                            "../lib/replay_pkts/multicast.pcap",
                                                            context.host_info[host_send]['session']['credential']['username'],
                                                            context.host_info[host_send]['session']['host']))

    context.hosts[host_send].tcp_tool.rewrite(infile="multicast.pcap", outfile="multicast_out.pcap",
                                                sip=context.host_info[host_send]["testbed"]["cur_host"], 
                                                dip=dst_ip, 
                                                smac=context.host_info[host_send]["testbed"]["mac_address"])
    context.hosts[host_send].tcp_tool.send(sendfile="multicast_out.pcap", number=count)
    context.multicast_group_addr = dst_ip
    time.sleep(10)


@then('"{host_recv}" {action} receive multicast packets from "{host_send}"')
def step_impl(context, host_recv, action, host_send):
    '''
    action can be 'shall' or 'shall not'
    '''
    context.hosts[host_recv].tshark.stop()

    ret = context.hosts[host_recv].tshark.retrieve()
    print('receive packets: ', ret)

    if len(ret) == 0:
        raise ValueError('packet receiving fails')

    ret_lines = ret.split('\n')

    destip_count = {}
    # parse and get dest IP counts
    for a in ret_lines:
        # skip if not UDP
        if a.find("UDP") == -1:
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
    host_recv_ip = context.multicast_group_addr

    if host_recv_ip not in destip_count:
        recv_packet_count = 0
    else:
        recv_packet_count = destip_count[host_recv_ip]

    if action == "shall":
        assert int(recv_packet_count) > 0, f'{host_recv} expect to receive packets but receive {recv_packet_count}'
    elif action == "shall not":
        assert int(recv_packet_count) == 0, f'{host_recv} expect to not receive packets but receive {recv_packet_count}'