from host import *
from behave import *
from steps import login, interface, common

@when('"{host}" send UDP traffic to destination ip and port')
def step_impl(context, host):
    print(
        f'send traffic: {context.host_info[host]["testbed"]["cur_host"]} {context.table[0]["nat_dest_ip"]}:{context.table[0]["nat_dest_port"]}'
    )
    context.hosts[host].hping3.send( \
        tcpudp_flags=['udp'], \
        host = context.table[0]['nat_dest_ip'], \
        count = 4, \
        port = context.table[0]['nat_dest_port'])
    time.sleep(5)


@then('check "{host}" receive udp traffic with destination IP and port')
def step_impl(context, host):
    context.hosts[host].tshark.stop()

    ret = context.hosts[host].tshark.retrieve()

    ret_lines = ret.split('\n')

    count = 0
    # parse and get dest IP counts
    for a in ret_lines:
        # skip if not UDP
        if a.find("UDP") == -1:
            continue

        arr = a.lstrip(' ').split(' ')

        # skip unexpected format
        if arr[3] != '→' and arr[8] != '→':
            raise ValueError(f'unexpected tshark format {a}')

        if arr[4] == context.table[0]['real_dest_ip'] and arr[9] == context.table[0]['real_dest_port']:
            count += 1

    assert count >= 1 , \
        f'expect receive 4 number of udp but {count}, {ret}'