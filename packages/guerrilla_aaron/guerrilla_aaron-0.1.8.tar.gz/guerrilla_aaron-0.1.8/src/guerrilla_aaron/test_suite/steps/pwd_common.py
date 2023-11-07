
from guerrilla_aaron.host import *
from behave import *
from guerrilla_aaron.steps import common, interface, login


@when('set password mininum length as {length} on "{device}"')
def step_impl(context, length, device):
    context.dut[device].go_config().set_password_policy(min_len=length)


@when('{action} password "{policy}" policy on "{device}"')
def step_impl(context, action, policy, device):
    global_complexity_check = item = None
    if policy == "complexity strength check":
        global_complexity_check = True
    elif policy == "must contain at least one digit":
        item = "digit"
    elif policy == "must include both upper and lower case letter":
        item = "alphabet"
    elif policy == "must contain at least one special character":
        item = "special-characters"

    context.dut[device].go_config().set_password_policy(
        action=action,
        global_complexity_check=global_complexity_check,
        complexity_item=item)
