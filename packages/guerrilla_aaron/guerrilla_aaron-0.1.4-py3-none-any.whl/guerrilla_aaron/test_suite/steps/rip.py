import time
import random
from behave import *
from steps import common, interface, login

@when(u'send {pkt_count} rip {rip_type} packet with the content of the table from "{host}" to "{device}"')
def step_impl(context, pkt_count, rip_type, host, device):
    ripentries = []
    for row in context.table:
        row_dict = {}
        for heading, value in row.items():
            if heading == "nexthop":
                row_dict[heading] = context.host_info[host]["testbed"]["cur_host"]
            else:
                row_dict[heading] = value
        ripentries.append(row_dict)
    context.ripentries = ripentries
    
    print(ripentries)
    script = context.hosts[host].scapy.generate_rip_scapy_script(rip_type = rip_type,
                                                                 sip=context.host_info[host]["testbed"]["cur_host"],
                                                                 dip=context.host_info[host]["testbed"]["cur_gw"],
                                                                 smac=context.host_info[host]["testbed"]["mac_address"],
                                                                 dmac="01:00:5E:00:00:09",
                                                                 iface=context.host_info[host]["nic"],
                                                                 ripentries=ripentries 
                                                                )
    from datetime import datetime
    import os

    # write the scapy script to file
    scapy_file_name = datetime.now().isoformat().replace(":", "_")[:19]
    with open(f'../lib/atb/service/scapy_template/{scapy_file_name}', "w") as script_file:
        script_content = script_file.write(script)
    
    os.system('sshpass -p "{0}" scp {1} {2}@{3}:~/'.format(context.host_info[host]['session']['credential']['password'],
                                                            f"../lib/atb/service/scapy_template/{scapy_file_name}",
                                                            context.host_info[host]['session']['credential']['username'],
                                                            context.host_info[host]['session']['host']))
    # Clean up
    for _ in range(int(pkt_count)):
        context.hosts[host].scapy.do_script(scapy_file_name)
    os.system(f'rm ../lib/atb/service/scapy_template/{scapy_file_name}')

@when(u'set rip with below table on "{device}"')
def step_impl(context, device):
    network = context.table[0]["network"].strip().split(",")
    version = context.table[0]["version"]
    redistribute = context.table[0]["redistribute"]
    print("network:", network)
    print("version:", version)
    print("redistribute:", redistribute)
    context.dut[device].go_config_rip().set_rip(network=network, 
                                                version=version, 
                                                redistribute=redistribute
                                                )

@then(u'routing table should be updated with response on "{device}"')
def step_impl(context, device):
    flag = False
    ret = context.dut[device].main().show_ip_route()
    for rip_entry in context.ripentries:
        expect_addr = rip_entry['addr']
        expect_mask = rip_entry['mask']
        expect_nexthop = rip_entry['nexthop']
        expect_metric = str(int(rip_entry['metric']) + 1)

        binary_mask = ''.join(format(int(x), '08b') for x in expect_mask.split('.'))
        expect_mask = str(len(binary_mask.rstrip('0')))
        if any((actual_entry['destination'] == f"{expect_addr}/{expect_mask}" \
               and actual_entry['next_hop'] == expect_nexthop \
               and actual_entry['metric'] == expect_metric) for actual_entry in ret):
            flag = True
    
    assert flag, f"routing rule is not updated ->\n expect: {context.ripentries}\n actual: {ret}"