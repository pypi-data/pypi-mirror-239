import re
import sys
import time

from guerrilla_aaron.host import *
from behave import *
from guerrilla_aaron.steps import common, interface, login
from guerrilla_aaron.mdc.router.cli.rp_base.ng_router.base import Base
from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000.base import Base as tn5000


@given(
    u'set a dos rule to deny {dos_type} and enable logging flash on "{device}"')
def step_impl(context, dos_type, device):
    # dos icmp-death 1000
    # no dos icmp-death
    # dos syn-flood 1000
    # no dos syn-flood
    # dos arp-flood 1000
    # no dos arp-flood
    dos_type = dos_type.lower().replace(' ', '-')
    context.dut[device].go_config(). \
    command(f'dos {dos_type}'). \
    command(f'logging dos'). \
    command(f'logging dos flash')
    dos_type = dos_type.lower().replace('-', '_').replace('/', '_')
    r = context.dut[device].main().show_dos()
    assert r[0][dos_type].strip(
    ) == "Enable", f'dos setting fail: expect {dos_type}: Enable but {r[0][dos_type]}'


@when(
    u'{enable_disable} dos rule of {dos_type} on "{device}" created by previous step'
)
def step_impl(context, enable_disable, dos_type, device):
    dos_type = dos_type.lower().replace(' ', '-')
    if enable_disable.lower() == 'enable':
        context.dut[device].go_config().command(f'dos {dos_type}')
    else:
        context.dut[device].go_config().command(f'no dos {dos_type}')
    dos_type = dos_type.lower().replace('-', '_').replace('/', '_')
    r = context.dut[device].main().show_dos()
    assert r[0][dos_type].strip() == enable_disable.capitalize(
    ), f'dos setting fail: expect {dos_type}: {enable_disable.capitalize()} but {r[0][dos_type]}'


@given(u'{action} all dos rule on "{device}"')
def step_impl(context, action, device):
    dos_type_list = [
        'Null Scan', 'Xmas Scan', 'Nmap-ID Scan', 'SYN-FIN Scan', 'FIN Scan',
        'SYN-RST Scan', 'Nmap-Xmas Scan', 'New-TCP-without-SYN Scan'
    ]
    if issubclass(context.dut[device]._model, tn5000):
        dos_type_list[3] = 'SYN/FIN Scan'
        dos_type_list[5] = 'SYN/RST Scan'
        dos_type_list[7] = 'New-without-SYN Scan'

    if action == 'enable':
        for i in dos_type_list:
            dos_type = i.lower().replace(' ', '-')
            context.dut[device].go_config().command(f'dos {dos_type}')
    elif action == 'disable':
        for i in dos_type_list:
            dos_type = i.lower().replace(' ', '-')
            context.dut[device].go_config().command(f'no dos {dos_type}')
    else:
        raise ValueError(f'input invalid action: {action}')
