import time
from guerrilla_aaron.host import *
from behave import *
from guerrilla_aaron.steps import login, interface, common

@fixture
def run_mail_server(context, host):
    try:
        # -- SETUP-FIXTURE
        context.hosts[host].mail_server.start()
        yield
    finally:
        # -- CLEANUP-FIXTURE
         context.hosts[host].mail_server.clean_up("mail_server")

@fixture
def run_mutt_client(context, host, ip):
    try:
        # -- SETUP-FIXTURE
        context.hosts[host].mail_server.set_mutt_service(ip=ip)
        yield
    finally:
        # -- CLEANUP-FIXTURE
         context.hosts[host].mail_server.clean_up("mutt")

@Given('disable auto-logout on "{device}"')
def step_impl(context, device):
    context.dut[device].go_config()._s.command_expect('ip auto-logout 0')

@When('run email server on "{host}" with following configuration')
def step_impl(context, host):
    use_fixture(run_mail_server, context, host)
    for row in context.table:
        context.hosts[host].mail_server.add_mailserver_account(user=row["user"], paswd=row["paswd"])
    context.hosts[host].mail_server.set_mailserver()
    context.hosts[host].mail_server.set_local_hosts(ip=context.host_info[host]['testbed']['lan_host'])

@When('run mutt client on "{host}" with following configuration')
def step_impl(context, host):  
    use_fixture(run_mutt_client, context, host, ip=context.host_info[host]['testbed']['lan_host'])

@When('set email settings on "{device}" with following configuration')
def step_impl(context, device):
    cfg = context.dut[device].go_config()
    cfg.MailServer(cfg.get_session()).set_server(context.host_info[context.table[0]["server"]]['testbed']['lan_host'], port='587')
    cfg.MailServer(cfg.get_session()).set_mail_address(context.table[0]["mail_address"])
    cfg.MailServer(cfg.get_session()).set_account(context.table[0]["account"], context.table[0]["paswd"])
    cfg.MailServer(cfg.get_session()).set_sender(context.table[0]["sender"])

@When('send test email from "{device}" to mutt client')
def step_impl(context, device):
    cfg = context.dut[device].go_config()
    cfg.MailServer(cfg.get_session()).send_test()
    time.sleep(20)

@Then('test email can be received by mutt client on "{host}"')
def step_impl(context, host):
    ret = context.hosts[host].mail_server.get_email()
    assert "MOXA Test Mail" in ret, f'Test mail not received: {ret}'