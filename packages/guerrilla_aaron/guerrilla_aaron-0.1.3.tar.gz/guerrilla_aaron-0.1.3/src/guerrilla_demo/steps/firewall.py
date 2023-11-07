import time

from behave import *
from mdc.router.cli.rp_base.ng_router.base import Base
from mdc.router.cli.rp_base.lg_router.tn5000.base import Base as tn5000

@when('{action} global firewall rule on "{device}"')
@given('{action} global firewall rule on "{device}"')
def step_impl(context, device, action):
    '''
    action: enable/disable
    '''
    context.dut[device].go_config().set_global_l3l7_policy(global_action=action).\
                                        set_global_l3l7_policy(default_action="allow")
    if action == "enable":
        time.sleep(10)


def set_firewall_rule(context, specific_protocols, specified_filter_mode,
                      in_itf, out_itf, host1, host2, device, model):
    if issubclass(model, tn5000):
        # get policy information
        src_ip = context.host_info[host1]['testbed']['cur_host']
        dst_ip = context.host_info[host2]['testbed']['cur_host']
        src_mac = context.host_info[host1]['testbed']['mac_address']

        if src_ip == "":
            src_ip = context.host_info[host1]['testbed'][
                f'{in_itf.lower()}_host']
        if dst_ip == "":
            dst_ip = context.host_info[host2]['testbed'][
                f'{out_itf.lower()}_host']
        print(f'{host1}: {src_ip}')
        print(f'{host2}: {dst_ip}')
        # set firewall log
        context.dut[device].go_config().set_log("firewall")
        # set filter mode
        mode = {
            "IP and Port Filtering": "ip",
            "Source MAC": "mac"
        }[specified_filter_mode]
        print("\nMode:", specified_filter_mode)

        # set firewall policy
        if mode == "ip":
            context.dut[device].go_config_firewall(1).set_firewall_policy(
                action="drop",
                mode=mode,
                protocol=specific_protocols.upper(),
                itf={
                    'in': in_itf.upper(),
                    'out': out_itf.upper()
                },
                sip=src_ip,
                dip=dst_ip,
                enable_log=["flash"])

        elif mode == "mac":
            print("Source Mac:", src_mac)
            context.dut[device].go_config_firewall(1).set_firewall_policy(
                action="drop",
                mode=mode,
                protocol=specific_protocols.upper(),
                itf={
                    'in': in_itf.upper(),
                    'out': out_itf.upper()
                },
                smac=src_mac,
                enable_log=["flash"])

    elif issubclass(model, Base):
        # set object...
        # set l37policy...
        src_ip = context.host_info[host1]['testbed']['cur_host']
        dst_ip = context.host_info[host2]['testbed']['cur_host']
        if src_ip == "":
            src_ip = context.host_info[host1]['testbed'][
                f'{in_itf.lower()}_host']
        if dst_ip == "":
            dst_ip = context.host_info[host2]['testbed'][
                f'{out_itf.lower()}_host']
        print(f'{host1}: {src_ip}')
        print(f'{host2}: {dst_ip}')

        context.dut[device].go_config_object_addr().create_object(
            name=f"src_ip_{src_ip.split('.')[2]}", ip_addr=src_ip)
        context.dut[device].go_config_object_addr().create_object(
            name=f"dst_ip_{dst_ip.split('.')[2]}", ip_addr=dst_ip)

        context.dut[device].go_config_object_serv(specific_protocols.lower()). \
                            set_object_serv(name=specific_protocols.upper())

        mode = {
            "IP and Port Filtering": "ip",
            "IP and Source MAC": "ip-mac",
            "Source MAC": "mac"
        }[specified_filter_mode]
        mode_rule = {
            "IP and Port Filtering": "IP/Port Filtering",
            "IP and Source MAC": "IP/Source Source MAC",
            "Source MAC": "Source MAC"
        }[specified_filter_mode]

        print("mode", mode)
        print("mode_rule", mode_rule)
        print("src_mac", context.dut_info[device]['mac_address'])

        if in_itf.upper() == 'BRG':
            in_itf = f'{in_itf}_LAN'
        if out_itf.upper() == 'BRG':
            out_itf = f'{out_itf}_LAN'
        if mode == "ip":
            context.dut[device].go_config().set_log(log_item="l3l7-policy")
            context.dut[device].go_config_l37policy().set_l37_policy(
                name=f"deny_{specific_protocols}_{mode}",
                enable=True,
                logging="enable",
                itf={
                    'in': in_itf.upper(),
                    'out': out_itf.upper()
                },
                policy_action="deny",
                mode=mode,
                sip=f"src_ip_{src_ip.split('.')[2]}",
                dip=f"dst_ip_{dst_ip.split('.')[2]}",
                dport=specific_protocols.upper())
            r = context.dut[device].main().show_l37_policy()
            rule_setting = [
                r[0]['incoming_interface'], r[0]['outgoing_interface'],
                r[0]['source_ip_address'], r[0]['destination_ip_address'],
                r[0]['destination_port_or_protocol'], r[0]['filter_mode'],
                r[0]['action'], r[0]['log']
            ]
            rule_expect = [
                in_itf.upper(),
                out_itf.upper(), f"src_ip_{src_ip.split('.')[2]}",
                f"dst_ip_{dst_ip.split('.')[2]}",
                specific_protocols.upper(), f"{mode_rule}", 'Deny', 'Enable'
            ]
            assert rule_setting == rule_expect, \
            f'polic setting dismatch: expect "{rule_expect}" but "{rule_setting}"'

        elif mode == "ip-mac":
            context.dut[device].go_config().set_log(log_item="l3l7-policy")
            context.dut[device].go_config_l37policy().set_l37_policy(
                name=f"deny_{specific_protocols}_{mode}",
                enable=True,
                logging="enable",
                itf={
                    'in': in_itf.upper(),
                    'out': out_itf.upper()
                },
                policy_action="deny",
                mode=mode,
                sip=f"src_ip_{src_ip.split('.')[2]}",
                smac=context.host_info[host1]['testbed']['mac_address'])
            r = context.dut[device].main().show_l37_policy()
            print(r)

        elif mode == "mac":
            context.dut[device].go_config().set_log(log_item="l3l7-policy")
            context.dut[device].go_config_l37policy().set_l37_policy(
                name=f"deny_{specific_protocols}_{mode}",
                enable=True,
                logging="enable",
                itf={
                    'in': in_itf.upper(),
                    'out': out_itf.upper()
                },
                policy_action="deny",
                mode=mode,
                smac=context.host_info[host1]['testbed']['mac_address'])
            r = context.dut[device].main().show_l37_policy()
            print(r)


@given(
    u'set a firewall rule on "{device}" to deny {specific_protocols} and "{specified_filter_mode}" from {in_itf} ("{host1}") to {out_itf} ("{host2}") and enable logging flash'
)
@when(
    u'set a firewall rule on "{device}" to deny {specific_protocols} and "{specified_filter_mode}" from {in_itf} ("{host1}") to {out_itf} ("{host2}") and enable logging flash'
)
def step_impl(context, specific_protocols, specified_filter_mode, in_itf,
              out_itf, host1, host2, device):
    set_firewall_rule(context, specific_protocols, specified_filter_mode,
                      in_itf, out_itf, host1, host2, device,
                      context.dut[device]._model)


@when(u'{status} the firewall rule with index {index} on "{device}"')
@given(u'{status} the firewall rule with index {index} on "{device}"')
def step_impl(context, device, index, status):
    '''
    status: enable/disable
    '''
    if issubclass(context.dut[device]._model, tn5000):
        context.dut[device].go_config().set_firewall_rule_status(
            context, index, status)
    elif issubclass(context.dut[device]._model, Base):
        context.dut[device].go_config().set_l37_rule_status(
            context, index, status)


def show_logging_event_log_firewall(context, device, model):
    if issubclass(model, tn5000):
        ret = context.dut[device].main().show_logging_event_log_firewall()
    else:
        ret = context.dut[device].main().show_logging_event_log_l3l7()
    return ret


@then(
    u'"{device}" can record firewall logs block {specific_protocols} traffic from {in_itf} ("{host1}") to {out_itf} ("{host2}")'
)
def step_impl(context, device, specific_protocols, in_itf, host1, out_itf,
              host2):
    ret = show_logging_event_log_firewall(context, device,
                                          context.dut[device]._model)
    count = 0
    if in_itf.upper() == 'BRG' and out_itf.upper() == 'BRG':
        in_itf, out_itf = 'BRG_LAN', 'BRG_LAN'

    if issubclass(context.dut[device]._model, tn5000):
        log_expect = [specific_protocols.upper(), in_itf.upper(), context.host_info[host1]['testbed']['cur_host'], out_itf.upper(), \
             context.host_info[host2]['testbed']['cur_host'], 'DROP']
    else:
        log_expect = [specific_protocols.upper(), in_itf.upper(), context.host_info[host1]['testbed']['cur_host'], out_itf.upper(), \
             context.host_info[host2]['testbed']['cur_host'], 'Deny']
    for r in ret:
        log_actual = [
            r['protocol'], r['in'], r['src_ip'], r['out'], r['dest_ip'],
            r['action']
        ]
        if log_expect == log_actual:
            count += 1
    if count == 0:
        assert False, '0 message lines logged'
    if specific_protocols.upper() == 'ICMP':
        assert count == 1, f'logged event-log dismatch: expect 1 but {count}, {log_expect} <-> {log_actual}'
    else:
        assert count >= 1, f'logged event-log dismatch: expect 4 but {count}, {log_expect} <-> {log_actual}'


@when(u'send traffic with {specific_protocols} from "{host1}" to "{host2}"')
def step_impl(context, specific_protocols, host1, host2):
    context.hosts[host2].tshark.start(interface=context.host_info[host2]['nic'])
    time.sleep(5)
    print(
        f'send traffic: {context.host_info[host1]["testbed"]["cur_host"]} {context.host_info[host2]["testbed"]["cur_host"]}'
    )
    context.hosts[host1].hping3.send( \
        tcpudp_flags=[specific_protocols.lower()], \
        host = context.host_info[host2]['testbed']['cur_host'], \
        count = 4)
    time.sleep(5)


@then(
    u'"{host1}" {can_or_cannot} receive traffic with {specific_protocols} from "{host2}"'
)
@then(
    u'check if "{host1}" {can_or_cannot} receive traffic with {specific_protocols} from "{host2}"'
)
def step_impl(context, host1, can_or_cannot, specific_protocols, host2):
    # ['ICMP' , 'Flags [S]', 'UDP']
    flag = { \
        'can': True, \
        'cannot': False}[can_or_cannot]
    context.hosts[host1].tshark.stop()
    ret = context.hosts[host1].tshark.retrieve()
    print(ret)
    count = 0
    if ret != None:
        print(
            f'{context.host_info[host2]["testbed"]["cur_host"]} → {context.host_info[host1]["testbed"]["cur_host"]} {specific_protocols.upper()}'
        )
        count = ret.count(
            f'{context.host_info[host2]["testbed"]["cur_host"]} → {context.host_info[host1]["testbed"]["cur_host"]} {specific_protocols.upper()}'
        )
    if flag:
        assert count >= 1 , \
        f'expect receive 4 number of {specific_protocols.upper()} but {count}, {ret}'
    else:
        assert count == 0, \
        f'expect receive 0 number of {specific_protocols.upper()} but {count}, {ret}'
