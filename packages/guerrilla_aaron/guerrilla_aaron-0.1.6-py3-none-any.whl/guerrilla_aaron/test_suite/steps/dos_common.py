import re
import sys
import time

from host import *
from behave import *
from steps import common, interface, login
from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000.base import Base as tn5000


@when(u'send traffic with dos_type {dos_type} from "{host1}" to "{host2}"')
def step_impl(context, dos_type, host1, host2):
    command_dict = {
        "Null Scan": ['null'],
        "Xmas Scan": ['fin', 'urg', 'push', 'syn', 'rst', 'ack'],
        "Nmap-ID Scan": ['fin', 'urg', 'push', 'syn'],
        "SYN-FIN Scan": ['fin', 'syn'],
        "FIN Scan": ['fin'],
        "SYN-RST Scan": ['syn', 'rst'],
        "Nmap-Xmas Scan": ['fin', 'urg', 'push'],
        "New-TCP-without-SYN Scan": ['ack'],
        "New-without-SYN Scan": ['ack'],
    }
    context.hosts[host2].tshark.start(interface=context.host_info[host2]['nic'])
    time.sleep(5)
    dos_type = dos_type.replace('/', '-')
    context.hosts[host1].hping3.send( \
        tcpudp_flags=command_dict[dos_type], \
        host = context.host_info[host2]['testbed']['cur_host'], \
        count = 4)
    time.sleep(5)


@then(
    u'check if "{host}" {can_or_cannot} receive traffic with dos_type {dos_type}'
)
def step_impl(context, can_or_cannot, dos_type, host):
    # ['ICMP' , 'Flags [S]', 'UDP']
    flag = { \
        'can': True, \
        'cannot': False}[can_or_cannot]
    command_dict = {
        "Null Scan":
            '<None>',
        "Xmas Scan": (', ').join(['fin', 'syn', 'rst', 'psh', 'ack',
                                  'urg']).upper(),
        "Nmap-ID Scan": (', ').join(['fin', 'syn', 'psh', 'urg']).upper(),
        "SYN-FIN Scan": (', ').join(['fin', 'syn']).upper(),
        "FIN Scan": ('').join(['fin']).upper(),
        "SYN-RST Scan": (', ').join(['syn', 'rst']).upper(),
        "Nmap-Xmas Scan": (', ').join(['fin', 'psh', 'urg']).upper(),
        "New-TCP-without-SYN Scan": ('').join(['ack']).upper(),
        "New-without-SYN Scan": ('').join(['ack']).upper(),
    }
    context.hosts[host].tshark.stop()
    ret = context.hosts[host].tshark.retrieve()
    print(ret)
    dos_type = dos_type.replace('/', '-')
    count = 0
    if ret != None:
        count = ret.count(f'{command_dict[f"{dos_type}"]}')
    if flag:
        assert count >= 1, f'expect receive 4 number of {command_dict[f"{dos_type}"]} but {count}'
    else:
        assert count == 0, f'expect receive 0 number of {command_dict[f"{dos_type}"]} but {count}'


@then(
    u'check traffic with {dos_type} from {incoming_interface} ("{host1}") to {outgoing_interface} ("{host2}") can be blocked and logged by "{device}"'
)
def step_impl(context, dos_type, incoming_interface, outgoing_interface, device,
              host1, host2):
    if issubclass(context.dut[device]._model, tn5000):
        ret = context.dut[device].main().show_logging_event_log_firewall()
    else:
        ret = context.dut[device].main().show_logging_event_log_dos()
    count = 0
    if incoming_interface.upper() == 'BRG' and outgoing_interface.upper(
    ) == 'BRG':
        incoming_interface, outgoing_interface = 'BRG_LAN', 'BRG_LAN'
    log_expect = ['TCP', incoming_interface.upper(), context.host_info[host1]['testbed']['cur_host'], outgoing_interface.upper(), \
           context.host_info[host2]['testbed']['cur_host'], 'DROP']
    log_actual = []
    for r in ret:
        log_actual = [
            r['protocol'], r['in'], r['src_ip'], r['out'], r['dest_ip'],
            r['action']
        ]
        if log_expect == log_actual:
            count += 1
    if dos_type.upper() == 'ICMP':
        assert count == 1, f'logged event-log dismatch: expect 1 but {count}, {log_expect} <-> {log_actual}'
    else:
        assert count == 4, f'logged event-log dismatch: expect 4 but {count}, {log_expect} <-> {log_actual}'
