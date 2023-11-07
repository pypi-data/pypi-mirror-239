import time

from host import *
from behave import *
from steps import common, interface, login


@then('show vlan including vlan id of "{intf}" on "{device}"')
def step_impl(context, intf, device):
    time.sleep(1)
    r = context.dut[device].main().show_vlan()
    print("-------------------------------------------")
    print(r)
    print("-------------------------------------------")
    if context.dut_info[device]['testbed'][f'{intf.lower()}_vlan'] == r[1][
            'vid']:
        print(
            f'VLAN {context.dut_info[device]["testbed"][f"{intf.lower()}_vlan"]} exist'
        )
        result = 'pass'
    else:
        result = 'fail'
    assert result == 'pass', f'VLAN {context.dut_info[device]["testbed"][f"{intf.lower()}_vlan"]} not exist'
