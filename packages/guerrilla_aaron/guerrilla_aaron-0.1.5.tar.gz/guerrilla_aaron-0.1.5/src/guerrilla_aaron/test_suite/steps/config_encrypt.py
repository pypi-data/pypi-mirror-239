import time

from behave import *
from steps.login import loginToDUT
from steps import vpn

@when('create vlan with id "{vlan_id}" on "{device}"')
def step_impl(context, vlan_id, device):
    context.dut[device].go_config().set_vlan_id(vlan_id)


@when('delete vlan with id "{vlan_id}" on "{device}"')
def step_impl(context, vlan_id, device):
    context.dut[device].go_config().set_vlan_id(vlan_id, delete=True)


@when('enable file encryption with signature information as "{info}" and key string as "{key_str}" on "{device}"')
def step_impl(context, info, key_str, device):
    info = {"Encrypt all information":"all",
            "Encrypt sensitive information only":"sensitive"}[info]
    context.dut[device].main().set_config_file(dig_signature="enable", data_encrypt=info, encrypt_pwd=key_str)


@when('disable file encryption on "{device}"')
def step_impl(context, device):
    context.dut[device].main().set_config_file(dig_signature="disable")


@then('import configuration file to "{device}" from {server} failed')
def step_impl(context, device, server):
    ret = context.dut[device].main().import_config(tftp_ip=context.host_info["HOST_EXECUTOR"]["testbed"]["cur_host"])
    context.dut[device].close()
    assert "Config file import failed" in ret['data'] or "Configuration Upgrade Fail" in ret['data'], \
        f'Configuration Import Successfully: {ret["data"]}'
    loginToDUT(context, device)


@then('import configuration file to "{device}" from {server} successfully')
def step_impl(context, device, server):
    ret = context.dut[device].main().import_config(
        tftp_ip=context.host_info["HOST_EXECUTOR"]["testbed"]["cur_host"])
    context.dut[device].close()
    assert ret['matched'] and '^Parse error' not in ret[
        'data'], f'Configuration Import Fail: {ret["data"]}'
    loginToDUT(context, device)
    time.sleep(10)


@then('vlan id "{vlan_id}" is not on "{device}"')
def step_impl(context, vlan_id, device):
    ret = context.dut[device].main().show_vlan()
    for i in ret:
        if i['vid']==vlan_id:
            assert False, f'vlan id {vlan_id} is on {device}' 


@then('vlan id "{vlan_id}" is on "{device}"')
def step_impl(context, vlan_id, device):
    ret = context.dut[device].main().show_vlan()
    flag = 0
    for i in ret:
        if i['vid']==vlan_id:
            flag = 1
            break
    assert flag==1, f'vlan id {vlan_id} is not on {device}' 


@when('create NTP Authentication Keys on "{device}"')
def step_impl(context, device):
    context.dut[device].go_config().set_ntp_auth(context.table[0]['key_id'], context.table[0]['key_type'], context.table[0]['key'])


@when('enable PPTP Dialup on "{device}"')
def step_impl(context, device):
    context.dut[device].go_config_if_wan().set_pptp(context.table[0]['ip'], context.table[0]['username'], context.table[0]['password'])


@when('create account for L2TP on "{device}"')
def step_impl(context, device):
    context.dut[device].go_config().set_l2tp_user(context.table[0]['username'], context.table[0]['password'])


@when('set email account on "{device}"')
def step_impl(context, device):
    context.dut[device].go_config().set_email(context.table[0]['username'], context.table[0]['password'])


@when('configure Dynamic DNS on "{device}"')
def step_impl(context, device):
    context.dut[device].go_config().set_ddns(name=context.table[0]['username'], pwd=context.table[0]['password'])


@when('set IEEE 802.1X radius 1st-server on "{device}"')
def step_impl(context, device):
    context.dut[device].go_config().set_dot1x_radius_server(server_idx=1, key=context.table[0]['share_key'])


@when('set IEEE 802.1X Local Database on "{device}"')
def step_impl(context, device):
    context.dut[device].go_config().set_dot1x_local_db(context.table[0]['username'], context.table[0]['password'])


@when('set RADIUS server on "{device}"')
def step_impl(context, device):
    """
     RADIUS authentication server index must be 1~2.
        1: Primary RADIUS authentication server
        2: Backup RADIUS authentication server
    """
    for row in context.table:
        context.dut[device].go_config().set_radius_server(server_idx=row['idx'], 
                                                          ip=row['ip'], 
                                                          port=row['port'], 
                                                          key=row['share_key'])


@when('add OSPF area on "{device}"')
def step_impl(context, device):
    context.dut[device].go_config_ospf(context.table[0]['router_id']).set_ospf_area(context.table[0]['area_id'])


@when('create interface for ospf on "{device}"')
def step_impl(context, device):
    if context.table[0]['interface'] == "LAN":
        if context.table[0]['auth_type'] == "simple":
            context.dut[device].go_config_if_lan().set_ospf(area_id=context.table[0]['area_id'], 
                                                        auth={'type':context.table[0]['auth_type'],
                                                              'key':context.table[0]['auth_key']})
        elif context.table[0]['auth_type'] == "md5":
            context.dut[device].go_config_if_lan().set_ospf(area_id=context.table[0]['area_id'], 
                                                        auth={'type':context.table[0]['auth_type'],
                                                              'key':context.table[0]['auth_key'],
                                                              'key_id':context.table[0]['auth_key_id']})


@then('the following sensitive information in running config on "{device}" is encrypted')
def step_impl(context, device):
    context.running_config = context.dut[device].main().get_running_config(context.dut_info[device]["session"]["con_type"]).replace("\r", "").split('\n')
    for i in range(len(context.running_config)):
        for j in context.table:
            if j['information'] in context.running_config[i]:
                ret = context.running_config[i].split(' ')[-1]
                if len(ret)>50 and ret!=j['original_value']:
                    print(f"{j['information']}:{ret} ok pass!")                    
                    assert True
                else:
                    assert False, f"{j['information']}:{ret} not encrypted!"
                break