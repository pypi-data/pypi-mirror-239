import time

from host import *
from behave import *
from steps import login, interface, common
from guerrilla_aaron.mdc.router.cli.rp_base.ng_router.base import Base
from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000.base import Base as tn5000


@then(
    u'check if "{host}" {can_or_cannot} receive traffic with "{device}"s {interface} ip and {specific_protocols}'
)
def step_impl(context, host, can_or_cannot, specific_protocols, device,
              interface):
    # ['ICMP' , 'Flags [S]', 'UDP']
    flag = { \
        'can': True, \
        'cannot': False}[can_or_cannot]
    context.hosts[host].tshark.stop()
    ret = context.hosts[host].tshark.retrieve()
    print(ret)
    count = 0
    if ret != None:
        print(
            f'{context.dut_info[device]["testbed"][f"{interface.lower()}_ip"]} → {context.host_info[host]["testbed"]["cur_host"]} {specific_protocols.upper()}'
        )
        count = ret.count(
            f'{context.dut_info[device]["testbed"][f"{interface.lower()}_ip"]} → {context.host_info[host]["testbed"]["cur_host"]} {specific_protocols.upper()}'
        )
    if flag:
        assert count >= 1, f'expect receive 4 number of {specific_protocols.upper()} but {count}'
    else:
        assert count == 0, f'expect receive 0 number of {specific_protocols.upper()} but {count}'


@given('"{device}" insert {mode} nat rules')
@given('set {mode} nat rule on "{device}"')
def step_impl(context, device, mode):
    for rule in context.table:
        index_arr = rule['nat_indexes'].split("-")
        index_start = int(index_arr[0])
        index_end = (int(index_arr[0]) +
                     1) if len(index_arr) == 1 else (int(index_arr[1]) + 1)
    if issubclass(context.dut[device]._model, tn5000):
        if mode == '1-1':
            context.dut[device].go_config_nat().set_one2one_rule(ipaddr_in=rule['real_dest_ip'], \
                                                                 ipaddr_out=rule['nat_dest_ip'], \
                                                                 if_out=rule['nat_iface'])
        elif mode == 'N-1':
            context.dut[device].go_config_nat().set_dynamic_rule(ipaddr_start=rule['source_ip_start'], \
                                                                 ipaddr_end=rule['source_ip_end'], \
                                                                    if_out=rule['outgoing_interface'])
        elif mode == 'PAT':
            context.dut[device].go_config_nat().set_port_forward_rule(ipaddr_in=rule['real_dest_ip'], \
                                                                      port_in=rule['real_dest_port'], \
                                                                      if_out=rule['nat_iface'], \
                                                                      port_out=rule['nat_dest_port'], \
                                                                      protocol=rule['protocol'].lower())
        else:
            raise ValueError('input invalid mode of NAT')
    elif issubclass(context.dut[device]._model, Base):
        for rule in context.table:
            index_arr = rule['nat_indexes'].split("-")
            index_start = int(index_arr[0])
            index_end = (int(index_arr[0]) +
                        1) if len(index_arr) == 1 else (int(index_arr[1]) + 1)
            if mode == '1-1':
                for idx in range(index_start, index_end):
                    context.dut[device].go_config_nat(idx).\
                        mode(mode).\
                        original(
                            in_iface=rule["nat_iface"],
                            osi="any",
                            osp="any",
                            odi=rule["nat_dest_ip"],
                            odp="any").\
                        translated(
                            out_iface="any",
                            tsi="any",
                            tsp="any",
                            tdi=rule["real_dest_ip"],
                            tdp="any"
                        ).\
                        exit()
            elif mode == 'N-1':
                for idx in range(index_start, index_end):
                    context.dut[device].go_config_nat(idx).\
                        mode("n-1").\
                        original(
                            in_iface="any",
                            osi=f'{rule["source_ip_start"]}-{rule["source_ip_end"]}',
                            osp="any",
                            odi="any",
                            odp="any").\
                        translated(
                            out_iface=rule["outgoing_interface"],
                            tsi="any",
                            tsp="any",
                            tdi="any",
                            tdp="any"
                        ).\
                        exit()
            elif mode == 'PAT':
                for idx in range(index_start, index_end):
                    context.dut[device].go_config_nat(1).\
                        mode("pat").\
                        original(
                            in_iface=rule['nat_iface'],
                            osi="any",
                            osp="any",
                            odi="any",
                            odp=rule['nat_dest_port']).\
                        translated(
                            out_iface="any",
                            tsi="any",
                            tsp="any",
                            tdi=rule["real_dest_ip"],
                            tdp=rule['real_dest_port']
                        ).\
                        protocol(rule["protocol"].lower()).\
                        exit()
        

        # Wait 5 secs for rule to activate.
        time.sleep(5)


@when('"{host}" send some icmp echo request packets for each destination IP')
def step_impl(context, host):
    context.hosts[host].shellcmd.restart_network(context.host_info[host]["nic"])
    for item in context.table:
        context.hosts[host].hping3.send( \
            tcpudp_flags=['icmp'], \
            host = item['nat_dest_ip'], \
            count = item['pkt_num'],
            interval = "100000")
        time.sleep(2)


@then(
    'check "{host}" receive some icmp echo request packets with destination IP')
def step_impl(context, host):
    context.hosts[host].tshark.stop()

    ret = context.hosts[host].tshark.retrieve()

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
    for item in context.table:
        assert item[
            'real_dest_ip'] in destip_count, f'{item[f"real_dest_ip"]} expect to receive {item[f"pkt_num"]} packets but receive 0'

        assert int(destip_count[item['real_dest_ip']]) == int(
            item['pkt_num']
        ), f'{item[f"real_dest_ip"]} expect to receive {item["pkt_num"]} packets but receive {destip_count[item["real_dest_ip"]]}'
