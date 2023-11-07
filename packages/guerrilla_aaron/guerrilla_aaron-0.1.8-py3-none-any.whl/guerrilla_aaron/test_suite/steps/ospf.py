import time

@when(u'run ospf service on "{host}"')
def step_impl(context, host):
    intf = context.host_info[host]["nic"]
    area_id = context.table[0]["area_id"]
    priority = int(context.table[0]["priority"])
    hello_interval = int(context.table[0]["hello_interval"])
    dead_interval = int(context.table[0]["dead_interval"])
    router_id = context.host_info[host]["testbed"]["cur_host"]
    context.hosts[host].bird.set_ospf_config(router_id = router_id,
                                             intf = intf, 
                                             area_id = area_id,
                                             priority = priority,
                                             hello_interval = hello_interval, 
                                             dead_interval = dead_interval)
    context.hosts[host].bird.start()
    context.ospf_host = host

@when(u'set ospf config on "{device}" {intf}')
def step_impl(context, device, intf):
    area_id = context.table[0]["area_id"]
    priority = int(context.table[0]["priority"])
    hello_interval = int(context.table[0]["hello_interval"])
    dead_interval = int(context.table[0]["dead_interval"])
    router_id = context.dut_info[device]["testbed"]["wan_ip"]
    redistribute = None if context.table[0]["redistribute"] == "disable" \
        else context.table[0]["redistribute"]
    context.dut[device].go_config_ospf(router_id).set_ospf_area(area_id=area_id)
    context.dut[device].go_config_ospf(router_id).set_ospf_intf(intf=intf,
                                                                area_id=area_id,
                                                                priority=priority,
                                                                hello_interval=hello_interval,
                                                                dead_interval=dead_interval)
    context.dut[device].go_config_ospf(router_id).set_ospf_redistribute(redistribute)
    
@then(u'ospf should be "{state}" on "{device}" {intf}')
def step_impl(context, state, device, intf):
    ret = context.dut[device].main().show_ip_ospf_interface()
    flag = False
    for _ in range(12):
        if ret[0]["state"] == state:
            flag = True
            break
        ret = context.dut[device].main().show_ip_ospf_interface()
    context.hosts[context.ospf_host].bird.clean_up()
    assert flag, f'ospf act as wrong state on {device}: expect {state} but actual {ret["state"]}'

@then(u'ospf neighbor {action} contain "{host}" on "{device}"')
def step_impl(context, host, action, device):
    ret = context.dut[device].main().show_ip_ospf_neighbor()
    flag = False
    for _ in range(12):
        try:
            ret = context.dut[device].main().show_ip_ospf_neighbor()
            if context.host_info[host]["testbed"]["cur_host"] in ret[0]["neighbor_id"] \
                and "2-Way" not in ret[0]["state"]:
                flag = True
                break
        except:
            print(f"no any ospf neighbor on {device}")
    context.hosts[context.ospf_host].bird.clean_up()
    assert flag if action == "should" else not flag, \
    f'ospf neighbor {action} have {context.host_info[host]["testbed"]["cur_host"]} on {device} but {ret}'

@then(u'ospf database {action} have ospf information from "{device}"s {intf}')
def step_impl(context, action, device, intf):
    import ipaddress
    def get_subnet(ip, mask):
        # Convert IP and mask to IPv4Address and IPv4Network objects
        ip_obj = ipaddress.IPv4Address(ip)
        network_obj = ipaddress.IPv4Network(f"{ip}/{mask}", strict=False)
        
        # Return the network address of the subnet
        return str(network_obj.network_address)
    def mask_to_cidr(mask):
        # Split the mask into octets and convert each octet to binary
        binary_mask = ''.join([bin(int(octet))[2:].zfill(8) for octet in mask.split('.')])
        
        # Count the number of '1' bits in the binary representation
        return binary_mask.count('1')
    ret = context.dut[device].main().show_ip_ospf_database()
    subnet = get_subnet(context.dut_info[device]["testbed"][f"{intf.lower()}_ip"], 
                        context.dut_info[device]["testbed"][f"{intf.lower()}_netmask"])
    mask = mask_to_cidr(context.dut_info[device]["testbed"][f"{intf.lower()}_netmask"])
    flag = False
    print(subnet, mask, context.dut_info[device]["testbed"]["wan_ip"] )
    for _ in range(12):
        try:
            ret = context.dut[device].main().show_ip_ospf_database()
            if subnet in ret[0]["link_state_id"] and \
               context.dut_info[device]["testbed"]["wan_ip"] in ret[0]["adv_router"] and \
               f'{subnet}/{mask}' in ret[0]["router"] and \
                "AS-external" in ret[0]["ls_type"]:
                flag = True
                break
        except:
            print(f"no any external route on ospf database")
    context.hosts[context.ospf_host].bird.clean_up()
    assert flag if action == "should" else not flag, \
        f'ospf database should have external route but {ret}'
    
@then(u'"{host}" should receive Type 3 Summary LSAs')
def step_impl(context, host):
    context.hosts[host].tshark.capture_by_number(interface='eth1',
                                                 number = 5,
                                                 timeout = 60,
                                                 capture_filter = f'ip proto 89 and src host 192.168.128.254 and ip[21] = 4',
                                                 additional_options = "-O ospf")
    context.hosts[host].tshark.stop()
    rcv_pkt = context.hosts[host].tshark.retrieve()
    print(rcv_pkt)

    assert "LSA-type 3 (Summary-LSA (IP network))" in rcv_pkt, \
    f"packets with [LSA-type 3] are not existed"