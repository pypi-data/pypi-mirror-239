import time
from datetime import datetime, timedelta

from behave import *

@given('set summer time to start at "{start_time}" on "{device}"')
def step_impl(context, start_time, device):
	context.dut[device].go_config().set_clock_summer_time(start_date=start_time)


@given('set summer time to end at "{end_time}" on "{device}"')
def step_impl(context, end_time, device):
	context.dut[device].go_config().set_clock_summer_time(end_date=end_time)


@given('set summer time offset as "{offset}" hour on "{device}"')
def step_impl(context, offset, device):
	context.dut[device].go_config().set_clock_summer_time(offset=offset)


@when('set the current time on "{device}" {min} minute behind "{real_start_time}"')
def step_impl(context, device, min, real_start_time):

    # Parse the original date string
    original_time = datetime.strptime(real_start_time, "%a %B %d %H:%M:%S %Y")
    # Format the date as "02:00:00 3 12 2023"
    # formatted_date = original_time.strftime("%H:%M:%S %m %d %Y")
    
    new_time = original_time - timedelta(minutes=1)
    cfg = context.dut[device].go_config()
    cfg.TimeSync(cfg.get_session()).set_time_manually(new_time.year, new_time.month, new_time.day, \
        new_time.hour, new_time.minute, new_time.second)


@when('wait {min} minute until the current time on "{device}" reaches "{start_time}"')
def step_impl(context, min, device, start_time):
    time.sleep(int(min)*60)


@then('the current time on "{device}" should be {offset} hour ahead of "{real_start_time}"')
def step_impl(context, device, offset, real_start_time):
    ret = context.dut[device].main().show_clock()
    clock_time = ret['Current Time']

    clock_datetime = datetime.strptime(clock_time, "%a %b %d %H:%M:%S %Y")
    real_start_datetime = datetime.strptime(real_start_time, "%a %B %d %H:%M:%S %Y")
    time_difference = clock_datetime - real_start_datetime

    # Check if the time difference is within 1 hour +1/-0 minute 
    is_within = timedelta(hours=1) <= time_difference <= timedelta(hours=1, minutes=1)

    assert is_within, f'the clock_datetime is {clock_datetime} while real_start_datetime is {real_start_datetime}'


@then('the current time on "{device}" should be {offset} hour behind "{real_end_time}"')
def step_impl(context, device, offset, real_end_time):
    ret = context.dut[device].main().show_clock()
    clock_time = ret['Current Time']

    clock_datetime = datetime.strptime(clock_time, "%a %b %d %H:%M:%S %Y")
    real_end_datetime = datetime.strptime(real_end_time, "%a %B %d %H:%M:%S %Y")
    time_difference = real_end_datetime - clock_datetime

    # Check if the time difference is within 1 hour +0/-1 minute
    is_within = timedelta(hours=1, minutes=-1) <= time_difference <= timedelta(hours=1)

    assert is_within, f'the clock_datetime is {clock_datetime} while real_end_datetime is {real_end_datetime}'