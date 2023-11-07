from guerrilla_aaron.host import *
from behave import *
from guerrilla_aaron.steps import common, interface, login


@when(u'test "{device}"')
def step_impl(context, device):
    pass
    # context.hosts['HOST_EXECUTOR'].shellcmd.show_network()
    # context.hosts['HOST_A'].shellcmd.show_network()
    # context.hosts['HOST_B'].shellcmd.show_network()
    # context.hosts['HOST_B'].shellcmd.unzip_file('qq', 'qq', 'qq')
    # context.hosts['HOST_B'].shellcmd.arp(4, '192.168.127.95')
    # context.hosts['HOST_B'].tcpdump.tcpdump('eth1', 'qq')
    # context.hosts['HOST_B'].tcpdump.get_tcpdumpfile('123')
    # pass
    # context.dut[device].main().set_backdoor(
    #     context.dut_info[device]['credential']['root_account'],
    #     context.dut_info[device]['credential']['root_password'])
    # device = 'DUT'
    # context.execute_steps(f'''given authorize CLI of "{device}"''')
    # context.dut[device].main().show_system()
    # info = context.host_info['HOST_EXECUTOR']
    # context.hosts['HOST_EXECUTOR'] = make_host(info)
    # context.hosts['HOST_EXECUTOR'].login()
    # context.hosts['HOST_EXECUTOR'].tftp.check_env()
    # print(context.dut["DUT"].main().show_dos())
    # print(context.dut["DUT"].main().show_system())
    # print(context.dut["DUT"].main().show_version())
    # print(context.dut["DUT"].main().show_l37_policy())
    # print(context.dut["DUT"].main().show_logging_event_log_dos())
    # print(context.dut["DUT"].main().show_logging_event_log_system())
    # print(context.dut["DUT"].main().show_logging_event_log_l3l7())
    # print(context.dut["DUT"].main().show_interface('lan'))
    # print(context.dut["DUT"].main().show_interface('wan'))
    # print(context.dut["DUT"].main().show_interface('bridge'))
    # print(context.dut["DUT"].main().show_trusted_access())
    # context.dut["DUT"].go_config_ipsec('T1').go_phase1().command('qq')
    # context.dut["DUT"].go_config_ipsec('T1').go_phase2().command('qq')
    # info = context.host_info['HOST']
    # context.host = make_host(info)
    # context.host.login()
    # context.dut["DUT"].go_config().enable_service_dhcp()
    # context.dut["DUT"].go_config().enable_service_dhcp('auto-assign')
    # context.dut["DUT"].go_config_dhcp(1). \
    # network('192.168.127.1', '192.168.127.254', '255.255.255.0'). \
    # lease('1440'). \
    # dns_server('8.8.8.8'). \
    # ntp_server('192.168.127.32'). \
    # default_router('192.168.127.254'). \
    # exit()
    # context.dut["DUT"].go_config_dhcp('qq'). \
    # host('192.168.127.93', '255.255.255.0'). \
    # hardware_address('00:0c:29:49:cd:1e'). \
    # lease('1440'). \
    # dns_server('8.8.8.8'). \
    # ntp_server('192.168.127.32'). \
    # default_router('192.168.127.254'). \
    # exit()

    # context.host.shellcmd.enable_dhcp_client(dev='ens224')
