import sys

from behave import *
from guerrilla_aaron.host import HostFactory


def loginToDUT(context, device):
    context.dut[device] = HostFactory.create_mdc_rp(
            context.dut_info[device], 
            debug_output=sys.stdout)
    return True


def logoutFromDUT(context, device):
    print(f"context.dut[{device}].disconnect()!!!!!")
    try:
        print(f"\n ---- dut log out start !!! ----")
        print(f"\n ---- dut back to main !!! ----")
        context.dut[device].main().exit()
        print(f"\n ---- dut close session !!! ----")
        context.dut[device].close()
        print(f"\n ---- dut log out finish!!! ----")
    except ValueError as e:
        print(f'\n ---- {e} ----')
        print(f'\n ---- dut is not alive ----')


@fixture
def loginToDUTWithFixture(context, device):
    try:
        # -- SETUP-FIXTURE
        loginToDUT(context, device)
        yield
    finally:
        # -- CLEANUP-FIXTURE
        logoutFromDUT(context, device)


@given('authorize CLI of "{device}"')
def step_impl(context, device):
    use_fixture(loginToDUTWithFixture, context, device)

@given('login "{device}" with ip "{ip}"')
def step_impl(context, device, ip):
    context.dut_info[device]['session']['host'] = ip
    loginToDUT(context, device)

@given('login "{device}" as Admin')
def step_impl(context, device):
    context.dut_info[device]['credential']['username'], context.dut_info[device]['credential']['password'] = 'admin', 'moxa'
    loginToDUT(context, device)


@given('logout "{device}"')
@when('logout "{device}"')
def step_impl(context, device):
    try:
        context.dut[device].main()._s.command('exit')
        context.dut[device].close()
    except ValueError as e:
        print(f'\n ---- {e} ----')


@then('login "{device}" as {user} with password {password} successfully')
def step_impl(context, device, user, password):
    context.dut_info[device]['credential']['username'], context.dut_info[device]['credential']['password'] = user, password

    try:
        context.dut[device] = HostFactory.create_mdc_rp(
            context.dut_info[device], 
            debug_output=sys.stdout)
    except ValueError as e:
        print(f'\n ---- {e} ----')
        assert False, f"The {user} should be able to login {device}"


@then('unable to login "{device}" as {user} with password {password}')
def step_impl(context, device, user, password):
    context.dut_info[device]['credential']['username'], context.dut_info[device]['credential']['password'] = user, password

    try:
        context.dut[device] = HostFactory.create_mdc_rp(
            context.dut_info[device], 
            debug_output=sys.stdout)
    except:
        print("OK! Suppose to catch exception!")
    else:
        assert False, f"The {user} should not be able to login {device}"
