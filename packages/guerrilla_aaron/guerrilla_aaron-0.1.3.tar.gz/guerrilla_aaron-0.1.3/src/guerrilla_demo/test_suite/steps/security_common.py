import time

from host import *
from behave import *
from steps import common, interface, login


@given('enable telnet service on "{device}"')
@when('enable telnet service on "{device}"')
def step_impl(context, device):
    context.dut[device].go_config().set_global_telnet(port=23)


@when(
    'add and enable rule "{ip}" with "{netmask}" on "{device}" trusted-access list'
)
def step_impl(context, ip, netmask, device):
    context.dut[device].go_config().set_trusted_access(ip=ip,
                                                       mask=netmask,
                                                       action="enable")
    time.sleep(5)

@when(
    'add and enable rule for "{host}" on "{device}" trusted-access list'
)
def step_impl(context, host, device):
    context.dut[device].go_config().set_trusted_access(ip=context.host_info[host]['testbed']['host'],
                                                       mask='255.255.255.0',
                                                       action="enable")
    time.sleep(5)


@when('{action} rule "{ip}" with "{netmask}" on "{device}"')
def step_impl(context, ip, netmask, device, action):
    context.dut[device].go_config().set_trusted_access(ip=ip,
                                                       mask=netmask,
                                                       action=action)
    time.sleep(3)


@then(
    '"{host}" {action} to access "{device}" with "{protocol}" from {interface}')
def step_impl(context, host, action, device, protocol, interface):
    flag = {'success': True, 'fail': False}[action]

    for row in context.table:
        cmd = {
            "HTTP": {
                "LAN":
                    f'curl -m 10 -I {context.dut_info[device]["testbed"]["lan_ip"]} --connect-timeout 10',
                "WAN":
                    f'curl -m 10 -I {context.dut_info[device]["testbed"]["wan_ip"]} --connect-timeout 10'
            },
            "HTTPS": {
                "LAN":
                    f'curl -m 10 -I https://{context.dut_info[device]["testbed"]["lan_ip"]} --connect-timeout 10',
                "WAN":
                    f'curl -m 10 -I https://{context.dut_info[device]["testbed"]["wan_ip"]} --connect-timeout 10'
            },
            "Telnet": {
                "LAN":
                    f'telnet {context.dut_info[device]["testbed"]["lan_ip"]}',
                "WAN":
                    f'telnet {context.dut_info[device]["testbed"]["wan_ip"]}'
            },
            "SSH": {
                "LAN":
                    f'ssh admin@{context.dut_info[device]["testbed"]["lan_ip"]}',
                "WAN":
                    f'ssh admin@{context.dut_info[device]["testbed"]["wan_ip"]}'
            },
        }[row['protocol']][interface]

        print(cmd)

        if flag:
            if row['protocol'] == 'HTTP':
                ret = context.hosts[host].shellcmd._ssh.command(cmd,
                                                           timeout=5).lower()
                assert any(map(lambda s: s in ret.lower(), \
                               ["http/1.1 200 ok", "http/1.1 308 permanent redirect", "http/1.0 302 redirect"])), \
                                f'[HTTP shall succeed but fail]: ret = {ret}'
            if row['protocol'] == 'HTTPS':
                ret = context.hosts[host].shellcmd._ssh.command(cmd,
                                                           timeout=5).lower()
                assert "ssl certificate problem" in ret, \
                f'[HTTPS shall succeed but fail]: {ret}'
            if row['protocol'] == 'Telnet':
                ret = context.hosts[host].shellcmd._ssh.command(
                    cmd, timeout=10, exact_prompts='login: ').lower()
                '''
                if we can access device via telent, the prompt will show "Trying xxx(ip)...
                                                                          Connected to xxx(ip).
                                                                          Escape character is '^]'." 
                then we should use "Ctrl-d" to quit
                '''
                context.hosts[host].shellcmd._ssh.sendcontrol('d')
                assert "connected" in ret, \
                f'[TELNET shall succeed but fail]: {ret}'
            if row['protocol'] == 'SSH':
                ret = context.hosts[host].shellcmd._ssh.command(
                    cmd, timeout=10, exact_prompts='password').lower()
                context.hosts[host].shellcmd._ssh.sendcontrol('c')
                assert (context.dut_info[device]["testbed"][f"{interface.lower()}_ip"] in ret) or ("rsa key fingerprint" in ret), \
                f'[SSH shall succeed but fail]: {ret}'
        else:
            if row['protocol'] == 'HTTP':
                ret = context.hosts[host].shellcmd._ssh.command(cmd, timeout=5)
                assert (ret == None) or ("http/1.1 200 OK" not in ret.lower()) or ("http/1.1 308 permanent redirect" in ret.lower()), \
                f'[HTTP shall fail but succeed]: {ret}'
            if row['protocol'] == 'HTTPS':
                ret = context.hosts[host].shellcmd._ssh.command(cmd, timeout=5)
                assert (ret == None) or "ssl certificate problem" not in ret.lower(), \
                f'[HTTPS shall fail but succeed]: {ret}'
            if row['protocol'] == 'Telnet':
                ret = context.hosts[host].shellcmd._ssh.command(
                    cmd, timeout=5, exact_prompts='login: ')
                '''
                if we cannot access device via telent, the prompt will show "Trying xxx(ip) ..." 
                then we should use "Ctrl-c" to quit
                '''
                context.hosts[host].shellcmd._ssh.sendcontrol('c')
                assert (ret == None) or ("connected" not in ret), \
                f'ret= {ret}, [TELNET shall fail but succeed]: {ret}'
            if row['protocol'] == 'SSH':
                ret = context.hosts[host].shellcmd._ssh.command(cmd,
                                                           timeout=5,
                                                           exact_prompts=':')
                context.hosts[host].shellcmd._ssh.sendcontrol('c')
                assert (ret == None) or ("password" in ret.lower()) or ("rsa key fingerprint?" not in ret.lower()), \
                f'ret= {ret}, [SSH shall fail but succeed]: {ret}'
