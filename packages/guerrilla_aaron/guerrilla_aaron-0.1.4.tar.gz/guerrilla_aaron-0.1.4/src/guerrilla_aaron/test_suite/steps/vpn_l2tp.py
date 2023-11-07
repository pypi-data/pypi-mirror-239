from behave import *
from steps import common, interface, login


@when(u'set L2TP server on "{device}"')
def step_impl(context, device):
    local_ip = context.table[0]['Local IP']
    end_ip = context.table[0]['Offered IP: End']
    context.start_ip = context.table[0]['Offered IP: Start']

    context.cfg = context.dut[device].go_config()
    context.l2tp_cfg = context.cfg.L2tp(context.cfg.get_session())
    context.l2tp_cfg.set_l2tp_rule(local_ip, context.start_ip, end_ip)


@when(u'set L2TP user on "{device}"')
def step_impl(context, device):
    username = context.table[0]['Username']
    password = context.table[0]['Password']

    context.l2tp_cfg.set_l2tp_user(username, password)


@then(u'the following rule should be on "{device}"s l2tp table')
def step_impl(context, device):
    server_mode = context.table[0]['Server Mode']
    local_ip = context.table[0]['Local IP']
    username = context.table[0]['User Name']
    offered_ip = context.table[0]['Offered IP Range'].replace('-', '').split()
    flag = False

    ret = context.dut[device].main().show_l2tp_setting()[0]
    if ret['server_mode'] == server_mode and ret['local_ip'] == local_ip and \
        ret['start_ip'] == offered_ip[0] and ret['end_ip'] == offered_ip[1] and \
        ret['username'] == username:

        flag = True

    assert flag, f"l2tp is not setting up correctly ->\n expect: {context.table[0]}\n actual: {ret}"


@when(u'"{host}" tries to establish l2tp connection to "{device}"s l2tp server')
def step_impl(context, host, device):
    context.hosts[host].nmcli.intf_setting(managed=True)

    context.con_name = 'test_l2tp'

    ## Create a new host named "l2tp_client" based on HOST_A.
    context.hosts['l2tp_client'] = context.hosts['HOST_A']
    context.host_info['l2tp_client'] = context.host_info['HOST_A']
    context.host_info['l2tp_client']["testbed"]["cur_host"] = context.start_ip

    context.hosts[host].nmcli.create_connection(
        con_type='vpn',
        con_name=context.con_name,
        vpn_type='l2tp',
        gateway=context.dut_info[device]['testbed']['wan_ip'],
        user='user',
        password='admin')
    context.hosts[host].nmcli.activate_connection(con_name=context.con_name,
                                                  ifname='eth1')


@then(u'verify "{host}" is assigned the IP "{ip}" with interface "{intf}"')
def step_impl(context, host, ip, intf):
    ret = context.hosts[host].shellcmd.show_network(dev=intf)
    ret = context.hosts[host].shellcmd.show_network()

    assert 'does not exist' not in ret, f'{intf} does not exist'
    assert ip in ret, f'Interface "{intf}" has no ip "{ip}"'


@given(u'disable and clean up l2tp connection on "{host}"')
def step_impl(context, host):

    context.hosts[host].nmcli.deactivated_connection(con_name=context.con_name)
    context.hosts[host].nmcli.delete_connection(con_name=context.con_name)
    context.hosts[host].nmcli.intf_setting(managed=False)
