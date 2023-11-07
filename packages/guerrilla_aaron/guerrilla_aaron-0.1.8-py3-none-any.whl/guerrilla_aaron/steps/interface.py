import time
import ipaddress

from behave import *
from guerrilla_aaron.utils.input_chk import chk_is_private_ip
from guerrilla_aaron.mdc.router.cli.rp_base.ng_router.base import Base
from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000.base import Base as tn5000

'''
    Description:
        To specify DUT interface configuration, add table to the step.
        If table or table header is missing, network configuration is loaded from guerrilla_aaron.topology JSON.

    Example Tables:
        | wan             | mask          | wan_vlan | wan_port | wan_gw        |
        | 192.168.128.254 | 255.255.255.0 | 2        | 8        | 192.168.128.1 |

        | brg             | mask          | brg_vlan | brg_port |
        | 192.168.126.254 | 255.255.255.0 | 4040     | 1,8      |
'''
def get_intf_ip(context, interface, device):
    # Interface IP Address
    if context.table and interface.lower() in context.table.headings:
        dut_iface_ip = context.table[0][interface.lower()]
    else:
        dut_iface_ip = context.dut_info[device]["testbed"][
            f"{interface.lower()}_ip"]
    return dut_iface_ip
def get_intf_port(context, interface, device):
    # Interface Port
    if context.table and f"{interface.lower()}_port" in context.table.headings:
        if interface == 'BRG':
            dut_iface_port = context.table[0][
                f"{interface.lower()}_port"].split(',')
        else:
            dut_iface_port = context.table[0][f"{interface.lower()}_port"]
    else:
        dut_iface_port = context.dut_info[device]["testbed"][
            f"{interface.lower()}_port"]
    return dut_iface_port
def get_intf_vlan(context, interface, device):
    # Interface Vlan
    if context.table and f"{interface.lower()}_vlan" in context.table.headings:
        dut_iface_vlan = context.table[0][f"{interface.lower()}_vlan"]
    else:
        dut_iface_vlan = context.dut_info[device]["testbed"][
            f"{interface.lower()}_vlan"]
    return dut_iface_vlan
def get_intf_mask(context, interface, device):
    # Interface Netmask
    if context.table and "mask" in context.table.headings:
        dut_iface_mask = context.table[0]["mask"]
    else:
        dut_iface_mask = context.dut_info[device]["testbed"]["mask"]
    return dut_iface_mask
def get_intf_gw(context, interface, device):
    # Interface Default GW
    if context.table and f"{interface.lower()}_gw" in context.table.headings:
        dut_iface_gw = context.table[0][f"{interface.lower()}_gw"]
    else:
        dut_iface_gw = None
    return dut_iface_gw
def set_interface(context, interface, device, dut_iface_port, 
                  dut_iface_ip, dut_iface_mask, dut_iface_gw, dut_iface_vlan):
    if interface == 'WAN':
        context.dut[device].go_config().set_vlan_id(dut_iface_vlan)
        context.dut[device].go_config_if_ethernet(
            f'1/{dut_iface_port}').set_switchport(dut_iface_vlan)
        context.dut[device].go_config_if_wan().set_wan_interface(
            ip=dut_iface_ip, mask=dut_iface_mask, bind_vlan=dut_iface_vlan, gateway=dut_iface_gw)
    elif interface == 'LAN':
        if chk_is_private_ip(dut_iface_ip) is False:
            raise ValueError(
                f"The interface IP {dut_iface_ip} on {interface} is not a private IP!"
            )
        context.dut[device].go_config_if_ethernet(
            f'1/{dut_iface_port}').set_switchport(dut_iface_vlan)
        context.dut[device].go_config_if_lan().set_lan_interface(
            ip=dut_iface_ip, mask=dut_iface_mask, bind_vlan=dut_iface_vlan)
        
    elif interface == 'BRG':
        if chk_is_private_ip(dut_iface_ip) is False:
            raise ValueError(
                f"The interface IP {dut_iface_ip} on {interface} is not a private IP!"
            )
        if issubclass(context.dut[device]._model, tn5000):
            context.dut[device].go_config_bridge().set_brg_interface(
                name="BRG", ip=dut_iface_ip, mask=dut_iface_mask)
            for p in dut_iface_port:
                dut_iface_vlan = int(dut_iface_vlan) + int(p)
                context.dut[device].go_config_if_ethernet(f'1/{p}'). \
                                    set_switchport(dut_iface_vlan) .\
                                    set_bridge_group(group=1)
        else:
            context.dut[device].go_config_bridge().set_brg_interface(
                ip=dut_iface_ip, mask=dut_iface_mask)
            for p in dut_iface_port:
                dut_iface_vlan = int(dut_iface_vlan) + int(p)
                context.dut[device].go_config_if_ethernet(f'1/{p}'). \
                                    set_switchport(dut_iface_vlan) .\
                                    set_bridge_group()
    else:
        raise ValueError(f'input interface:{interface} is not exist')
def check_interface(context, interface, device, dut_iface_ip):
    interface_cmd = {
        "wan": "wan",
        "lan": "lan",
        "brg": "bridge"
    }[interface.lower()]
    count = 0
    ret = context.dut[device].main().show_interface(interface_cmd)
    while ret[0]['ip_address'].strip() not in dut_iface_ip.strip(
    ) and count < 60:
        print(ret[0]['ip_address'], dut_iface_ip)

        time.sleep(1)
        count += 1
        ret = context.dut[device].main().show_interface(interface_cmd)

@given(u'set {interface} interface on "{device}" to access internet')
@when(u'set {interface} interface on "{device}" to access internet')
def step_impl(context, interface, device):
    dut_iface_ip = get_intf_ip(context, interface, device)
    dut_iface_vlan = get_intf_vlan(context, interface, device)
    dut_iface_port = context.dut_info[device]["testbed"]["internet_port"]
    dut_iface_mask = get_intf_mask(context, interface, device)
    dut_iface_gw = get_intf_gw(context, interface, device)
    set_interface(context, interface, device, dut_iface_port, 
                  dut_iface_ip, dut_iface_mask, dut_iface_gw, dut_iface_vlan)
    check_interface(context, interface, device, dut_iface_ip)
    
@given(u'set {interface} interface on "{device}" with dhcp mode')
@When(u'set {interface} interface on "{device}" with dhcp mode')
def step_impl(context, interface, device):
    dut_iface_vlan = get_intf_vlan(context, interface, device)
    dut_iface_port = context.dut_info[device]["testbed"]["internet_port"]

    context.dut[device].go_config().set_vlan_id(dut_iface_vlan)
    context.dut[device].go_config_if_ethernet(
            f'1/{dut_iface_port}').set_switchport(dut_iface_vlan)
    context.dut[device].go_config_if_wan().ip_address_dhcp(bind_vlan=dut_iface_vlan)
    for i in range(30):
        time.sleep(1)
        ret = context.dut[device].main().show_interface('wan')
        if '0.0.0.0' not in ret[0]['ip_address']:
            break

@given(u'set {interface} interface on "{device}"')
@When(u'set {interface} interface on "{device}"')
def step_impl(context, interface, device, internet=None):
    dut_iface_ip = get_intf_ip(context, interface, device)
    dut_iface_vlan = get_intf_vlan(context, interface, device)
    dut_iface_port = get_intf_port(context, interface, device)
    dut_iface_mask = get_intf_mask(context, interface, device)
    dut_iface_gw = get_intf_gw(context, interface, device)
    set_interface(context, interface, device, dut_iface_port, 
                  dut_iface_ip, dut_iface_mask, dut_iface_gw, dut_iface_vlan)
    check_interface(context, interface, device, dut_iface_ip)
    
@given(u'set "{host}" ip address within "{device}"s {interface} subnet')
@when(u'set "{host}" ip address within "{device}"s {interface} subnet')
def step_impl(context, interface, host, device):
    # IP Address
    if context.table and interface.lower() in context.table.headings:
        host_testbed_ip = context.table[0][interface.lower()]
    else:
        host_testbed_ip = context.host_info[host]["testbed"][
            f"{interface.lower()}_host"]

    # Subnet Mask
    if context.table and "mask" in context.table.headings:
        host_testbed_mask = context.table[0]["mask"]
    else:
        host_testbed_mask = context.host_info[host]["testbed"]["mask"]

    # Network name (subnet)
    host_testbed_subnet = str(
        ipaddress.ip_network(f'{host_testbed_ip}/{host_testbed_mask}',
                             strict=False)).split('/')[0]

    # Gateway IP
    if context.table and "gateway" in context.table.headings:
        host_testbed_gw = context.table[0]["gateway"]
    else:
        host_testbed_gw = context.host_info[host]["testbed"][
            f"{interface.lower()}_gw"]

    context.host_info[host]["testbed"]["cur_host"] = host_testbed_ip
    context.host_info[host]["testbed"]["cur_subnet"] = host_testbed_subnet
    context.host_info[host]["testbed"]["cur_gw"] = host_testbed_gw

    context.hosts[host].shellcmd.set_network(ip=host_testbed_ip,
                                        mask=host_testbed_mask,
                                        dev=context.host_info[host]['nic'])
    print(context.hosts[host].shellcmd.show_network(dev=context.host_info[host]['nic']))

'''
    Description:
        Since multiple IP addresses are not defined in topology JSON, step table is required.

    Example Table:
        | lan            | mask          |
        | 192.168.127.10 | 255.255.255.0 |
        | 192.168.127.20 | 255.255.255.0 |
        | 192.168.127.30 | 255.255.255.0 |
'''


@given(u'set "{host}" multiple ip address within "{device}"s {interface} subnet'
      )
def step_impl(context, interface, host, device):
    assert context.table is not None

    context.host_info[host]['testbed']['cur_host'] = context.table[0][
        interface.lower()]
    context.host_info[host]["testbed"]["cur_subnet"] = str(
        ipaddress.ip_network(
            f'{context.host_info[host]["testbed"]["cur_host"]}/{context.host_info[host]["testbed"]["mask"]}',
            strict=False)).split('/')[0]
    context.host_info[host]["testbed"]["cur_gw"] = context.host_info[host][
        "testbed"][f"{interface.lower()}_gw"]

    ip_list = []
    mask_list = []
    for if_list in context.table:
        ip_list.append(if_list[interface.lower()])
        mask_list.append(if_list['mask'])

    context.hosts[host].shellcmd.set_networks(ip=ip_list,
                                         mask=mask_list,
                                         dev=context.host_info[host]['nic'])
    print(context.hosts[host].shellcmd.show_network())


@given(u'add static route for "{host1}" routing to "{host2}"')
@when(u'add static route for "{host1}" routing to "{host2}"')
def step_impl(context, host1, host2):
    if context.host_info[host2]["testbed"]["cur_subnet"] != context.host_info[host1]["testbed"]["cur_subnet"]:
        context.hosts[host1].shellcmd.add_route(
            dip=context.host_info[host2]["testbed"]["cur_subnet"],
            mask=context.host_info[host2]["testbed"]["mask"],
            gw=context.host_info[host1]["testbed"]["cur_gw"],
            dev=context.host_info[host1]['nic'])
        print(context.hosts[host1].shellcmd.show_route())


@when(u'add static route for "{host}" with the following rule')
def step_impl(context, host):
    context.hosts[host].shellcmd.add_route(
        dip=context.table[0]["Subnet"],
        mask=context.table[0]["Mask"],
        gw=context.table[0]["Gateway"],
        dev=context.host_info[host]['nic'])
    print(context.hosts[host].shellcmd.show_route())


@When('set network "{port}" on "{itf}" interface binding to VLAN '
      '"{vlan_id}" on "{device}"')
@Given('set network "{port}" on "{itf}" interface binding to VLAN '
       '"{vlan_id}" on "{device}"')
def step_impl(context, port, itf, vlan_id, device):
    context.dut[device].go_config().set_vlan_id(vlan_id)
    if itf == 'WAN':
        if ',' in context.dut_info[device]["testbed"][port]:
            wan_port_list = context.dut_info[device]["testbed"][port].split(',')
        else:
            wan_port_list = [context.dut_info[device]["testbed"][port]]

        for wan_port in wan_port_list:
            context.dut[device].go_config_if_wan().set_wan_interface(
                context.dut_info[device]["testbed"]["wan_ip"],
                context.dut_info[device]["testbed"]["wan_netmask"],
                bind_vlan=vlan_id)
            context.dut[device].go_config_if_ethernet(
                f'1/{wan_port}').set_switchport(vlan_id)

        r = context.dut[device].main().show_interface(itf)
        count = 0

        while context.dut_info[device]["testbed"]["wan_ip"] not in r[0][
                'ip_address'] and count < 60:
            time.sleep(1)

            r = context.dut[device].main().show_interface(itf)

            count += 1

    elif itf == 'LAN':
        context.dut[device].go_config_if_ethernet(
            context.dut_info[device]["testbed"][port]).set_switchport(vlan_id)
        context.dut[device].go_config_if_vlan(vlan_id).set_ip(
            context.dut_info[device]["testbed"]["lan_ip"],
            context.dut_info[device]["testbed"]["lan_netmask"])
        context.dut[device].go_config_if_vlan(vlan_id).set_name(
            f'VLAN-{vlan_id}')

        r = context.dut[device].main().show_interface('vlan', vid=vlan_id)
        count = 0

        while context.dut_info[device]["testbed"]["lan_ip"] not in r[0][
                'ip_address'] and count < 60:
            time.sleep(1)
            r = context.dut[device].main().show_interface('vlan', vid=vlan_id)

            count += 1
