import re
import sys
import time

from host import *
from behave import *
from steps import common, interface, login


@when('"{device}" {dosType} Dos Defense turns {flag}')
def step_impl(context, flag, dosType, device):
    switch = {'on': True, 'off': False}[flag.lower()]

    if switch:
        context.dut[device].go_config().command(f'dos {dosType.lower()}-scan')
    else:
        context.dut[device].go_config().command(
            f'no dos {dosType.lower()}-scan')

    dos_status = context.dut[device].main().show_dos()
    expect = {'on': 'Enable', 'off': 'Disable'}[flag.lower()]
    assert expect == dos_status[0]['syn_rst_scan'].strip(), \
           f'show_dos syn/rst-scan is not {expect}: {dos_status[0]["syn_rst_scan"]}'


@when('"{device}" Dos Defense {logType} log turns {flag}')
def step_impl(context, flag, logType, device):
    switch = {'on': True, 'off': False}[flag.lower()]
    if flag:
        context.dut[device].go_config().command(f'logging dos')
        context.dut[device].go_config().command(f'logging dos {logType}')
    else:
        context.dut[device].go_config().command(f'no logging dos {logType}')

    dos_status = context.dut[device].main().show_dos()
    expect = {'on': 'Enable', 'off': 'Disable'}[flag.lower()]

    assert expect == dos_status[0]['flash'].strip(), \
           f'show_dos Flash is not {expect}: {dos_status[0]["flash"]}'


@when('"{host}" starts tshark to sniffer')
def step_impl(context, host):
    context.hosts[host].tshark.start()


@when('"{host}" waits {second} seconds then stops tshark snifferring')
def step_impl(context, second, host):
    time.sleep(int(second))
    context.hosts[host].tshark.stop()


@when(
    '"{host1}" sends {pack_num} TCP packets in flag of SYN and RST to "{host2}"\'s port {port}'
)
def step_impl(context, pack_num, port, host1, host2):
    # sudo hping3 192.168.127.254 -R -S --faster -p 80 -c 1000
    dst = context.host_info[host2]['testbed']['cur_host']
    context.hosts[host1].hping3.send(host=dst,
                                     port=port,
                                     tcpudp_flags=['syn', 'rst'],
                                     count=pack_num)


@then('"{host1}" received {pack_num} packets from "{host2}"')
def step_impl(context, pack_num, host1, host2):
    result = context.hosts[host1].tshark.retrieve()
    # print(result)
    expect = int(pack_num) * 0.9
    pattern = f"{context.host_info[host2]['testbed']['cur_host']} → " \
              f"{context.host_info[host1]['testbed']['cur_host']}"
    count = result.count(pattern)
    print("%" * 20, f'verify syn-rst Tshark count: {count}', "%" * 20)
    if expect == 0:
        assert count == expect, f'expect {expect} but get {count}'
    else:
        assert count >= expect, f'expect {expect} but get {count}'


@then(
    '"{device}" logging {detect} attack events from "{host1}" to "{host2}" in the period of testing'
)
def step_impl(context, detect, device, host1, host2):
    verifier = {'some': lambda c: c > 1, 'no': lambda c: c == 0}[detect.lower()]

    count = 0
    logs = context.dut[device].main().show_logging_event_log_dos()
    expect_log = (context.host_info[host1]['testbed']['cur_host'], \
        context.host_info[host2]['testbed']['cur_host'], \
            'TCP', \
            'DROP')
    for log in logs:
        # print(log['src_ip'], log['dest_ip'], log['protocol'], log['action'])
        if (log['src_ip'], log['dest_ip'], log['protocol'],
                log['action']) == expect_log:
            count += 1
    print("%" * 20, f'verify Event Log count: {count}', "%" * 20)
    assert verifier(count), f'expect {detect} but get {count}'
