import time
import json

from host import *
from behave import *
from steps import login, interface, common


@when('"{device}" enable WAN-Ping-Response')
@when('enable WAN-Ping-Response on "{device}"')
@given('enable WAN-Ping-Response on "{device}"')
def step_impl(context, device):
    time.sleep(1)
    context.dut[device].go_config().set_ip_ping_response()


@When('disable {interface} interface from "{device}"')
def step_impl(context, interface, device):
    if interface == "WAN":
        context.dut[device].go_config_if_wan().disable_wan_interface()
    elif interface == "BRG":
        context.dut[device].go_config_bridge().disable_brg_interface()
    else:
        raise ValueError(f'inpurt invalid interface {interface}')


@given('modify {interface} ip address on "{device}"')
@when('modify {interface} ip address on "{device}"')
def step_impl(context, interface, device):
    context.dut_info[device]["testbed"][
        f"{interface.lower()}_ip"] = context.table[0][interface.lower()]
    if interface == "WAN":
        context.dut[device].go_config_if_wan().set_wan_interface( \
            ip=context.table[0][interface.lower()], \
            mask=context.table[0]["mask"])
    elif interface == "LAN":
        context.dut[device].go_config_if_lan().set_lan_interface( \
            ip=context.table[0][interface.lower()], \
            mask=context.table[0]["mask"])
    elif interface == "BRG":
        context.dut[device].go_config_bridge().set_brg_interface( \
            ip=context.table[0][interface.lower()], \
            mask=context.table[0]["mask"])
    else:
        raise ValueError(f'inpurt invalid interface {interface}')


@when('"{host}" create {number} web session to "{device}" {intf}')
def step_impl(context, host, device, number, intf):
    if hasattr(context, 'dut_jwt'):
        # Session Clean Up
        if device in context.dut_jwt:
            for jwt in context.dut_jwt[device]:
                context.hosts[host].dut_ui.web_post(
                    uri="api/v1/auth/logout",
                    jwt=jwt,
                    ip=context.dut_info[device]['session']['host'])
        context.dut_jwt[device] = []
    else:
        context.dut_jwt = {}

    web_jwt = []
    for i in range(1, int(number) + 1):
        web_jwt_one = context.hosts[host].dut_ui.web_get_jwt( \
            username=context.dut_info[device]['credential']['username'], \
            password=context.dut_info[device]['credential']['password'], \
            ip=context.dut_info[device]['testbed'][f'{intf.lower()}_ip'])
        if web_jwt_one is not None:
            web_jwt.append(web_jwt_one)
    assert len(web_jwt) == int(
        number), f'Only {len(web_jwt)} is created but {number} is required.'
    context.dut_jwt[device] = web_jwt


@then('"{host}" retrieve "{device}" {intf} uptime with each web session')
def step_impl(context, host, device, intf):
    for jwt in context.dut_jwt[device]:
        ret = context.hosts[host].dut_ui.web_get(
            uri="api/v1/status/systemInformation",
            jwt=jwt,
            ip=context.dut_info[device]['testbed'][f'{intf.lower()}_ip'])
        assert ret != None, f'Fail to retrieve {device} uptime with jwt {jwt}'
        print(f"-----> uptime: {json.loads(ret[0])['uptime']}")


@when('set maximum web session to {number} on "{device}"')
def step_impl(context, number, device):
    context.dut[device].go_config().set_ip_http_max_login_users(number)


@then('"{host}" fail to create {session_seq} web session to "{device}" {intf}')
def step_impl(context, host, device, session_seq, intf):
    session_index = int(session_seq[:-2])
    assert session_index - 1 == len(
        context.dut_jwt[device]
    ), f'assume there are {session_index-1} web sessions but {len(context.dut_jwt[device])}'

    web_jwt_one = context.hosts[host].dut_ui.web_get_jwt( \
        username=context.dut_info[device]['credential']['username'], \
        password=context.dut_info[device]['credential']['password'], \
        ip=context.dut_info[device]['testbed'][f'{intf.lower()}_ip'])
    assert web_jwt_one == None, f'{session_seq} web session should fail but success'
