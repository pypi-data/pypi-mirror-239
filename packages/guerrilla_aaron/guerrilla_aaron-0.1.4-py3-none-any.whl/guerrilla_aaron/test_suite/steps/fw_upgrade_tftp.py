import re
import sys
import time

from host import *
from behave import *
from steps import common, interface, login


def check_message(ret, msg):
    for r in ret:
        if msg in r['event']:
            return True
    return False

@given(u'run tftp service on "{host}"')
def step_impl(context, host):
    context.hosts[host].tftp.check_env()

@given(u'get running firmware version from "{device}"')
def step_impl(context, device):
    ret = context.dut[device].main().show_version()
    model_tmp = ret[0]['model_name'].split('-')
    model = model_tmp[0] + '-' + model_tmp[1]
    version = ret[0]['firmware_version'].replace("build", "Build").replace(" ", "_") 
    if 'TN-49' in model:
        model = 'TN-4900'
    elif 'TN-59' in model:
        model = model.replace("-", "")
    context.fw = 'FWR_' + model + '_' + version + '.rom'
    print(context.fw)

@then(
    u'"{device}" record two event logs "{message_1}" and "{message_2}" with "Firmware Upgrade"'
)
def step_impl(context, device, message_1, message_2):
    ret = context.dut[device].main().show_logging_event_log_system()
    assert check_message(ret, message_1) and check_message(ret, message_2), \
    f"DUT fail to record event logs: expect {message_1} and {message_2}, but {[r['event'] for r in ret]}"

@then(u'"{device}" record one event log "{message_1}"')
def step_impl(context, device, message_1):
    ret = context.dut[device].main().show_logging_event_log_system()
    assert message_1 in [r['event'] for r in ret], \
    f"DUT fail to record event logs: expect {message_1}, but {[r['event'] for r in ret]}"

@then(u'show version containing the correct information of {firmware} on "{device}"')
def step_impl(context, device, firmware):
    version = re.findall(r'V(.*)_Build_(\d+)', firmware)[0][0]
    build = re.findall(r'V(.*)_Build_(\d+)', firmware)[0][1]
    ret = context.dut[device].main().show_version()
    assert version in ret[0]['firmware_version'] and build in ret[0]['firmware_version'], \
    f"Expect {version}_{build} but {ret[0]['firmware_version']}"

@then(u'check "{device}" is upgraded back to the running firmware')
def step_impl(context, device):  
    version = re.findall(r'V(.*)_Build_(\d+)', context.fw)[0][0]
    build = re.findall(r'V(.*)_Build_(\d+)', context.fw)[0][1]
    ret = context.dut[device].main().show_version()
    assert version in ret[0]['firmware_version'] and build in ret[0]['firmware_version'], \
    f"Expect {version}_{build} but {ret[0]['firmware_version']}"

@when(u'upgrade "{device}" back to running firmware')
def step_impl(context, device):  
    ret = context.dut[device].main().upgrade_firmware(
        tftp_ip=context.host_info["HOST_EXECUTOR"]["testbed"]["cur_host"],
        file_name=context.fw)
    context.dut[device].close()
    assert ret['matched'] and '^Parse error' not in ret['data']
    login.loginToDUT(context, device)
    time.sleep(10)
