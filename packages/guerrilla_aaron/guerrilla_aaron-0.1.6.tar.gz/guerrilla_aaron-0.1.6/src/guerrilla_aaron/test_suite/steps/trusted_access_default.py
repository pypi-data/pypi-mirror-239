from host import *
from behave import *
from steps import login, interface, common
from guerrilla_aaron.mdc.router.cli.rp_base.ng_router.base import Base
from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000.base import Base as tn5000


@when(u'check Trusted Access default setting on "{device}"')
def step_impl(context, device):
    if issubclass(context.dut[device]._model, tn5000):
        ret = context.dut[device].main().show_trusted_access()
        actual_setting = [ \
        ret[0]["accessible_ip_list"], \
        ret[0]["log"], \
        ret[0]["syslog"], \
        ret[0]["trap"], \
        ret[0]["lan"]]

        expect_setting = [ \
        context.table[0]["Accessible IP List"], \
        context.table[0]["Log Enable"], \
        context.table[0]["Syslog"], \
        context.table[0]["Trap"], \
        context.table[0]["LAN"]]

        assert actual_setting == expect_setting, \
        f'Trusted IP List Setting Mismatch: expect {expect_setting} but {actual_setting}'
    elif issubclass(context.dut[device]._model, Base):
        ret = context.dut[device].main().show_trusted_access()
        actual_setting = [ \
        ret[0]["trusted_access_list"], \
        ret[0]["syslog"], \
        ret[0]["trap"], \
        ret[0]["accept_all_lan"]]

        expect_setting = [ \
        context.table[0]["Trusted Access List"], \
        context.table[0]["Syslog"], \
        context.table[0]["Trap"], \
        context.table[0]["Accept All LAN"]]

        assert actual_setting == expect_setting, \
        f'Trusted IP List Setting Mismatch: expect {expect_setting} but {actual_setting}'


@then(u'"{action}" to access "{device}" with "{protocol}" from "{interface}"')
def step_impl(context, action, protocol, interface, device):
    for row in context.table:
        flag = {'success': True, 'fail': False}[row[action]]
        cmd = {
            "HTTP": {
                "LAN":
                    f'curl -I {context.dut_info[device]["testbed"]["lan_ip"]} --connect-timeout 10',
                "WAN":
                    f'curl -I {context.dut_info[device]["testbed"]["wan_ip"]} --connect-timeout 10'
            },
            "HTTPS": {
                "LAN":
                    f'curl -I https://{context.dut_info[device]["testbed"]["lan_ip"]} --connect-timeout 10',
                "WAN":
                    f'curl -I https://{context.dut_info[device]["testbed"]["wan_ip"]} --connect-timeout 10'
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
        }[row['protocol']][row['interface']]
        host = {'WAN': 'HOST_A', 'LAN': 'HOST_B'}[row['interface']]
        print(cmd)
        if flag:
            if row['protocol'] == 'HTTP':
                ret = context.hosts[host].shellcmd._ssh.command(cmd, timeout=5)
                assert any(map(lambda s: s in ret.lower(), \
                               ["http/1.1 200 ok", "http/1.1 308 permanent redirect", "http/1.0 302 redirect"])), \
                                f'[HTTP shall succeed but fail]: ret = {ret}'
            if row['protocol'] == 'HTTPS':
                ret = context.hosts[host].shellcmd._ssh.command(cmd, timeout=5)
                # assert "SSL certificate problem" in ret, f'[HTTPS shall succeed but fail]'
                assert "ssl certificate problem" in ret.lower(), \
                f'[HTTPS shall succeed but fail]: ret = {ret}'
            if row['protocol'] == 'Telnet':
                ret = context.hosts[host].shellcmd._ssh.command(
                    cmd, timeout=5, exact_prompts='login: ')
                context.hosts[host].shellcmd._ssh.sendcontrol('c')
                # assert "Connected" in ret, f'[TELNET shall succeed but fail]'
                assert "connected" in ret.lower(), \
                f'[TELNET shall succeed but fail]: ret = {ret}'
            if row['protocol'] == 'SSH':
                ret = context.hosts[host].shellcmd._ssh.command(cmd,
                                                           timeout=5,
                                                           exact_prompts='password')
                context.hosts[host].shellcmd._ssh.sendcontrol('c')
                # assert ("Password" in ret) or ("RSA key fingerprint" in ret), f'[SSH shall succeed but fail]'
                assert (context.dut_info[device]["testbed"][f"{row['interface'].lower()}_ip"]in ret.lower()) or ("rsa key fingerprint" in ret.lower()), \
                f'[SSH shall succeed but fail]: ret = {ret}'
        else:
            if row['protocol'] == 'HTTP':
                ret = context.hosts[host].shellcmd._ssh.command(cmd, timeout=5)
                # assert (ret == None) or ("HTTP/1.1 200 OK" not in ret), f'[HTTP shall fail but succeed]'
                assert (ret == None) or ("http/1.1 200 OK" not in ret.lower()) or ("http/1.1 308 permanent redirect" in ret.lower()), \
                f'[HTTP shall fail but succeed]: ret = {ret}'
            if row['protocol'] == 'HTTPS':
                ret = context.hosts[host].shellcmd._ssh.command(cmd, timeout=5)
                # assert (ret == None) or "SSL certificate problem" not in ret, f'[HTTPS shall fail but succeed]'
                assert (ret == None) or "ssl certificate problem" not in ret.lower(), \
                f'[HTTPS shall fail but succeed]: ret = {ret}'
            if row['protocol'] == 'Telnet':
                ret = context.hosts[host].shellcmd._ssh.command(
                    cmd, timeout=5, exact_prompts='login: ')
                context.hosts[host].shellcmd._ssh.sendcontrol('c')
                # assert (ret == None) or ("Connected" not in ret), f'ret= {ret}, [TELNET shall fail but succeed]'
                assert (ret == None) or ("connected" not in ret), \
                f'ret= {ret}, [TELNET shall fail but succeed]: ret = {ret}'
            if row['protocol'] == 'SSH':
                ret = context.hosts[host].shellcmd._ssh.command(cmd,
                                                           timeout=5,
                                                           exact_prompts=':')
                context.hosts[host].shellcmd._ssh.sendcontrol('c')
                # assert (ret == None) or ("Password" in ret) or ("RSA key fingerprint?" not in ret), f'ret= {ret}, [SSH shall fail but succeed]'
                assert (ret == None) or ("password" in ret.lower()) or ("rsa key fingerprint?" not in ret.lower()), \
                f'[SSH shall fail but succeed]: ret = {ret}'
