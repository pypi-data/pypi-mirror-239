from host import *
from behave import *
from steps.login import loginToDUT
from steps import common, interface, login
import time


@given(
    u'create "{tcp_connection}" with destination "{host}" and limitation "{conn_num}" on "{device}"'
)
def step_impl(context, tcp_connection, host, conn_num, device):
    '''
        Sessoion control rule will be like:
        index 1 session_1 dst_ip: dst_lan, ttl_tcp_conn: 10
    '''
    dst_ip = context.host_info[host]["testbed"]["cur_host"]
    obj_name = f'dst_{host}'
    # cerate object
    context.object = context.dut[device].go_config_object_addr().create_object(
        name=obj_name, ip_addr=dst_ip)

    context.dut[device].main().command('show object')

    # create session control policy
    context.session_name = f'session_{int(time.time())}'
    context.tcp_connection = tcp_connection
    context.index = 1
    if tcp_connection == 'total_tcp_connection':
        context.dut[device].go_config_session_ctrl().set_session_ctrl(
            name=context.session_name,
            enable=True,
            logging="enable",
            policy_action="deny",
            dip=obj_name,
            dport=None,
            ttl_tcp_conn=conn_num)
    elif tcp_connection == 'concurrent_tcp_conn':
        context.dut[device].go_config_session_ctrl().set_session_ctrl(
            name=context.session_name,
            enable=True,
            logging="enable",
            policy_action="deny",
            dip=obj_name,
            dport=None,
            concur_tcp_conn=conn_num)

    context.dut[device].main().command('show session-control')


@then(u'the session control rule is successfully {status} on "{device}"')
def step_impl(context, status, device):
    ret = context.dut[device].main().show_session_ctrl()
    flag = 0
    for i in ret:
        context.index = i['index']
        print(context.index)
        if i['session_name'] == context.session_name:
            flag = 1
            break
    if status == 'created':
        assert flag, f"the {context.session_name} session is not created"
    elif status == 'deleted':
        assert not flag, f"the {context.session_name} session is not deleted"


@when(u'create "{ssh_num}" TCP connection from "{host1}" to "{host2}"')
def step_impl(context, ssh_num, host1, host2):
    server_ip = context.host_info[host2]["testbed"]["cur_host"]
    server_account = context.host_info[host2]['session']["credential"][
        "username"]
    server_password = context.host_info[host2]['session']["credential"][
        "password"]

    context.hosts[host2].tshark.start(interface=context.host_info[host2]['nic'])
    time.sleep(2)

    context.hosts[host1].dut_ui.cli_init()
    for i in range(int(ssh_num)):
        print(f'this is {i} time to establish ssh session')
        context.hosts[host1].dut_ui.cli_cmd(
            f'''/bin/bash -c 'sshpass -p {server_password} ssh -o "StrictHostKeyChecking no" {server_account}@{server_ip}' ''',
            detach=True)
    time.sleep(2)
    context.hosts[host1].dut_ui.cli_destroy()


@when(
    u'send "{ssh_num}" TCP syn from "{host1}" to "{host2}" within 1 sec'
)
def step_impl(context, ssh_num, host1, host2):
    server_ip = context.host_info[host2]["testbed"]["cur_host"]
    server_account = context.host_info[host2]['session']["credential"][
        "username"]
    server_password = context.host_info[host2]['session']["credential"][
        "password"]

    context.hosts[host2].tshark.start(interface=context.host_info[host2]['nic'])
    time.sleep(2)

    print('== Trying to establish ssh session ==')
    context.hosts[host1].hping3.send( \
        tcpudp_flags=['syn'], \
        host = context.host_info[host2]['testbed']['cur_host'], \
        count = ssh_num, \
        port = 22)
    time.sleep(5)


@then(
    u'"{ssh_num}" TCP connection will be established from "{host1}" to "{host2}"'
)
def step_impl(context, ssh_num, host1, host2):
    context.hosts[host2].tshark.stop()
    ret = context.hosts[host2].tshark.retrieve()
    print(ret)
    count = 0
    if ret != None:
        print(
            f'{context.host_info[host2]["testbed"]["cur_host"]} → {context.host_info[host1]["testbed"]["cur_host"]} [SYN]'
        )  #
        count = ret.count(
            f'{context.host_info[host2]["testbed"]["cur_host"]} → {context.host_info[host1]["testbed"]["cur_host"]}' and \
            '→ 22 [SYN]')

    assert count == int(
        ssh_num
    ), f'expect receive {ssh_num} number of SYN but receive {count}, {ret}'
