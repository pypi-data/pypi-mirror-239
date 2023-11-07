from host import *
from behave import *
from steps.login import loginToDUT
from steps import common, interface, login


@given(u'import max firewall rule configuration from "{host}" to "{device}"')
def step_impl(context, device, host):
    context.dut[device].main()._s.command_expect(
        command=
        f'copy tftp {context.host_info[host]["testbed"]["cur_host"]} config-file max_firewall.ini',
        prompts=['Config file import successfully.'],
        timeout=60)
    context.dut[device].close()
    loginToDUT(context, device)


@given(u'set virtual interfaces on "{device}" ports')
def step_impl(context, device):
    for row in context.table:
        if row['virtual interfaces'] == 'WAN':
            context.dut[device].go_config().set_vlan_id(
                context.dut_info[device]["testbed"]["wan_vlan"])
            context.dut[device].go_config_if_ethernet(
                f'1/{row["ports"]}').set_switchport(
                    context.dut_info[device]["testbed"]["wan_vlan"])
            context.dut[device].go_config_if_wan().set_wan_interface(
                ip=row["virtual ip"],
                mask="255.255.255.0",
                bind_vlan=row["ports"])
        elif row['virtual interfaces'] == 'BRG':
            context.dut[device].go_config_if_ethernet(f'1/{row["ports"]}'). \
                                set_switchport(context.dut_info[device]["testbed"]["brg_vlan"]) .\
                                set_bridge_group()
            context.dut[device].go_config_bridge().set_brg_interface(
                ip=row["virtual ip"], mask="255.255.255.0")
        else:
            raise ValueError(
                f'input virtual interfaces:{row["virtual interfaces"] } is not exist'
            )


@given(
    u'cycle a maximum number of rules with a set of firewall rules and only sepcified index rule mapping the traffic on "{device}"'
)
def step_impl(context, device):
    '''
        Firewall rule list will be like:
        index 0 deny_ICMP_0 from WAN (128.94)      to LAN (127.93)
        index 1 deny_TCP_1  from LAN (dismatch_ip) to WAN (128.93)
        index 2 deny_UDP_2  from BRG (dismatch_ip) to BRG (126.93)
        .
        .
        .
        index 511 deny_ICMP_511 from WAN (dismatch_ip) to LAN (128.93)
        index 512 deny_TCP_512  from LAN (127.94)      to WAN (128.93)
        .
        .
        .
        index 1022 deny_TCP_1022 from LAN (dismatch_ip) to WAN (128.93)
        index 1023 deny_UDP_1023 from BRG (126.94)      to BRG (126.93)
    '''
    src_ip, dst_ip = {}, {}
    specific_index, protocol, incoming_interface, outgoing_interface, sender, receiver = [], [], [], [], [], []

    # store necessary information for creating the firewall rule
    for row in context.table:
        specific_index.append(row['specified index'])
        protocol.append(row['specific protocols'])
        incoming_interface.append(row['incoming interface'])
        outgoing_interface.append(row['outgoing interface'])
        sender.append(row['sender'])
        receiver.append(row['receiver'])
    print(specific_index, protocol, incoming_interface, outgoing_interface)

    # loop for createing object
    for i in range(3):
        src_ip[incoming_interface[i]] = context.host_info[
            sender[i]]["testbed"][f"{incoming_interface[i].lower()}_host"]
        context.dut[device].go_config_object_addr().create_object(name=f"src_{incoming_interface[i].lower()}", \
                                                                  ip_addr=src_ip[incoming_interface[i]])

        dst_ip[outgoing_interface[i]] = context.host_info[
            receiver[i]]["testbed"][f"{outgoing_interface[i].lower()}_host"]
        context.dut[device].go_config_object_addr().create_object(name=f"dst_{outgoing_interface[i].lower()}", \
                                                                  ip_addr=dst_ip[outgoing_interface[i]])

    context.dut[device].go_config_object_addr().create_object(name=f"dismatch_10", \
                                                              ip_addr=f"10.10.10.99")
    # loop for creating service object
    for p in protocol:
        context.dut[device].go_config_object_serv(p.lower()). \
        command(f"name {p.upper()}")
    context.dut[device].main().command('show object')

    # loop for creating firewall rule
    for i in range(1024):
        if f'{i}' in specific_index:
            index = specific_index.index(f'{i}')
            context.dut[device].go_config().command(f"logging l3l7-policy")
            context.dut[device].go_config_l37policy().set_l37_policy(
                name=f"deny{protocol[index]}_{i}",
                enable=True,
                logging="enable",
                itf={
                    'in': incoming_interface[index].upper(),
                    'out': outgoing_interface[index].upper()
                },
                policy_action="deny",
                mode='ip',
                sip=f"src_{incoming_interface[index].lower()}",
                dip=f"dst_{outgoing_interface[index].lower()}",
                dport=protocol[index].upper())
        else:
            context.dut[device].go_config().command(f"logging l3l7-policy")
            context.dut[device].go_config_l37policy().set_l37_policy(
                name=f"deny{protocol[i%3]}_{i}",
                enable=True,
                logging="enable",
                itf={
                    'in': incoming_interface[i % 3].upper(),
                    'out': outgoing_interface[i % 3].upper()
                },
                policy_action="deny",
                mode='ip',
                sip=f"dismatch_10",
                dip=f"dst_{outgoing_interface[i%3].lower()}",
                dport=protocol[i % 3].upper())
    context.dut[device].main().command('show l3l7-policy')
