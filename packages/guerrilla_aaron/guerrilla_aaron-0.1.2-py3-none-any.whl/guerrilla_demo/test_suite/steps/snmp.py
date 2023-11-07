from host import *
from behave import *
import time


@when(u'set snmp version to {snmp_version} on "{device}"')
@given(u'set snmp version to {snmp_version} on "{device}"')
def step_impl(context, snmp_version, device):
    context.cfg = context.dut[device].go_config()
    context.cfg.Snmp(context.cfg.get_session()).set_snmp_version(snmp_version)


## only SNMPv3
@when(u'set snmp user authentication and privacy method on "{device}"')
def step_impl(context, device):
    context.user = context.table[0]['User']
    context.security = context.table[0]['Security level']
    context.auth_type = context.table[0]['Auth Type'].lower()
    if context.table[0]['Priv Method'].lower() == 'none':
        context.priv_method = None
    else:
        context.priv_method = context.table[0]['Priv Method'].lower()
    context.priv_key = context.table[0]['Priv Key']

    context.cfg.Snmp(context.cfg.get_session()).set_snmp_user(
        user=context.user,
        priv_key=context.priv_key,
        auth_type=context.auth_type,
        priv_method=context.priv_method)


## only SNMPv3
@when(u'set password for the following account on the "{device}"')
@given(u'set password for the following account on the "{device}"')
def step_impl(context, device):

    if context.auth_type != 'no-auth':

        context.auth_key = context.table[0]['Password']

        ## default.yaml user password
        context.dut_info[device]['credential']['password'] = context.auth_key
        context.cfg.set_login_account(action='modify',
                                      username=context.table[0]['User'],
                                      password=context.auth_key)
    else:
        context.auth_key = None


## only SNMPv3
@when(u'set snmp engineid to "{engine_id}"')
def step_impl(context, engine_id):
    context.cfg.Snmp(
        context.cfg.get_session()).set_engine_id(engine_id=engine_id)


@then(u'the following rule should be on "{device}"s snmp setting table')
def step_impl(context, device):
    flag = False
    snmp_setting = context.dut[device].main().show_snmp()

    for entry in snmp_setting:
        if entry['version'] == context.table[0]['Version'] and \
            entry['engine_id'] == context.table[0]['Engine ID'] and \
            entry['admin_auth_status'] == context.table[0]['Auth status'] and \
            len(entry['admin_auth_key']) == len(context.table[0]['Auth passwd']) :
            flag = True
            break

    assert flag, set_to_default_passwd(
        context,
        f"No match found -> expect: {context.table[0]}, actual: {snmp_setting}")


@when(u'get the sysname from "{device}"')
def step_impl(context, device):
    res = context.dut[device].main().show_system()
    time.sleep(5)
    context.sysname = res[0]['system_name']


@then(
    u'"{host}" {can_or_cannot} get "{device}"s sysname by SNMP version {version}'
)
def step_impl(context, host, can_or_cannot, device, version):

    if version == '1' or version == '2c':
        ret = context.hosts[host].snmp.get_snmp(
            version=version,
            community='public',
            agent_id=context.dut_info[device]['testbed']['lan_ip'],
            oid='1.3.6.1.2.1.1.5.0')

    if version == '3':
        ret = context.hosts[host].snmp.get_snmp(
            version=version,
            username=context.user,
            security=context.security,
            auth_type=context.auth_type,
            auth_key=context.auth_key,
            priv_method=context.priv_method,
            priv_key=context.priv_key,
            agent_id=context.dut_info[device]['testbed']['lan_ip'],
            oid='1.3.6.1.2.1.1.5.0')

    if can_or_cannot == 'can':
        assert context.sysname in ret, set_to_default_passwd(
            context,
            f'Expected to receive SNMP message, but did not receive. actual: {ret}'
        )

    if can_or_cannot == 'can not':
        assert context.sysname not in ret, set_to_default_passwd(
            context,
            f'Expected not to receive SNMP message, but received. return: {ret}'
        )


@given(
    u'"{host}" send snmp set request to set "{device}"s sysnem as "{new_sysname}" by SNMP version {version}'
)
def step_impl(context, host, device, version, new_sysname):

    if version == '1' or version == '2c':
        ret = context.hosts[host].snmp.set_snmp(
            version=version,
            community='private',
            agent_id=context.dut_info[device]['testbed']['lan_ip'],
            oid='1.3.6.1.2.1.1.5.0',
            new_info=new_sysname)

    if version == '3':
        ret = context.hosts[host].snmp.set_snmp(
            version=version,
            username=context.user,
            security=context.security,
            auth_type=context.auth_type,
            auth_key=context.auth_key,
            priv_method=context.priv_method,
            priv_key=context.priv_key,
            agent_id=context.dut_info[device]['testbed']['lan_ip'],
            oid='1.3.6.1.2.1.1.5.0',
            new_info=new_sysname)


@then(u'"{device}"s sysname {can_or_not} be set to "{new_sysname}"')
def step_impl(context, device, can_or_not, new_sysname):
    time.sleep(5)
    res = context.dut[device].main().show_system()
    current_sysname = res[0]['system_name']

    if can_or_not == 'can':
        assert current_sysname == new_sysname, set_to_default_passwd(
            context,
            f'No match found, except -> {new_sysname}; actual -> {current_sysname}'
        )
    else:
        assert current_sysname != new_sysname, set_to_default_passwd(
            context,
            f"Sysname should not be same, but it's same -> {new_sysname}; actual -> {current_sysname}"
        )


@given(u'set password and sysname to default on the "{device}"')
def step_impl(context, device):
    set_to_default_passwd(context, message=None)
    context.cfg.set_hostname(context.sysname)
    res = context.dut[device].main().show_system()


def set_to_default_passwd(context, message):
    try:
        cfg = context.dut['DUT'].go_config()
        cfg.set_login_account(action='modify',
                              username="admin",
                              password="moxa")
    except:
        print('The sysname has not been changed by this test case.')

    if message:
        print(message)


@given(u'set snmp trap/inform trap mode to {mode} on "{device}"')
def step_impl(context, mode, device):

    if 'v3' in mode:
        user = context.table[0]['User']
        auth_type = context.table[0]['Auth Type'].lower()
        passwd = context.table[0]['Password']
        priv_key = context.table[0]['Priv Key'] if \
            context.table[0]['Priv Key'] else None
        context.cfg.Snmp(context.cfg.get_session()).set_snmp_trap_inform_v3(
            trap_mode=mode,
            user=user,
            auth_type=auth_type,
            passwd=passwd,
            priv_key=priv_key)
    # SNMPv2-inform
    elif 'inform' in mode and '2c' in mode:
        mode = 'inform'
        retry = context.table[0]['Inform Retry']
        timeout = context.table[0]['Inform Timeout']
        context.cfg.Snmp(context.cfg.get_session()).set_snmp_trap_mode(
            trap_mode=mode, retry=retry, timeout=timeout)
    # SNMPv1, v2 trap
    else:
        context.cfg.Snmp(
            context.cfg.get_session()).set_snmp_trap_mode(trap_mode=mode)


@given(u'set snmp trap/inform host to receive snmp notification on "{device}"')
def step_impl(context, device):
    host_ip = context.table[0]['Host IP']
    community = context.table[0]['Community']

    context.cfg.Snmp(context.cfg.get_session()).set_snmp_trap_host(
        host_ip, community)


@when('starts tshark sniffer on "{host}" for snmp packet')
def step_impl(context, host):
    context.hosts[host].tshark.start(interface=context.host_info[host]['nic'],
                                     display_filter="snmp")
    time.sleep(5)


@when(
    'starts tshark sniffer and decrypt message on "{host}" for snmp packet {with_without} verbose'
)
def step_impl(context, host, with_without):
    uat = context.table[0]['UAT']
    username = context.table[0]['username']
    auth_type = context.table[0]['Auth Type']
    passwd = context.table[0]['Password']
    encry_method = context.table[0]['Encrypt Method']
    encry_key = context.table[0]['Encrypt Key']
    verbose = True if with_without == 'with' else False

    context.hosts[host].tshark.start(
        interface=context.host_info[host]['nic'],
        display_filter="snmp",
        verbose=verbose,
        option=
        f'uat:{uat},\"{username}\",\"{auth_type}\",\"{passwd}\",\"{encry_method}\",\"{encry_key}\"'
    )
    time.sleep(5)


@given(
    u'starts snmptrapd tool on "{host}" to report SNMPv3 inform to get informRequest'
)
def step_impl(context, host):
    context.hosts[host].snmp.start_snmptrapd()


@then(
    u'"{host}" should receive {pkt_num} snmp {pkt_name} packet from "{device}"')
def step_impl(context, host, pkt_num, pkt_name, device):
    time.sleep(10)
    context.hosts[host].tshark.stop()
    ret = context.hosts[host].tshark.retrieve().split('\n')

    if len(ret) == 0:
        raise ValueError('packet receiving fails')

    pkt_count = 0

    for line in ret:
        if 'SNMP' in line and pkt_name in line:
            pkt_count += 1

    assert pkt_count >= int(
        pkt_num
    ), f'except to receive {pkt_num} packet(s) but receive {pkt_count}.'


@then(
    u'"{host}" should receive {pkt_num} {pkt_name} snmp packet with the following info from "{device}"'
)
def step_impl(context, host, pkt_num, pkt_name, device):
    time.sleep(10)
    context.hosts[host].tshark.stop()
    ret = context.hosts[host].tshark.retrieve().split('\n')

    if len(ret) == 0:
        raise ValueError('packet receiving fails')

    pkt_count = 0
    info = context.table[0]['info']

    for line in ret:
        if 'SNMP' in line and pkt_name in line and info in line:
            pkt_count += 1

    assert pkt_count >= int(
        pkt_num
    ), f'except to receive {pkt_num} snmp packet(s) but receive {pkt_count}.'


@then(
    u'"{host}" should receive snmp packet with engine id that is same as "{device}"s snmp table'
)
def step_impl(context, host, device):
    snmp_setting = context.dut[device].main().show_snmp()
    except_engine_id = snmp_setting[0]['engine_id']
    time.sleep(10)
    context.hosts[host].tshark.stop()
    ret = context.hosts[host].tshark.retrieve().split('\n')

    if len(ret) == 0:
        raise ValueError('packet receiving fails')

    flag = False
    actual_engine_id = []

    for line in ret:
        if 'contextEngineID' in line:
            actual_engine_id.append(line.strip())
            if except_engine_id in line:
                flag = True

    assert flag, f'The engine id of snmp should be {except_engine_id} but {actual_engine_id}'
