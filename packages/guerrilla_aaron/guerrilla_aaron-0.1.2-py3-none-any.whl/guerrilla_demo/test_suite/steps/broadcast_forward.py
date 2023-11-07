from behave import *
import time
from datetime import datetime
import os

@when('{action} broadcast forwarding on "{device}"')
def step_impl(context, action, device):
    context.dut[device].go_config().set_broadcast_forward_status(action = action)


@when('add broadcast forwarding rule on "{device}"')
def step_impl(context, device):
    context.dut[device].go_config().add_broadcast_forward_rule(context.table[0]['In_interface'],
                                                                context.table[0]['Out_interface'],
                                                                context.table[0]['UDP_Port'])
    context.dut[device].main().save()


@when('"{host}" send broadcast packet to its subnet')
def step_impl(context, host):
    sip = context.host_info[host]['testbed']['cur_host']
    ip_parts = sip.split(".")
    ip_parts[3] = "255"
    subnet_ip = ".".join(ip_parts) 
    dip =  subnet_ip
    dport = context.table[0]['dest_port']
    iface = context.host_info[host]['nic']
    script = context.hosts[host].scapy.generate_broadcast_scapy_script(sip, dip, dport, iface, 1)

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
    time.sleep(8)

    context.broadcast_forward = {
        "sip":sip,
        "dip":dip
    }


@then('"{host_recv}" {result} receive broadcast packet from "{host_send}"')
def step_impl(context, host_recv, result, host_send):
    """
    result can be "shall" or "shall not"
    """
    context.hosts[host_recv].tshark.stop()
    ret = context.hosts[host_recv].tshark.retrieve()
    
    if len(ret) == 0:
        raise ValueError('packet receiving fails')

    pkt_count = 0

    ret_lines = ret.split('\n')
    for a in ret_lines:
        arr = a.lstrip(' ').split(' ')
        # skip if not tshark packet
        if arr[0].isdigit() == False:
            continue
        if arr[3] != '→':
            raise ValueError(f'unexpected tshark format {a}')

        # Match Source and Destination IP Address
        if arr[2] == context.broadcast_forward['sip'] and arr[4] == context.broadcast_forward['dip']:
            pkt_count += 1

    if result == 'shall not':
        assert pkt_count == 0, f'{host_recv} expect to receive no packets but receive {pkt_count}'
    elif result == 'shall':
        assert pkt_count > 0, f'{host_recv} expect to receive packets but receive {pkt_count}'