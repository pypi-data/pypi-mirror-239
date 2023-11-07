import time


@then(u'mac entry should be recorded on "{device}"')
def step_impl(context, device):
    # make sure the mac table already update
    for _ in range(10):
        flag = False
        mac_table = context.dut[device].main().show_mac_address_table()
        
        for entry in mac_table:
            entry["mac"] = entry["mac"].replace("-", ":").lower()
            if context.mac_info["mac"][0] in entry["mac"]:
                flag = True
                break
        if flag is True: break
        time.sleep(1)

    # confirm the mac table info is correct or not
    for mac in context.mac_info["mac"]:
        flag = False
        for entry in mac_table:
            entry["mac"] = entry["mac"].replace("-", ":").lower()

            if mac in entry["mac"] and \
                context.mac_info["vlan"] in entry["vlan"] and \
                context.mac_info["port"] in entry["port"]:
                flag = True
                break

        assert flag, \
            f'expect-> [mac: {context.mac_info["mac"]}, \
                port: {context.mac_info["port"]}\n but {mac_table}'


@then(u'mac entry should be cleared within the aging time on "{device}"')
def step_impl(context, device):
    ret = context.dut[device].main()._s.command_expect("show mac-address-table")

    # mac-address-table aging time: 5~300 seconds
    aging_time = context.table[0]["aging_time"]
    context.dut[device].go_config().command(f'mac-address-table aging-time {aging_time}')
    time.sleep(int(aging_time))
    
    flag = True
    for mac in context.mac_info["mac"]:
        if mac in ret["data"]:
            flag = False

    assert flag, \
        f'mac table could not be cleared within the aging time: {ret["data"]}'

    
    