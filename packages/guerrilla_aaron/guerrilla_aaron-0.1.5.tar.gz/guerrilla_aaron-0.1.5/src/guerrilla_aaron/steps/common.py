import re
import time
import requests
from requests.auth import HTTPBasicAuth

from behave import *
from host import HostFactory, SessionFactory
from steps.login import loginToDUT
from topology.topology_info import *
from utils.threading import ThreadWithResult
from mdc.router.cli.rp_base.lg_router.tn5000.base import Base as tn5000

def login_and_measure_time(context, device):
    # try to login DUT after restart
    elapsed_time = 0
    start_time = time.time() 
    is_login = False
    while not is_login and elapsed_time <= 120:
        try:
            end_time = time.time()
            elapsed_time = end_time - start_time
            print('is_login: ', is_login)
            is_login = loginToDUT(context, device)
        except Exception as e:
            print(f'Can not login to DUT yet: {e}')
    
    return elapsed_time

@given(u'prepare "{file_name}" topology')
def step_impl(context, file_name):
    ''' get topology file absloute path from lib 
        e.g. 
            cur_path = /usr/src/app/sqa/{function}/
            root_path = /usr/src/app/
            abs_path = /usr/src/app/lib/topology/
    '''
    prepare_json(context, file_name)


@when('clear "{device}" all logging event log')
@given('clear "{device}" all logging event log')
def step_impl(context, device):
    if issubclass(context.dut[device]._model, tn5000):
        context.dut[device].main().clear_event_log()
    else:
        context.dut[device].main().clear(event_log="all")


def reset(context, device):
    # Step-1: authorize CLI of "{device}"
    # Step-2: reload factory-default "{device}"
    # Step-3: clear "{device}" all logging event log
    context.execute_steps(f'''given authorize CLI of "{device}"''')
    context.execute_steps(f'''when reload factory-default "{device}"''')
    context.execute_steps(f'''given clear "{device}" all logging event log''')


@given('reset all devices')
def step_impl(context):
    reset_threads = []
    for row in context.table:
        reset_threads.append(
            ThreadWithResult(target=reset,
                             kwargs={
                                 'context': context,
                                 'device': row['devices']
                             }))
    for t in reset_threads:
        t.start()
    for t in reset_threads:
        t.join()


@given(u'prepare a "{host}" to connect to "{device}"')
def step_impl(context, host, device):
    info = context.host_info[host]
    context.hosts[host] = HostFactory.create_atb(info)
    context.hosts[host].login()
    context.hosts[host].check_env()
    context.hosts[host].shellcmd.remove_residual_artifact()
    context.hosts[host].shellcmd.set_network(dev=info["nic"], 
                                             ip=info["testbed"]["lan_host"], 
                                             mask=info["testbed"]["mask"])
        
@given(u'check "{host}" has installed {tool}')
def step_impl(context, host, tool):
    if tool.lower() == "tshark":
        context.hosts[host].tshark.check_env()
    elif tool.lower() == "hping3":
        context.hosts[host].hping3.check_env()


@when('reload factory-default "{device}"')
@given('reload factory-default "{device}"')
def step_impl(context, device):
    def _backup():
        ret = context.dut[device].main().import_config(
            tftp_ip=context.host_info["HOST_EXECUTOR"]["testbed"]["cur_host"],
            file_name="default.ini")
        context.dut[device].close()
        assert ret['matched'] and '^Parse error' not in ret[
            'data'], f'Configuration Import Fail: {ret["data"]}'
        login_and_measure_time(context=context, device=device)
    def _reset():
        context.dut[device].go_config().set_hostname('init_check')
        sys_name = context.dut[device].main().show_system()[0]['system_name']
        assert sys_name == 'init_check', \
            f'Set system_name fail: {sys_name}'
        
        context.dut[device].main().reload_factory_default()
        time.sleep(context.dut_info[device]['reload_delay'])
        context.dut[device].close()
        

        login_time = login_and_measure_time(context=context, device=device)
        print(f"Reload Factory Time: {context.dut_info[device]['reload_delay']} + {login_time:.2f} seconds")

        sys_name = context.dut[device].main().show_system()[0]['system_name']
        assert "init_check" not in sys_name, \
            f'Bad hostanme after reload: {sys_name}'
    if context.dut_info[device]['init_method'] == "restore":
        _backup()
    elif context.dut_info[device]['init_method'] == "reset":
        _reset()
    else:
        raise ValueError(f"input wrong initial method, \
                         it should be reset or restore: {context.dut_info[device]['init_method']}")


def do_ping(context, machine1, machine2, result):
    '''
    parameter
        machine can be DUT or host(VM)
        there will be 4 combinations
        1. dut -> host 
        2. dut -> dut 
        3. host -> host 
        4. host -> dut 

        Note:
        if machine2 is dut, you need to specify interface for machine2
        e.g.
            "DUT" will ping "DUT WAN" successfully
            "HOST_A" will ping "DUT WAN" successfully
    '''
    if "dut" in machine1.lower() and "host" in machine2.lower():
        context.hosts[machine2].shellcmd.restart_network(context.host_info[machine2]["nic"])
        for i in range(5):
            # retry 5 times
            r = context.dut[machine1].main().ping(
                context.host_info[machine2]['testbed']['cur_host'])
            if int(r['received']) > 0:
                break
        if result == "successfully":
            assert int(
                r['received']
            ) == 4, f'expect {machine1} ping {machine2} {result}, Packets: Received = {int(r["received"])}'
        else:
            assert int(
                r['received']
            ) == 0, f'expect {machine1} ping {machine2} {result}, Packets: Received = {int(r["received"])}'
        # assert int(r['received']) > 0, f'{machine1} fail to ping {machine2}, Packets: Received = {int(r["received"])}'

    elif "dut" in machine1.lower() and "dut" in machine2.lower():
        machine2_list = machine2.split(' ')
        if len(machine2_list) == 2:
            machine2_name = machine2.split(' ')[0]
            machine2_intf = machine2.split(' ')[1]
        else:
            raise ValueError(
                f"format error: {machine2}, it should contain interface name")
        for i in range(5):
            # retry 5 times
            r = context.dut[machine1].main().ping(
                context.dut_info[machine2_name]["testbed"]
                [f"{machine2_intf.lower()}_ip"])
            if int(r['received']) > 0:
                break
        if result == "successfully":
            assert int(
                r['received']
            ) == 4, f'expect {machine1} ping {machine2} {result}, Packets: Received = {int(r["received"])}'
        else:
            assert int(
                r['received']
            ) == 0, f'expect {machine1} ping {machine2} {result}, Packets: Received = {int(r["received"])}'

    elif "host" in machine1.lower() and "host" in machine2.lower():
        context.hosts[machine1].shellcmd.restart_network(context.host_info[machine1]["nic"])
        context.hosts[machine2].shellcmd.restart_network(context.host_info[machine2]["nic"])
        for i in range(5):
            # retry 5 times
            r = context.hosts[machine1].shellcmd._ssh.command(
                cmd=
                f'ping {context.host_info[machine2]["testbed"]["cur_host"]} -c 4',
                timeout=10)
            # print(r)
            try:
                count = int(re.findall(r'(\d+)\s+received', r)[0])
            except:
                count = None
            if count == 4:
                break
        if result == "successfully":
            assert count == 4, f'expect {machine1} ping {machine2} {result}, Packets: Received = {count}'
        else:
            assert count == 0 or count == None, f'expect {machine1} ping {machine2} {result}, Packets: Received = {count}'

    elif "host" in machine1.lower() and "dut" in machine2.lower():
        context.hosts[machine1].shellcmd.restart_network(context.host_info[machine1]["nic"])
        machine2_list = machine2.split(' ')
        if len(machine2_list) == 2:
            machine2_name = machine2.split(' ')[0]
            machine2_intf = machine2.split(' ')[1]
        else:
            raise ValueError(
                f"format error: {machine2}, it should contain interface name")
        for i in range(5):
            # retry 5 times
            print(f"this is the {i+1} time!!!")
            r = context.hosts[machine1].shellcmd._ssh.command(
                cmd=
                f'ping {context.dut_info[machine2_name]["testbed"][f"{machine2_intf.lower()}_ip"]} -c 4',
                exact_prompts='packet loss',
                timeout=10)
            print(r)
            try:
                count = int(re.findall(r'(\d+)\s+received', r)[0])
            except:
                count = None
            if count == 4:
                break
        if result == "successfully":
            assert count == 4, f'expect {machine1} ping {machine2} {result}, Packets: Received = {count}'
        else:
            assert count == 0 or count == None, f'expect {machine1} ping {machine2} {result}, Packets: Received = {count}'
    else:
        if "host" in machine1.lower():
            context.hosts[machine1].shellcmd.restart_network(context.host_info[machine1]["nic"])
            for i in range(2):
                # retry 2 times
                print(f"this is the {i+1} time!!!")
                r = context.hosts[machine1].shellcmd._ssh.command(
                    cmd=
                    f'ping {machine2} -c 4',
                    exact_prompts='packet loss',
                    timeout=10)
                print(r)
                try:
                    count = int(re.findall(r'(\d+)\s+received', r)[0])
                except:
                    count = None
                if count == 4:
                    break
            if result == "successfully":
                assert count == 4, f'expect {machine1} ping {machine2} {result}, Packets: Received = {count}'
            else:
                assert count == 0 or count == None, f'expect {machine1} ping {machine2} {result}, Packets: Received = {count}'
        elif "dut" in machine1.lower():
            for i in range(2):
                # retry 2 times
                r = context.dut[machine1].main().ping(machine2)
                if int(r['received']) > 0:
                    break
            if result == "successfully":
                assert int(
                    r['received']
                ) == 4, f'expect {machine1} ping {machine2} {result}, Packets: Received = {int(r["received"])}'
            else:
                assert int(
                    r['received']
                ) == 0, f'expect {machine1} ping {machine2} {result}, Packets: Received = {int(r["received"])}'
        else:
            raise Exception("Suppose never goes here. Something wrong!")


def chk_arp(context, host_name=None, dut_name=None):
    if (host_name is None) and (dut_name is None):
        raise Exception("Empty input parameter for ARP check!")
    if host_name:
        context.hosts[host_name].shellcmd._ssh.command(
            cmd='export PATH="/usr/local/sbin:/usr/local/bin:/sbin:'
            '/bin:/usr/sbin:/usr/bin:/root/bin:/usr/local/games:'
            '/usr/games"',
            timeout=10)
        print("--------------check vm {host_name} arp table--------------")
        print(context.hosts[host_name].shellcmd._ssh.command(cmd="arp -n",
                                                        timeout=10))
        print("--------------check vm {host_name} arp table end --------------")
    if dut_name:
        print("--------------check dut {dut_name} arp table--------------")
        print(context.dut[dut_name].main().show_arp())
        print("--------------check dut {dut_name} arp table end --------------")


def clear_arp(context, clear_tgt_ip, host_name=None, dut_name=None):
    print('host_name' + str(host_name))
    if (host_name is None) and (dut_name is None):
        raise Exception("Empty input parameter for ARP check!")
    if host_name:
        print("--------------clear vm {machine1} arp table--------------")
        cmd = f'arp -D {clear_tgt_ip}'
        print(context.hosts[host_name].shellcmd._ssh.command(cmd, timeout=10))
    if dut_name:
        pass


def do_extra_after_ping(context, machine1, machine2, machine2_interface=None):
    '''
    parameter
        machine can be DUT or host(VM)
        there will be 4 combinations (MECE): 
        1. dut -> host 
        2. dut -> dut 
        3. host -> host 
        4. host -> dut 

        Note:
        if machine2 is dut, you need to specify interface for machine2
        e.g.
            "DUT" will ping "DUT WAN" successfully
            "HOST_A" will ping "DUT WAN" successfully
    '''
    if "dut" in machine1.lower() and "host" in machine2.lower():
        pass
    elif "dut" in machine1.lower() and "dut" in machine2.lower():
        pass
    elif "host" in machine1.lower() and "host" in machine2.lower():
        chk_arp(context, host_name=machine1)
    elif "host" in machine1.lower() and "dut" in machine2.lower():
        if machine2_interface:
            if "wan" in machine2_interface.lower():
                clear_arp(context,
                          context.dut_info[machine2]["testbed"]["wan_ip"],
                          host_name=machine1)
            elif "lan" in machine2_interface.lower():
                clear_arp(context,
                          context.dut_info[machine2]["testbed"]["lan_ip"],
                          host_name=machine1)
            elif "brg" in machine2_interface.lower():
                clear_arp(context,
                          context.dut_info[machine2]["testbed"]["brg_ip"],
                          host_name=machine1)
            else:
                raise Exception(
                    f"Non-Supported interface of machine2: {machine2_interface}"
                )
        chk_arp(context, host_name=machine1)
        chk_arp(context, dut_name=machine2)
    else:
        raise Exception(
            f"Suppose never goes here. Something wrong! machine1:{machine1}  machine2:{machine2}  machine2 interface:{machine2_interface}"
        )


@given('"{machine1}" will ping "{machine2}" {result}')
@then('"{machine1}" will ping "{machine2}" {result}')
def step_impl(context, machine1, machine2, result):
    '''
    parameter
        machine can be DUT or host(VM)
        there will be 6 combinations
        1. dut -> host 
        2. dut -> dut 
        3. host -> host 
        4. host -> dut 
        5. host -> any
        6. dut -> any

        Note:
        if machine2 is dut, you need to specify interface for machine2
        e.g.
            "DUT" will ping "DUT WAN" successfully
            "HOST_A" will ping "DUT WAN" successfully
        if you want to ping a specific address or URL, simply replace "machine2" with the desired address or URL.
        e.g.
            "DUT" will ping "google.com" successfully
            "HOST_A" will ping "192.168.127.253" successfully
    table
    '''
    try:
        for row in context.table:
            print('-----------------------------------------------')
            print(f'machine1: {row["device1"]}    machine2: {row["device2"]}')
            print('-----------------------------------------------')
            try:
                if context.dut[row['device1']]:
                    if "host" not in row['device1']:
                        context.dut[row['device1']].close()
                        loginToDUT(context, row['device1'])
                    print(f'{row["device1"]} already opened')
            except:
                if "host" in row['device1']:
                    context.hosts[row['device1']] = HostFactory.create_atb(
                        context.host_info[row['device1']])
                    context.hosts[row['device1']].login()
                    print('context.hosts' + str(context.hosts))
                else:
                    loginToDUT(context, row['device1'])

            do_ping(context, row['device1'], row['device2'], row['result'])
            # In case that machine2 is {DUT interface}, only DUT name is required.
            # extra steps after ping
            device1 = row['device1']
            device2_list = row['device2'].split(' ')
            device2 = device2_list[0]
            if len(device2_list) == 2:
                device2_interface = device2_list[1]
            else:
                device2_interface = None
            do_extra_after_ping(context, device1, device2, device2_interface)
    except:
        do_ping(context, machine1, machine2, result)

@then('{action} user account on "{device}" will {result}')
def step_impl(context, action, device, result):
    for row in context.table:
        if result == "fail":
            try:
                if 'privilege' in context.table.headings:
                    context.dut[device].go_config().set_login_account(
                        action=action,
                        username=row['username'],
                        password=row['password'],
                        privilege=row['privilege'])
                else:
                    context.dut[device].go_config().set_login_account(
                        action=action,
                        username=row['username'],
                        password=row['password'])
            except:
                print("OK! Suppose to catch exception!")
            else:
                assert False, f"{device} should not be able to {action} user account"
        elif result == "succeed":
            print(context.table.headings)
            if 'privilege' in context.table.headings:
                context.dut[device].go_config().set_login_account(
                    action=action,
                    username=row['username'],
                    password=row['password'],
                    privilege=row['privilege'])
            else:
                context.dut[device].go_config().set_login_account(
                    action=action,
                    username=row['username'],
                    password=row['password'])


@when('{action} user account on "{device}"')
def step_impl(context, action, device):
    username = password = privilege = None
    try:
        if context.table[0]['username']:
            username = context.table[0]['username']
        if context.table[0]['password']:
            password = context.table[0]['password']
        if context.table[0]['privilege']:
            privilege = context.table[0]['privilege']
    except:
        pass

    r = context.dut[device].go_config().set_login_account(username=username,
                                                          password=password,
                                                          privilege=privilege,
                                                          action=action)
    print(r)


@given('export "{device}" configuration file to {server}')
@when('export "{device}" configuration file to {server}')
def step_impl(context, device, server):
    ret = context.dut[device].main().export_config(
        tftp_ip=context.host_info["HOST_EXECUTOR"]["testbed"]["cur_host"])
    assert ret['matched'] and '^Parse error' not in ret[
        'data'], f'Configuration Upload Fail: {ret["data"]}'


@given('import {cfg_file} to "{device}" from {server}')
@when('import {cfg_file} to "{device}" from {server}')
def step_impl(context, device, server, cfg_file):
    ret = context.dut[device].main().import_config(
        tftp_ip=context.host_info["HOST_EXECUTOR"]["testbed"]["cur_host"],
        file_name=cfg_file)
    context.dut[device].close()
    assert ret['matched'] and '^Parse error' not in ret[
        'data'], f'Configuration Import Fail: {ret["data"]}'
    login_and_measure_time(context=context, device=device)


@given(
    'upgrade {firmware} to "{device}" from {server} and do warm start automatically on "{device}"'
)
@when(
    'upgrade {firmware} to "{device}" from {server} and do warm start automatically on "{device}"'
)
def step_impl(context, firmware, device, server):
    context.dut[device].main().save()
    ret = context.dut[device].main().upgrade_firmware(
        tftp_ip=context.host_info["HOST_EXECUTOR"]["testbed"]["cur_host"],
        file_name=firmware)
    context.dut[device].close()
    assert ret['matched'] and '^Parse error' not in ret['data']

    login_time = login_and_measure_time(context=context, device=device)
    print(f"Warm Start Time: {context.dut_info[device]['reload_delay']} + {login_time:.2f} seconds")
    time.sleep(10)


@given('get running config from "{device}"')
@when('get running config from "{device}"')
def step_impl(context, device):
    ret = context.dut[device].main().get_running_config(context.dut_info[device]["session"]["con_type"])
    context.running_config = ret.replace(" ", "").replace("\r", "").split('\n')
    context.running_config = list(filter(lambda x: x != '', context.running_config ))
    print("============context.running_config============")
    search_string = "showrunning-config"
    try:
        for index, item in enumerate(context.running_config):
            if search_string in item:
                context.running_config = context.running_config[index+1:]
                break
    except ValueError:
        print("No showrunning-config in running config")
    # if re.search(r'showrunning-config', context.running_config[0]) != None:
    #     context.running_config = context.running_config[1:]
    if re.search(r'[^\n]+[^\)]#', context.running_config[-1]) != None:
        context.running_config = context.running_config[:-1]
    if re.search(r'[^\n]+[^\)]>>', context.running_config[-1]) != None:
        context.running_config = context.running_config[:-1]
    

@then(
    'the comparison between running config and exported config must be the same'
)
def step_impl(context):
    with open('//tftp/test.ini') as f:
        lines = f.read().replace(" ", "").split('\n')[:-1]
    print('config: ', context.running_config)
    print('lines: ', lines)
    for i in range(max(len(context.running_config), len(lines))):
        assert context.running_config[i] == lines[i], \
            f"from line {i} running config is different from ini:\n \
              running config line {i}: {context.running_config[i]},\n\
              ini line {i}: {lines[i]}"


@then(
    '"{host}" tries to establish {ssh_num} ssh and {telnet_num} telnet connection to "{dut_name}"s {dut_itf} but only default {correct_num_of_session} session can be established'
)
@then(
    '"{host}" tries to establish {ssh_num} ssh and {telnet_num} telnet connection to "{dut_name}"s {dut_itf} but only modified {correct_num_of_session} session can be established'
)
def step_impl(context, host, ssh_num, telnet_num, dut_name, dut_itf,
              correct_num_of_session):
    context.dut[dut_name].main().clear_ssh_telnet_limit()

    # quit executor control session
    context.execute_steps(f'''given logout "{dut_name}"''')

    dut_ip = context.dut_info[dut_name]["testbed"][f"{dut_itf.lower()}_ip"]
    dut_account = context.dut_info[dut_name]["credential"]["username"]
    dut_password = context.dut_info[dut_name]["credential"]["password"]

    context.hosts[host].dut_ui.cli_init()
    for i in range(int(ssh_num)):
        context.hosts[host].dut_ui.cli_cmd(
            f'''/bin/bash -c 'sshpass -p {dut_password} ssh -o "StrictHostKeyChecking no" {dut_account}@{dut_ip} >> qqq.log' ''',
            detach=True)
        time.sleep(1)

    for i in range(int(telnet_num)):
        context.hosts[host].dut_ui.cli_cmd(
            f'''/bin/bash -c '(sleep 2; echo "{dut_account}"; sleep 2; echo "{dut_password}"; sleep 2) | telnet {dut_ip} >> qqq.log' ''',
            detach=True)
        time.sleep(3)
    for i in range(2):
        print(f'this is {i} time to cat session log')
        ret = context.hosts[host].dut_ui.cli_cmd("/bin/bash -c 'cat qqq.log'")
        login_symbol = 'MOXA'
        if login_symbol in ret:
            login_count = ret.count(login_symbol)
            break
    assert login_count == int(
        correct_num_of_session), f"Only {login_count} session(s)!"
    context.hosts[host].dut_ui.cli_destroy()

    # regain executor control
    context.execute_steps(f'''given login "{dut_name}" as Admin''')


@when('modify threshold of telnet and ssh connections on "{device}"')
def step_impl(context, device):
    threshold = int(context.table[0]['threshold'])
    context.dut[device].go_config().set_global_telnet(max_login_users=threshold)


@When('warm start on "{device}"')
def step_impl(context, device):
    context.dut[device].main().save()
    context.dut[device].main().reload()
    context.dut[device].close()
    time.sleep(context.dut_info[device]['reload_delay'])
    
    login_time = login_and_measure_time(context=context, device=device)
    print(f"Warm Start Time: {context.dut_info[device]['reload_delay']} + {login_time:.2f} seconds")


@When('cold start on "{device}"')
def step_impl(context, device):
    context.dut[device].main().save()
    if context.dut_info[device]["testbed"]["power_jig_device"] == "ip_power":
        requests.get(
            f'http://{context.dut_info[device]["testbed"]["power_jig_ip"]}/goform/setpower?p6{context.dut_info[device]["testbed"]["power_jig"]}=0',
            auth=HTTPBasicAuth('admin', '12345678'))
        time.sleep(1)
        requests.get(
            f'http://{context.dut_info[device]["testbed"]["power_jig_ip"]}/goform/setpower?p6{context.dut_info[device]["testbed"]["power_jig"]}=1',
            auth=HTTPBasicAuth('admin', '12345678'))
        context.dut[device].close()
        time.sleep(context.dut_info[device]['reload_delay'])
    
        login_time = login_and_measure_time(context=context, device=device)
        print(f"Cold Start Time: {context.dut_info[device]['reload_delay']} + {login_time:.2f} seconds")

    elif context.dut_info[device]["testbed"]["power_jig_device"] == "turtle":
        requests.get(
            f'http://{context.dut_info[device]["testbed"]["power_jig_ip"]}/outlet.cgi?outlet={context.dut_info[device]["testbed"]["power_jig"]}&command=2&time=1679423114457',
            auth=HTTPBasicAuth('admin', ''))
        time.sleep(5)
        requests.get(
            f'http://{context.dut_info[device]["testbed"]["power_jig_ip"]}/outlet.cgi?outlet={context.dut_info[device]["testbed"]["power_jig"]}&command=2&time=1679423114457',
            auth=HTTPBasicAuth('admin', ''))
        context.dut[device].close()
        time.sleep(context.dut_info[device]['reload_delay'])
    
        login_time = login_and_measure_time(context=context, device=device)
        print(f"Cold Start Time: {context.dut_info[device]['reload_delay']} + {login_time:.2f} seconds")
    else:
        raise ValueError(f"Wrong power_jig_device input: {context.dut_info[device]['testbed']['power_jig_device']}")
    


@given(u'set system name to "{name}" on "{device}"')
@when(u'set system name to "{name}" on "{device}"')
def step_impl(context, name, device):
    context.dut[device].go_config().set_hostname(name)


@Given('set default network on "LAN" interface and '
       'rename it as "{name}" on "{device}"')
@when('set default network on "LAN" interface and '
      'rename it as "{name}" on "{device}"')
def step_impl(context, name, device):
    # "DUT-1" set default network on "LAN" interface and rename it as "Lan-127"
    context.dut[device].go_config_if_lan().\
        ip_address_static(context.dut_info[device]['testbed']['lan_ip'], '255.255.255.0')
    context.dut[device].go_config_if_lan().name(name)

    r = context.dut[device].main().show_interface('lan')
    count = 0
    while context.dut_info[device]['testbed']['lan_ip'] not in r[0][
            'ip_address'] and count < 60:
        time.sleep(1)
        r = context.dut[device].main().show_interface('lan')
        count += 1


@Given('{action} trusted access on "{device}"')
@when('{action} trusted access on "{device}"')
def step_impl(context, device, action):
    time.sleep(1)
    context.dut[device].go_config().set_trusted_access(global_toggle=action)


@Given('save configuration into flash on "{device}"')
@when('save configuration into flash on "{device}"')
def step_impl(context, device):
    time.sleep(1)
    context.dut[device].main().save()


@Given('set and enable syslog server with "{host}" ip on "{device}"')
def step_impl(context, host, device):
    context.dut[device].go_config().set_syslog_server(
        'create', context.host_info[host]['testbed']['cur_host'])
    context.dut[device].main().show_logging_event_log_system()


@Given('enable system-event with "{item}" for syslog action on "{device}"')
def step_impl(context, item, device):
    context.dut[device].go_config().set_warning_notification(
        item, action='Syslog only', active=True)


@Given('enable system-event with "{item}" for "{event}" action on "{device}"')
def step_impl(context, item, event, device):
    context.dut[device].go_config().set_warning_notification(
        item, action=event, active=True)


@then('"{device}" record event log "{receive_log}"')
def step_impl(context, device, receive_log):
    logs = context.dut[device].main().show_logging_event_log_system()
    for log in logs:
        if receive_log in log['event']:
            result = 'pass'
            break
        else:
            result = 'fail'
    assert result == 'pass', f'cannot found "{receive_log}" in event log'

@given('connect to "{jig}"')
def step_impl(context, jig):
    print(context.jig_info[jig]["session"])
    context.jig = SessionFactory.create_telnet(context.jig_info[jig]["session"])