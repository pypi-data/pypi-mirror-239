import time

from guerrilla_aaron.host import *
from behave import *


@given('add a static route with unknown destination ip for "{host}"')
def step_impl(context, host):
    context.hosts[host].shellcmd.add_route(
        dip=f'{context.table[0]["st_route_dip"]}',
        gw=f'{context.table[0]["st_route_next_hop"]}',
        dev=context.host_info[host]["nic"],
        mask='32')


@when('set "{device}" a static route rule with parameters and status {status}')
@given('set "{device}" a static route rule with parameters and status {status}')
def step_impl(context, device, status):
    context.dut[device].go_config().command(
        f'ip route static TCR-664 {context.table[0]["destination_ip"]} {context.table[0]["mask"]} {context.table[0]["next_hop"]} {context.table[0]["metric"]}'
    )
    context.dut[device].go_config().command(
        f'ip route static TCR-664 {status.lower()}')


@when('send test packet with the destination ip form "{host1}" to "{host2}"')
def step_impl(context, host1, host2):
    context.hosts[host2].tshark.start(interface=context.host_info[host2]['nic'])
    context.hosts[host1].shellcmd._ssh.command(
        f'ping {context.table[0]["dip"]} -c 4')
    time.sleep(10)


@then('check if "{host1}" {action} receive test packet from "{host2}"')
def step_impl(context, action, host1, host2):
    context.hosts[host1].tshark.stop()
    rcv_pkt = context.hosts[host1].tshark.retrieve()
    hit = 0
    hit = rcv_pkt.count(
        f"{context.host_info[host2]['testbed']['cur_host']} → 192.168.129.30 ICMP"
    )
    print(f"[RSV PKT {hit}:]" + rcv_pkt)
    if "can" == action:
        assert hit != 0, f'test packets are not received! rcv_pkt: {rcv_pkt}'
    elif "can not" == action:
        assert hit == 0, f'{hit} test packets are received! rcv_pkt: {rcv_pkt}'
