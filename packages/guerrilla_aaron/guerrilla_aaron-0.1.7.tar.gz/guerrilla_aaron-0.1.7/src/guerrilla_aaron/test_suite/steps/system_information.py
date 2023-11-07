import re

from guerrilla_aaron.host import *
from behave import *
from guerrilla_aaron.steps import common, interface, login


@then('default system information of "{device}" is consistent with the spec')
def step_impl(context, device):
    sys_name = context.dut_info[device]['sys_name']
    sys_location = context.dut_info[device]['sys_location']
    sys_description = context.dut_info[device]['sys_description']

    ret = context.dut[device].main().show_system()
    cur_sys_name = re.findall(r'\D+', ret[0]['system_name'])[0].strip()

    assert cur_sys_name in sys_name, f'system name: {cur_sys_name} is not consistent with spec: {sys_name}'
    assert ret[0][
        'system_location'] in sys_location, f'sys location: {ret[0]["system_location"]} is not consistent with spec :{sys_location}'
    assert ret[0][
        'system_description'] in sys_description, f'sys description: {ret[0]["system_description"]} is not consistent with spec: {sys_description}'


@when('modify system information on "{device}"')
def step_impl(context, device):
    sys_name = context.table[0]['sys_name']
    sys_location = context.table[0]['sys_location']
    sys_description = context.table[0]['sys_description']
    context.dut[device].go_config().set_hostname(sys_name)
    context.dut[device].go_config().command(
        f'snmp-server location {sys_location}')
    context.dut[device].go_config().command(
        f'snmp-server description {sys_description}')


@then(
    'system information of "{device}" is consistent with the modified system information'
)
def step_impl(context, device):
    sys_name = context.table[0]['sys_name']
    sys_location = context.table[0]['sys_location']
    sys_description = context.table[0]['sys_description']

    ret = context.dut[device].main().show_system()

    assert ret[0][
        'system_name'] == sys_name, f'system name is not consistent with modified system information: {ret[0]["system_name"]}'
    assert ret[0][
        'system_location'] == sys_location, f'sys location is not consistent with modified system information :{ret[0]["system_location"]}'
    assert ret[0][
        'system_description'] == sys_description, f'sys description is not consistent with modified system information: {ret[0]["system_description"]}'
