import time
from guerrilla_aaron.mdc.router.cli import common_func
from guerrilla_aaron.mdc.router.cli.rp_parser import parser
from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000 import cli
from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000.cli import PROMPT_MAIN

class Main(cli.Cli):
    """
    Class for operating command at main prompt

        Args:
            session (obj): Session object.
            model (str): Model of the device.

        Attributes:
            _s (Session): A Session object used to communicate with the device.
            _model (str): Model of the device.
    """

    def __init__(self, session, model):
        super().__init__(session)
        self._model = model
        self._set_default_prompts()
        self._back_to_main()

    def _set_default_prompts(self):
        self._s.set_default_prompts([PROMPT_MAIN])

    def exit(self):
        self._s.command_expect('exit')

    def ping(self, host):
        return parser.ping(self._s, host, self._model)

    def show_version(self):
        return parser.show_version(self._s, self._model)

    def show_system(self):
        return parser.show_system(self._s, self._model)

    def show_interface(self, name='lan'):
        return parser.show_interface(self._s, name, self._model)

    def show_vlan(self):
        return parser.show_vlan(self._s, self._model)

    def show_clock(self):
        return parser.show_clock(self._s, self._model)

    def reload_factory_default(self):
        common_func.reload_factory_default(self._s)
    
    def reload_factory_default_no_cert(self):
        common_func.reload_factory_default_no_cert(self._s)

    def show_dos(self):
        return parser.show_dos(self._s, self._model)

    def show_ipsec(self, connection_name=None):
        if connection_name is None:
            ret = self._s.command_expect('show ipsec')
        else:
            ret = self._s.command_expect(f'show ipsec {connection_name}')
        return ret['data']

    def show_ipsec_status(self):
        ret = self._s.command_expect('show ipsec status')
        return ret['data']

    def show_ip_route(self):
        return parser.show_ip_route(self._s, self._model)

    # def show_logging_event_log_dos(self):
    #     return parser.show_logging_event_log_dos(self._s, self._model)

    def show_ip_igmp(self):
        return parser.show_ip_igmp(self._s, self._model)

    def show_logging_event_log_firewall(self):
        return parser.show_logging_event_log_firewall(
            self._s, self._model)

    def show_logging_event_log_system(self):
        return parser.show_logging_event_log_system(
            self._s, self._model)

    def show_user_accounts(self):
        return parser.show_user_accounts(self._s, self._model)

    def show_syslog_setting(self):
        self.command('show logging')

    # no parsing required for now
    def show_arp(self):
        self.command('show arp')

    def show_trusted_access(self):
        return parser.show_trusted_access(self._s, self._model)

    def reload(self):
        common_func.reload(self._s)

    def login(self):
        common_func.login(self._s)

    def clear_event_log(self):
        self.set_backdoor()
        self._s.command_expect('cd /mnt/log2', prompts=[r'/mnt/log2 #'])
        self._s.command_expect('cd /mnt/firewall_LOG',
                                prompts=[r'/mnt/firewall_LOG #'])
        self._s.command_expect('rm EDR900_LOG1', prompts=[r'/mnt/log2 #'])
        self._s.command_expect('rm firewall_log', prompts=[r'/mnt/log2 #'])
        self._s.command_expect('exit')
        # disable ctrl-t mode for serial control
        self._s.sendcontrol('t')

    def set_backdoor(self):
        self._s.sendcontrol('t')
        cmd_args = [
            ('ieisecureedr moxaiei89191230', [r'~ #']),
        ]
        for args in cmd_args:
            r = self._s.command_expect(args[0], prompts=args[1])
            if not r['matched']:
                print(f"return = {r}, command = {args[0]}")
                raise Exception("failed to setup backdoor")
        return self

    def clear_ssh_telnet_limit(self):
        '''
        This step may require modification for future usage.
        Due to the DUT's limit on the number of SSH and Telnet sessions, 
        we need to clear the limitation before logging in and out multiple times.
        '''
        self.set_backdoor()
        self._s.command_expect('iptables -F PortScan')
        self._s.command_expect('exit')
        # disable ctrl-t mode for serial control
        self._s.sendcontrol('t')

    def import_config(self,
                        tftp_ip: str = None,
                        usb: bool = False,
                        file_name: str = "test.ini"):
        if tftp_ip != None and usb == False:
            if file_name == 'configuration file':
                return self._s.command_expect(
                    f'copy tftp {tftp_ip} config-file test.ini',
                    prompts=[PROMPT_MAIN],
                    timeout=60)
            else:
                return self._s.command_expect(
                    f'copy tftp {tftp_ip} config-file {file_name}',
                    prompts=[PROMPT_MAIN],
                    timeout=60)
        elif tftp_ip == None and usb == True:
            if file_name == 'configuration file':
                return self._s.command_expect(
                    f'copy usb test.ini',
                    prompts=[PROMPT_MAIN],
                    timeout=60)
            else:
                return self._s.command_expect(
                    f'copy usb {file_name}',
                    prompts=[PROMPT_MAIN],
                    timeout=60)

    def export_config(self, tftp_ip, file_name="test.ini"):
        return self._s.command_expect(
            f'copy running-config tftp {tftp_ip} {file_name}',
            prompts=[PROMPT_MAIN], timeout=60)

    def get_running_config(self, con_type='serial'):
        running_config = ""
        ret = self._s.command_expect('show running-config',
                                        prompts=[PROMPT_MAIN],
                                        timeout=5)
        running_config += ret['data']
        while ret['matched'] == False:
            ret = self._s.command_expect('',
                                            prompts=[PROMPT_MAIN],
                                            timeout=1)
            running_config += ret['data']
        if con_type == 'telnet':
            return ret['data'].replace('\n--More--', '\n')
        else:
            return running_config.replace('\n--More--', '\n')

    def upgrade_firmware(self,
                            tftp_ip,
                            file_name="FWR_TN5916_V3.3_Build_22101415.rom"):
        ret = self._s.command_expect(
            f'copy tftp {tftp_ip} device-firmware {file_name}',
            prompts=['System will reboot now.'],
            timeout=300)
        time.sleep(60)
        return ret

    def save(self):
        return self._s.command_expect('save',
                                        prompts=[PROMPT_MAIN],
                                        exact_str=True,
                                        timeout=30)
    def show_rstp(self):
        """
         Show rstp global information in human readable form. This is useful for debugging purposes.
         
         
            Returns: 
                A string of RLP formatted to be displayed on screen
        """
        return parser.show_rstp(self._s, self._model)

    def show_vrrp(self):
        """
         Show VRRP in human readable form. This is useful for debugging purposes.
         
         
            Returns: 
                A string of RLP formatted to be displayed on screen
        """
        return parser.show_vrrp(self._s, self._model)

    def show_mac_address_table(self):
        """
        Execute the 'show mac-address-table' command on the device.

            Returns:
                str: Output of 'show mac-address-table' command.
        """
        return parser.show_mac_address_table(self._s, self._model)
