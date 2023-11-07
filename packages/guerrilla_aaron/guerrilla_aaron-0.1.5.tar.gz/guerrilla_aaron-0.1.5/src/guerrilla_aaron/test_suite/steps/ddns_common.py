import time

from behave import *
from steps import common, interface, login


@when(u'set ddns server with following table on "{device}"')
def step_impl(context, device):
    context.dut[device].go_config().set_ddns(service = context.table[0]['service'], 
                                             name = context.table[0]['username'], 
                                             pwd = context.table[0]['password'],
                                             domain = context.table[0]['domain'])

@when(u'set dns server on "{device}"')
def step_impl(context, device):
    context.dut[device].go_config_if_wan().set_dns(dns_server_1 = context.table[0]['dns_server_1'], 
                                                   dns_server_2 = context.table[0]['dns_server_2'],
                                                   dns_server_3 = context.table[0]['dns_server_3'])

@then(u'dig the domain name from "{host}" to check if the domain ip is replaced with "{device}"s {interface} ip')
def step_impl(context, host, device, interface):
    flag = False
    break_count = 0
    while not flag:
        ret_wan = context.dut[device].main().show_interface(name = 'wan')
        ret_dig = context.hosts[host].shellcmd.dig(context.table[0]['domain'])
        print(f'ret_wan: {ret_wan}, ret_dig: {ret_dig}')
        if ret_wan[0]['ip_address'].strip() in ret_dig:
            flag = True
        if break_count == 30:
            break
        break_count += 1
        time.sleep(10)
    assert flag, f'Domain ip is not changed by ddns, ori:{ret_dig}, expect:{ret_wan}'