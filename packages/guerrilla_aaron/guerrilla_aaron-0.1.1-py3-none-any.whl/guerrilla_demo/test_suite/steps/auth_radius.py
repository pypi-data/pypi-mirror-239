import os
import time
from behave import *
from datetime import datetime
from steps import common, interface, login


@given(u'modify RADIUS config on "{host}"')
def step_impl(context, host):
    context.hosts[host].radius.add_client(client_name='radiusclient')

    for row in context.table:
        raddb_username = row['username']
        raddb_password = row['password']
        raddb_service_type = row['service_type']
        context.hosts[host].radius.add_users(username=raddb_username,
                                             password=raddb_password,
                                             service_type=raddb_service_type)


@when(u'set Login Authentication as {auth_mode} on "{device}"')
def step_impl(context, device, auth_mode):
    auth_mode_map = {
        "Local":            "local",
        "RADIUS":           "radius",
        "RADIUS_Local":     "radius_local"    
    }[auth_mode]
    context.dut[device].go_config().set_authentication_login_mode(auth_mode=auth_mode_map)


@when(u'set authentication type as {auth_type} for the RADIUS server on "{device}"')
def step_impl(context, device, auth_type):
    context.dut[device].go_config().set_radius_server_auth_type(auth_type=auth_type)


@when(u'start Radius server on "{host}"')
def step_impl(context, host):
    context.hosts[host].radius.build_local_image()
    context.hosts[host].radius.start()


@when(u'stop Radius server on "{host}"')
def step_impl(context, host):
    context.hosts[host].radius.stop()


@then(u'"{host}" "{action}" to login "{device}" as "{username}" with "{password}" via "{console_type}" from {interface}')
@then(u'"{host}" "{action}" to login "{device}" as {username} with password {password} via "{console_type}"')
def step_impl(context, host, action, device, username, password, console_type, interface='lan'):
    target_ip = context.dut_info[device]["testbed"][f"{interface.lower()}_ip"]
    container_flag = False
    result_map = {}

    for row in context.table:
        success_action_flag = {'success': True, 'fail': False}[row['action']]
        result_map[row['console_type']] = False
        wait_time = row['wait_time'] if context.table and 'wait_time' in context.table.headings else 3
        ret = []

        if row['console_type'] == 'HTTP':
            ret_mark = ['access_token', 'login success']
            _filename = f'login_check_http_{datetime.now().isoformat()}'
            cmd = f"curl --location 'http://{target_ip}/api/v1/auth/login' "
            cmd += f"--header 'Content-Type: text/plain' "
            cmd += f"--data '{{\"username\": \"{username}\", \"password\": \"{password}\"}}' -k"
            cmd += f" > {_filename}.log"

            context.hosts[host].shellcmd._ssh.command(cmd, timeout=int(wait_time)).lower()
            for _ in range(int(wait_time) + 4):
                ret = context.hosts[host].shellcmd._ssh.command(f'cat {_filename}.log')
                if any(map(lambda s: s in ret, ret_mark)) or 'Invalid Authentication Information' in ret:
                    break
                time.sleep(1)

        elif row['console_type'] == 'HTTPS':
            ret_mark = ['access_token', 'login success']
            _filename = f'login_check_https_{datetime.now().isoformat()}'
            cmd = f"curl --location 'https://{target_ip}/api/v1/auth/login' "
            cmd += f"--header 'Content-Type: text/plain' "
            cmd += f"--data '{{\"username\": \"{username}\", \"password\": \"{password}\"}}' -k"
            cmd += f" > {_filename}.log"
            
            context.hosts[host].shellcmd._ssh.command(cmd, timeout=int(wait_time)).lower()
            for _ in range(int(wait_time) + 4):
                ret = context.hosts[host].shellcmd._ssh.command(f'cat {_filename}.log')
                if any(map(lambda s: s in ret, ret_mark)) or 'Invalid Authentication Information' in ret:
                    break
                time.sleep(1)

        elif row['console_type'] == 'Telnet':
            ret_mark = ['Firewall/VPN Router', 'MOXA']
            wait_time = int(wait_time) + 5
            cmd = f'''/bin/bash -c '(sleep 2; echo "{username}"; sleep 2; echo "{password}"; sleep {wait_time}) | \
            telnet {target_ip} > login_check_telnet.log' '''

            container_flag = True
            context.hosts[host].dut_ui.cli_cmd(cmd, detach=True)
            for _ in range(int(wait_time) + 5):
                ret = context.hosts[host].dut_ui.cli_cmd("/bin/bash -c 'cat login_check_telnet.log'")
                if any(map(lambda s: s in ret, ret_mark)) or 'Login incorrect' in ret:
                    break
                time.sleep(1)

        elif row['console_type'] == 'SSH':
            ret_mark = ['Firewall/VPN Router', 'MOXA']
            sleep_time = '3' if success_action_flag else '10'
            cmd = f'''/bin/bash -c 'sshpass -p {password} ssh -o "StrictHostKeyChecking no" \
            {username}@{target_ip} > login_check_ssh.log' '''

            container_flag = True
            context.hosts[host].dut_ui.cli_cmd(cmd, detach=True)
            for _ in range(int(wait_time) + 5):
                ret = context.hosts[host].dut_ui.cli_cmd("/bin/bash -c 'cat login_check_ssh.log'")
                if any(map(lambda s: s in ret, ret_mark)) or 'Permission denied' in ret:
                    break
                time.sleep(1)
            
        else:
            raise ValueError(f'This console type not supported: {console_type}')
        
        result_map[row['console_type']] = True if any(map(lambda s: s in ret, ret_mark)) else False
        print(result_map)
        time.sleep(2)

    if container_flag:
        context.hosts[host].dut_ui.cli_destroy()
    else :
        context.hosts[host].shellcmd._ssh.command('rm login_check_*')
    print(f'\n*---------End of login test--------*\n{result_map}')

    for key, value in result_map.items():
        if success_action_flag and not value:
            context.dut[device].go_config().set_authentication_login_mode(auth_mode='local')
            raise ValueError(f'Login should succeed but FAILS. Login test result: {result_map} \
            \n!!! RECOVERY: Restore DUT settings to the <Local> authentication mode. !!!')
        elif not success_action_flag and value: 
            context.dut[device].go_config().set_authentication_login_mode(auth_mode='local')
            raise ValueError(f'Login should fails but SUCCEED. Login test result: {result_map} \
            \n!!! RECOVERY: Restore DUT settings to the <Local> authentication mode. !!!')
