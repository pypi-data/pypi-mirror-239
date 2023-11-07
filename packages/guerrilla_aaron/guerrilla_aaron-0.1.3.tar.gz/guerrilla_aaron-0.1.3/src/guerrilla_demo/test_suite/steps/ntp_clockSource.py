import time
from math import *
from datetime import *

from host import *
from behave import *
from steps.login import *
from steps.common import *
from steps.interface import *

TIME_PATTERN = "%a %b %d %H:%M:%S %Y"
TIME_NOW = None
CLOCK_SOURCE = None
REMOTE_SERVER = None


def set_clock(context, device):
    cfg = context.dut[device].go_config()
    cfg.TimeSync(cfg.get_session()).clock_source(CLOCK_SOURCE, REMOTE_SERVER)
    ret = context.dut[device].main().show_clock()
    assert ret['Clock Source'].lower() == CLOCK_SOURCE.lower(
    ), f'Setting clock source failed!'


def get_time_from_str(context, device):
    # Pattern looks like e.g., Mon Dec 19 11:10:13 2022
    ret = context.dut[device].main().show_clock()
    return datetime.strptime(ret['Current Time'], TIME_PATTERN)


def polling_time_sync(context, device, target_time):
    time_sync_timeout = 180  # in sec
    wait_interval = 5  # in sec
    tolerance = 60  # in sec
    # Algorithm: polling mode
    start = end = time.time()
    while (end - start) < time_sync_timeout:
        time_query = get_time_from_str(context, device)
        time_diff_sec = round(abs((time_query - target_time).total_seconds()))
        if time_diff_sec < tolerance:
            break
        else:
            time.sleep(wait_interval)
            end = time.time()
    else:
        print(
            f"target time: {target_time.strftime(TIME_PATTERN)}, get time: {time_query.strftime(TIME_PATTERN)}, tolerance: {tolerance}"
        )
        raise Exception(f"Time sync failed!")


@given('set ntp server enabled on "{device}"')
def step_impl(context, device):
    cfg = context.dut[device].go_config()
    cfg.TimeSync(cfg.get_session()).ntp_server_toggle(True)
    ret = context.dut[device].main().show_clock()
    assert ret['NTP/SNTP Server'].lower() == "Enabled".lower(
    ), f'Setting NTP/SNTP Server failed!'


@when('set clock source to "{clk_src}" on "{device}"')
def step_impl(context, clk_src, device):
    global CLOCK_SOURCE
    CLOCK_SOURCE = clk_src
    if CLOCK_SOURCE.lower() == 'local':
        set_clock(context, device)


@when('set remote server to "{server}"\'s LAN IP address on "{device}"')
def step_impl(context, server, device):
    global REMOTE_SERVER
    REMOTE_SERVER = context.dut_info[server]['testbed']['lan_ip']
    if CLOCK_SOURCE.lower() != 'local':
        set_clock(context, device)


@when('set current time to "{device}"')
@given('set current time to "{device}"')
def step_impl(context, device):
    global TIME_NOW
    TIME_NOW = datetime.utcnow()
    cfg = context.dut[device].go_config()
    cfg.TimeSync(cfg.get_session()).set_time_manually(TIME_NOW.year, TIME_NOW.month, TIME_NOW.day, \
        TIME_NOW.hour, TIME_NOW.minute, TIME_NOW.second)
    read_back = get_time_from_str(context, device)
    assert round(abs(
        (TIME_NOW -
         read_back).total_seconds())) <= 1, f"set current time failed!"


@then('"{device}" displays current time with accuracy in minute')
def step_impl(context, device):
    polling_time_sync(context, device, TIME_NOW)


@when('set "{num}" days prior to current time on "{device}"')
def step_impl(context, num, device):
    # Prepare time to set
    time_set = TIME_NOW - timedelta(days=int(num))
    # Set time
    cfg = context.dut[device].go_config()
    cfg.TimeSync(cfg.get_session()).set_time_manually(time_set.year, time_set.month, time_set.day, \
        time_set.hour, time_set.minute, time_set.second)


@then('"{device}" displays correct date with "{num}" days prior to current date'
     )
def step_impl(context, device, num):
    target = TIME_NOW - timedelta(days=int(num))
    polling_time_sync(context, device, target)
