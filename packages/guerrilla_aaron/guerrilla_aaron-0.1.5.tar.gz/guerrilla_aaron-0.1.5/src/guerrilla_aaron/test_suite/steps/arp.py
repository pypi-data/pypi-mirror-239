import time
import random
from behave import *
from steps import common, interface, login

@when(u'send {pkt_count} arp packet from "{host}" to "{device}"')
def step_impl(context, pkt_count, host, device):
    target_ip = context.dut_info[device]["testbed"]["lan_ip"]
    host_ip = context.host_info[host]["testbed"]["cur_host"]
    connected_port = '1/' + context.host_info[host]["testbed"]["port"]
    vlan_res = context.dut[device].main().show_vlan()
    source_macs = []

    for _ in range(int(pkt_count)):
        mac = [0x00, 0x16, 0x3e,
            random.randint(0x00, 0x7f),
            random.randint(0x00, 0xff),
            random.randint(0x00, 0xff)]
        mac_address = ":".join(f"{x:02x}" for x in mac)
        source_macs.append(mac_address)
    ips = set()
    while len(ips) < int(pkt_count):
        ips.add(f"192.168.{random.randint(0, 255)}.{random.randint(1, 254)}")
    ips = list(ips)

    # fill arp scapy script with args
    script = context.hosts[host].scapy.generate_arp_scapy_script(source_macs, ips, target_ip, context.host_info[host]["nic"])
    from datetime import datetime
    import os

    # write the scapy script to file
    scapy_file_name = datetime.now().isoformat().replace(":", "_")[:19]
    with open(f'../lib/atb/service/scapy_template/{scapy_file_name}', "w") as script_file:
        script_content = script_file.write(script)

    # scp the file to remote host with scapy service
    os.system('sshpass -p "{0}" scp {1} {2}@{3}:~/'.format(context.host_info[host]['session']['credential']['password'],
                                                            f"../lib/atb/service/scapy_template/{scapy_file_name}",
                                                            context.host_info[host]['session']['credential']['username'],
                                                            context.host_info[host]['session']['host']))
    
    context.hosts[host].scapy.do_script(scapy_file_name)
    # Clean up
    os.system(f'rm ../lib/atb/service/scapy_template/{scapy_file_name}')
    context.arp_info = {
        "mac": context.host_info[host]["testbed"]["mac_address"],
        "ip" : ips
    }

    for entry in vlan_res:
        if connected_port in entry['acs_ports'] or entry['trk_ports'] or \
                             entry['hyb_ports'] or entry['brg_ports']:
            vlan = entry['vid']
    
    context.mac_info = {
        "mac": source_macs,
        "vlan": vlan,
        "port": f'1/{context.host_info[host]["testbed"]["port"]}'
    }


@then(u'arp entry should be cleared within the aging time on "{device}"')
def step_impl(context, device):
    ret = context.dut[device].main()._s.command_expect("show arp")
    count = ret["data"].count(context.arp_info["mac"])
    aging_time = 0
    while count >= int(context.table[0]["remove_thershold"]) and \
        aging_time <= int(context.table[0]["aging_time"]):
        time.sleep(10)
        ret = context.dut[device].main()._s.command_expect('show arp')
        count = ret["data"].count(context.arp_info["mac"])
        aging_time += 10

    assert count < int(context.table[0]["remove_thershold"]), \
        f'arp table could not be cleared within the aging time: {ret["data"]}'
    
@then(u'arp entry should be recorded on "{device}"')
def step_impl(context, device):
    arp_table = context.dut[device].main().show_arp()
    for ip in context.arp_info["ip"]:
        flag = False
        for entry in arp_table:
            if ip in entry["address"] and \
                context.arp_info["mac"] in entry["hardware_addr"]:
                flag = True
                break
        assert flag, \
            f'expect-> [mac: {context.arp_info["mac"]}, \
                ip: {ip}\n but {arp_table}'