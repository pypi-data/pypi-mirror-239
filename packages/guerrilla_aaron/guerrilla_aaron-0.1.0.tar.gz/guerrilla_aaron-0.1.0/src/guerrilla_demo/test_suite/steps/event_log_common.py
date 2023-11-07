import re
import sys
import time
import json

from host import *
from behave import *
from steps import syslog


def check_message(ret, msg):
    for r in ret:
        if msg in r['event']:
            return True
    return False


@given('"{device}" records event log "{message}"')
def step_impl(context, device, message):
    ret = context.dut[device].main().show_logging_event_log_system()
    assert check_message(ret, message), \
    f"DUT fail to record event logs: expect {message}, but {[r['event'] for r in ret]}"
    context.dut[device].main().clear(event_log='all')


@then('"{device}"s event log is cleared')
def step_impl(context, device):
    ret = context.dut[device].main().show_logging_event_log_system()
    assert ret[0]['number'] == '0', \
    f"DUT fail to clear system event logs: expect 0 number of event logs, but got {ret['number']} event logs"


@when('export "{device}" {category} eventlog file to {server} server on "{host}"')
def step_impl(context, device, category, server, host):
    context.dut[device].main().export_eventlog(server=server,
                                               server_ip=context.host_info[host]['testbed']['cur_host'],
                                               category=category)
 
@then(
    'the comparison between running {event_type} eventlog on "{device}" and exported system eventlog must be the same'
)
def step_impl(context, event_type, device):
    with open(f'//tftp/{event_type}.json') as f:
        data = json.load(f)
    print('data: ', data)
    ret = context.dut[device].main().show_logging_event_log_system()
    system_eventlog = dict(reversed(list(ret[0].items())))
    print('system_eventlog: ', system_eventlog)
    for i in range(max(len(system_eventlog), len(data[0]))):
        assert system_eventlog['event'] == data[0]['LOGSTR'], \
            f"from line {i} running system is different from ini:\n \
              running system line {i}: {system_eventlog['event']},\n\
              ini line {i}: {data[0]['LOGSTR']}"
