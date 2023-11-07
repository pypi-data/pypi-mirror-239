from behave import *


@when('create IP Address and Subnet object with single IP on "{device}"')
def step_impl(context, device):
    context.obj_name = context.table[0]['Name']
    context.obj_addr = context.table[0]['IP Address']
    print(context.obj_name)
    context.dut[device].go_config_object_addr().create_object(
                                                name=context.obj_name,
                                                ip_addr=context.obj_addr)


@when('create IP Address and Subnet object with range IP on "{device}"')
def step_impl(context, device):
    context.obj_name = context.table[0]['Name']
    context.obj_addr = f"{context.table[0]['IP Address1']}-{context.table[0]['IP Address2']}"
    context.dut[device].go_config_object_addr().create_object(
                                                name=context.obj_name,
                                                ip_addr=context.obj_addr)


@when('create IP Address and Subnet object with subnet IP on "{device}"')
def step_impl(context, device):
    context.obj_name = context.table[0]['Name']
    context.obj_addr = f"{context.table[0]['Subnet IP']}/{context.table[0]['Subnet Mask']}"
    context.dut[device].go_config_object_addr().create_object(
                                                name=context.obj_name,
                                                ip_addr=context.obj_addr)


@then('the {IP_type} IP object is successfully created on "{device}"')
def step_impl(context, IP_type, device):
    ret = context.dut[device].main().show_object()
    flag = 0
    for i in ret:
        if i['obejct_name']==context.obj_name and i['detail']==context.obj_addr:
            flag = 1
            break
    assert flag, "the {IP_type} IP object is not created"


@when('create Network Service: "{service_type}" object with name: "{obj_name}" on "{device}"')
def step_impl(context, service_type, obj_name, device):
    context.service_type = service_type
    context.obj_name = obj_name
    context.dut[device].go_config_object_net_serv().create_object(
                                                name=obj_name,
                                                service=[service_type])


@then('the Network Service object is successfully created on "{device}"')
def step_impl(context, device):
    ret = context.dut[device].main().show_object()
    flag = 0
    for i in ret:
        if i['obejct_name']==context.obj_name and i['detail']==context.service_type:
            flag = 1
            break
    assert flag, f"the {context.service_type} object is not created"


@when('create Industrial Application Service: "{service_type}" object with name: "{obj_name}" on "{device}"')
def step_impl(context, service_type, obj_name, device):
    context.service_type = service_type
    context.obj_name = obj_name
    context.dut[device].go_config_object_industrial_app_serv().create_object(
                                                name=obj_name,
                                                service=[service_type])


@then('the Industrial Application Service object is successfully created on "{device}"')
def step_impl(context, device):
    ret = context.dut[device].main().show_object()
    flag = 0
    for i in ret:
        if i['obejct_name']==context.obj_name and i['detail']==context.service_type:
            flag = 1
            break
    assert flag, f"the {context.service_type} object is not created"


@when('create User-defined Service object with name: "{obj_name}" on "{device}"')
def step_impl(context, obj_name, device):
    context.obj_name = obj_name
    if context.table[0]['IP Protocol'] == "TCP" or context.table[0]['IP Protocol'] == "UDP":
        ''' Example:
        | IP Protocol | Service Port |
        | TCP         | any          |
        | TCP         | 22           |
        | TCP         | 22-23        |
        | UDP         | any          |
        | UDP         | 23           |
        | UDP         | 100-101      |
        '''
        if context.table[0]['Service Port']=='any':
            context.obj_detail = context.table[0]['IP Protocol']
        else:
            context.obj_detail = f"{context.table[0]['IP Protocol']} {context.table[0]['Service Port']}"
        context.dut[device].go_config_object_serv(context.table[0]['IP Protocol'].lower()).set_object_serv(
                                                name=obj_name,
                                                port=context.table[0]['Service Port'])
    elif context.table[0]['IP Protocol'] == "TCP and UDP":
        if context.table[0]['Service Port']=='any':
            context.obj_detail = "TCP; UDP"
        else:
            context.obj_detail = f"TCP {context.table[0]['Service Port']}; UDP {context.table[0]['Service Port']}"
        context.dut[device].go_config_object_serv("tcpudp").set_object_serv(
                                                name=obj_name,
                                                port=context.table[0]['Service Port'])
    elif context.table[0]['IP Protocol'] == "ICMP":
        if context.table[0]['ICMP type']=='any' and context.table[0]['ICMP code']=='any':
            context.obj_detail = "ICMP Type Any Code Any"
        else:
            context.obj_detail = f"ICMP Type {context.table[0]['ICMP type']} Code {context.table[0]['ICMP code']}"
        context.dut[device].go_config_object_serv("icmp").set_object_serv(
                                                name=obj_name,
                                                icmp_type=context.table[0]['ICMP type'],
                                                icmp_code=context.table[0]['ICMP code'])
    elif context.table[0]['IP Protocol'] == "Custom":
        context.obj_detail = f"IP Protocol {context.table[0]['Service Port']}"
        context.dut[device].go_config_object_serv("ipproto").set_object_serv(
                                                name=obj_name,
                                                ipproto=context.table[0]['Service Port'])


@then('the User-defined Service object is successfully created on "{device}"')
def step_impl(context, device):
    ret = context.dut[device].main().show_object()
    flag = 0
    for i in ret:
        if i['obejct_name']==context.obj_name and i['detail']==context.obj_detail:
            flag = 1
            break
    assert flag, f"the {context.obj_detail} object is not created"