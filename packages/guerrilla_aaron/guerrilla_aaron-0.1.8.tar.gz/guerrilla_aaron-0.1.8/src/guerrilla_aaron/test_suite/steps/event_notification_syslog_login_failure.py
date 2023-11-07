from behave import *

from guerrilla_aaron.steps import common, interface, login


@when(
    'use "username" with "incorrect password" to login for the "ordinal" time on "{device}"'
)
def step_impl(context, device):
    login.logoutFromDUT(context, device)
    for row in context.table:
        user = row['username']
        password = row['incorrect password']
        context.execute_steps(
            f'''then unable to login "{device}" as {user} with password {password}'''
        )
    context.dut_info[device]['credential']['username'], context.dut_info[device]['credential']['password'] = 'admin', 'moxa'
    context.dut[device].close()
    login.loginToDUT(context, device) 
