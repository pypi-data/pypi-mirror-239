import sys

# from host import *
from behave import *
from host import HostFactory
from steps import login, interface, common


@when('login "{device}" via {username}')
def step_impl(context, device, username):
    context.dut_info[device]['credential']['username'] = username
    try:
        context.dut[device] = HostFactory.create_mdc_rp(
            context.dut_info[device], 
            debug_output=sys.stdout)
    except Exception as e:
        context.dut[device] = None


@then('"{device}" can be login successfully')
def step_impl(context, device):
    assert context.dut[device] != None, f'login failed!'


@then('check account privilege {action1} show system information on "{device}"')
def step_impl(context, action1, device):
    res = context.dut[device].main().show_system()
    if 'can' == action1:
        assert len(res) != 0, f'system information can not be shown!'
    elif 'can not' == action1:
        assert len(res) == 0, f'system information can be shown!'


@then('check account privilege {action2} enter configure level on "{device}"')
def step_impl(context, action2, device):
    try:
        res = context.dut[device].go_config()
    except Exception as e:
        res = None

    if 'can' == action2:
        assert res != None, f'configure level can not be entered!'
    elif 'can not' == action2:
        assert res == None, f'configure level can be entered!'


@then('check account privilege {action3} add a new user on "{device}"')
def step_impl(context, action3, device):
    try:
        res = context.dut[device].go_config().set_login_account(
            action="create",
            username="test",
            password="test",
            privilege="system admin")
    except Exception as e:
        res = None

    if 'can' == action3:
        assert res != None, f'new user can not be created!'
    elif 'can not' == action3:
        assert res == None, f'new user can be created!'
