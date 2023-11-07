import time

from behave import *


@fixture
def getSyslogServer(context, host):
    try:
        context.hosts[host].syslog.start()
        yield
    finally:
        try:
            context.hosts[host].syslog.stop()
        except:
            print('syslog server is no activated')


@given('run syslog service on "{host}"')
def step_impl(context, host):
    use_fixture(getSyslogServer, context, host)


@given('set and enable syslog server with {host} IP on "{device}"')
def step_impl(context, device, host):
    print("syslog ip", context.host_info[host]["testbed"]["cur_host"])
    context.dut[device].go_config().set_syslog_server(
        action="create", ip=context.host_info[host]["testbed"]["cur_host"])
    context.dut[device].main().show_syslog_setting()


@given('"{device}" enable system-event with "{item}" for syslog action')
def step_impl(context, device, item):
    context.dut[device].go_config().set_warning_notification(
        event=item, active=True, action="Syslog only")


@then('"{host}" receive syslog "{receive_syslog}"')
def step_impl(context, host, receive_syslog):
    time.sleep(5)
    t = 0
    logs = context.hosts[host].syslog.read_message()
    while receive_syslog not in logs and t != 60:
        logs = context.hosts[host].syslog.read_message()
        time.sleep(1)
        t += 1
        # print(type(logs))
        print("logs=", logs)
    assert receive_syslog in logs, f'cannot find "{receive_syslog}" in syslog: {logs}'
