import sys
import time

from host import *
from behave import *
from steps.common import *
from steps.interface import *
from steps.login import *


@given('"{device}" enables login lockout toggle')
def step_impl(context, device):
    cfg = context.dut[device].go_config()
    cfg.LoginLockout(cfg.get_session()).lockout_toggle(True)


@given('"{device}" sets "Login Failure Retry Threshold" to "{num}" times')
def step_impl(context, device, num):
    cfg = context.dut[device].go_config()
    cfg.LoginLockout(cfg.get_session()).lockout_retryThreshold(num)


@given('"{device}" sets "Lockout Duration" to "{num}" minute')
def step_impl(context, device, num):
    cfg = context.dut[device].go_config()
    cfg.LoginLockout(cfg.get_session()).lockout_lockoutTime(num)


@given('"{device}" logins with incorrect password for "{num}" times')
@when('"{device}" logins with incorrect password for "{num}" times')
def step_impl(context, device, num):
    # This is a trick, to avoid iptables PortScan chain dropping our packets.
    # PortScan will drop our packet if 3 attempts within 30 seconds request for TCP connection.
    context.dut[device].main().clear_ssh_telnet_limit()
    if (int(num) > 3):
        raise Exception(
            "Design limitation. Unable to initiate connection attempts more than 3 times within 30 seconds."
        )
    # print('logoutFromDUT 1') #debug
    logoutFromDUT(context, device)
    # print('logoutFromDUT 2') #debug
    for _ in range(int(num)):
        user = 'admin'
        password = 'wrong_pwd'
        context.execute_steps(
            f'''then unable to login "{device}" as {user} with password {password}'''
        )
    context.dut[device].timer = time.time()


@when(
    '"{device}" logins with correct password for one more time after "{num}" seconds'
)
def step_impl(context, device, num):
    s_time = context.dut[device].timer
    print(f"start time = {s_time}")
    print(f"current time = {time.time()}")
    r = int(num) - (time.time() - s_time) + 1  # +1 for get ceil
    print(f"residual time = {r} sec")
    if r > 0:
        time.sleep(r)
    try:
        context.dut[device].main().exit()
    except:
        pass
    try:
        context.dut[device].close()
    except:
        pass
    try:
        context.dut_info[device]['credential']['username'], context.dut_info[device]['credential']['password'] = 'admin', 'moxa'
        loginToDUT(context, device)  # may succeed or fail
    except:
        pass
    finally:
        # restore s_time back to router object
        context.dut[device].timer = s_time


@then('"{device}" is {capable} to login with correct password')
def step_impl(context, device, capable):
    if capable == "unable":
        try:
            context.dut[device].main().show_system(
            )  # suppose to be caught by exception
        except:
            print("OK! Suppose to except!")
        else:
            raise Exception(
                f"The device {device} is supposed to be unable to login")
    elif capable == "able":
        try:
            context.dut[device].main().show_system()  # suppose to work
        except:
            raise Exception(
                f"The device {device} is supposed to be able to login")
    else:
        raise Exception(f"Unsupported flag: {capable}")


@then('"{device}" can see system log "{log_key_word}" for "{num}" times')
def step_impl(context, device, log_key_word, num):
    logs = context.dut[device].main().show_logging_event_log_system()
    count = 0
    for log in logs:
        if log_key_word in log['event']:
            count += 1
    assert count == int(num), f'number of logs not matched {num} times'
