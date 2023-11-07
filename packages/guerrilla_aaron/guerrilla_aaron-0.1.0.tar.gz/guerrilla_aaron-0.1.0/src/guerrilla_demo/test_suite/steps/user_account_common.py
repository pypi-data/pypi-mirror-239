
from host import *
from behave import *
from steps import common, interface, login


@given('clear ssh and telnet limit on "{device}"')
def step_impl(context, device):
    '''
    This step may require modification for future usage.
    Due to the DUT's limit on the number of SSH and Telnet sessions, 
    we need to clear the limitation before logging in and out multiple times.
    '''
    context.dut[device].main().clear_ssh_telnet_limit()
    context.execute_steps(f'''given logout "{device}"''')
    context.execute_steps(f'''given login "{device}" as Admin''')


@then('no {user} on "{device}" User Accounts')
def step_impl(context, device, user):
    ret = context.dut[device].main().show_user_accounts()
    for i in ret:
        if user == i['Name']:
            assert False, f'{user} should not be on User Accounts list'
