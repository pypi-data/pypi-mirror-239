import re
import sys
import time

from host import *
from behave import *
from steps import common, interface, login


@given(u'enable dhcp service on "{device}"')
def step_impl(context, device):
    cfg = context.dut[device].go_config()
    cfg.DhcpService(cfg.get_session()).set_global_dhcp_service("enable")


@given(
    u'set configuration of {mode} dhcp server on "{device}" for dispatching ip to "{host}"'
)
def step_impl(context, mode, device, host):
    cfg = context.dut[device].go_config()
    if mode == "dhcp":
        context.host_info[list(context.hosts.keys(
        ))[0]]['testbed']['cur_host'] = context.table[0]['pool_ip_begin']
        context.dut[device].go_config_dhcp(1).set_dhcp_server(\
            network_begin=context.table[0]['pool_ip_begin'], \
            network_end=context.table[0]['pool_ip_end'], \
            network_mask=context.table[0]['mask'], \
            lease = context.table[0]['lease_time'], \
            default_router=context.table[0]['default_gw']). \
        exit()
        cfg.DhcpService(cfg.get_session()).set_global_dhcp_server(
            mode="pool", action="enable", index="1")

    elif mode == "mac-based":
        context.host_info[host]['testbed']['cur_host'] = context.table[1][
            'ip_host']
        context.dut[device].go_config_dhcp(mode).set_dhcp_server(\
            host=context.table[1]['ip_host'], \
            host_mask=context.table[1]['mask'], \
            hardware_address=context.host_info[host]['testbed']['mac_address'], \
            lease=context.table[1]['lease_time'], \
            default_router=context.table[1]['default_gw']). \
        exit()
        cfg.DhcpService(cfg.get_session()).set_global_dhcp_server(
            mode="static pool", action="enable", name=mode)
    else:
        raise ValueError(f'input dhcp mode is incorrect: {mode}')


@when(u'enable dhcp client in "{host}"')
def step_impl(context, host):
    context.hosts[host].shellcmd.enable_dhcp_client(
        dev=context.host_info[host]['nic'])


@then(u'"{host}" can receive ip address from {mode} server')
def step_impl(context, host, mode):
    count = 0
    ret = '' \
    if context.hosts[host].shellcmd.show_network(dev=context.host_info[host]['nic']) is None \
    else context.hosts[host].shellcmd.show_network(dev=context.host_info[host]['nic'])
    while 'inet' not in ret and count != 10:
        time.sleep(1)
        ret = '' \
        if context.hosts[host].shellcmd.show_network(dev=context.host_info[host]['nic']) is None \
        else context.hosts[host].shellcmd.show_network(dev=context.host_info[host]['nic'])
        count += 1
    print('ret:', ret)
    host_ip = re.findall(r'\d+\.\d+\.\d+\.\d+', ret)[0]
    cur_ip = host_ip.split('.')[-1]
    begin_ip = context.table[0]['pool_ip_begin'].split('.')[-1]
    end_ip = context.table[0]['pool_ip_end'].split('.')[-1]
    context.host_info[host]['testbed']['cur_host'] = host_ip
    if mode == "dhcp":
        assert int(begin_ip) <= int(cur_ip) <= int(
            end_ip
        ), f'{host} can not get ip within given pool from dhcp server: {host_ip}'
    elif mode == "mac-based":
        assert host_ip == context.table[0][
            'ip_host'], f'{host} can not get specified ip from dhcp server: {host_ip}'
    else:
        raise ValueError(f'input mode is incorrect: {mode}')


@then(u'"{device}" can ping "{host}"s received ip address')
def step_impl(context, device, host):
    ret = context.dut[device].main().ping(
        context.host_info[host]['testbed']['cur_host'])
    assert int(
        ret['received']) > 0, f'{device} can not ping {host} successfully'
