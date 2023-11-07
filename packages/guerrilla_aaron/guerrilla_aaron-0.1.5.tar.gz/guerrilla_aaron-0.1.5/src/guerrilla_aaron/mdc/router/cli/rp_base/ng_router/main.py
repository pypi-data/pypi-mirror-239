from mdc.router.cli import common_func
from mdc.router.cli.rp_parser import parser
from mdc.router.cli.rp_base.ng_router import cli
from mdc.router.cli.rp_base.ng_router.cli import PROMPT_MAIN

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

    def __init__(self, session: object, model: str):
        super().__init__(session)
        self._model = model
        self._set_default_prompts()
        self._back_to_main()

    def _set_default_prompts(self):
        """
        Set default prompts for the session.
        """
        self._s.set_default_prompts([PROMPT_MAIN])

    def exit(self):
        """
        Exit from the current session.
        """
        self._s.command_expect('exit')

    def ping(self, host: str):
        """
        Ping a given host from the device.

            Args: 
                host (str): Host to be pinged.

            Returns: 
                str: Output of ping command. 
        """
        return parser.ping(self._s, host, self._model)

    def show_version(self):
        """
        Returns the version of the device.
            
            Returns:
                str: The version of the device.
        """
        return parser.show_version(self._s, self._model)

    def show_package(self):
        """
        Returns the package installed on the device.

            Returns:
                str: The package installed on the device. 
        """
        return parser.show_package(self._s, self._model)

    def show_system(self):
        """
        Returns information about system configuration on the device.

            Returns: 
                str: Information about system configuration on the device. 
        """
        return parser.show_system(self._s, self._model)

    def show_interface(self, name: str = 'lan'):
        """
        Returns information about interface configuration on the device for given name or lan by default if no name is provided .

            Args: 
                name (str, optional): Name of interface to get information about it's configuration . Defaults to 'lan'. 

            Returns:
                str: Information about interface configuration on the device for given name or lan by default if no name is provided .   #name is optional parameter with default value 'lan'  
        """
        return parser.show_interface(self._s, name, self._model)

    def show_vlan(self):
        """
        Show VLAN information on the device.

            Returns:
                dict: A dictionary containing the VLAN information.
        """
        return parser.show_vlan(self._s, self._model)

    def show_clock(self):
        """
        Show clock information on the device.

            Returns:
                dict: A dictionary containing the clock information. 
        """
        return parser.show_clock(self._s, self._model)

    def reload_factory_default(self):
        """
        Reloads the device to factory default settings.
        """
        common_func.reload_factory_default(self._s)

    def reload_factory_default_no_cert(self):
        common_func.reload_factory_default_no_cert(self._s)
        
    def show_dos(self):
        """
        Shows the Denial of Service (DoS) settings on the device.

            Returns: 
                str: The DoS settings on the device. 
        """
        return parser.show_dos(self._s, self._model)

    def show_ip_route(self):
        """
        Shows the IP routing table on the device.

            Returns: 
                dict: The IP routing table on the device.  
        """
        return parser.show_ip_route(self._s, self._model)

    def show_ip_igmp(self):
        """
        Shows the IP IGMP table on the device.

            Returns: 
                dict: The IP IGMP table on the device.  
        """
        return parser.show_ip_igmp(self._s, self._model)

    def show_logging_event_log_dos(self):
        """
        Shows logging event log for DoS attacks on the device.

            Returns:  
                dict: Logging event log for DoS attacks on the device.  
        """
        return parser.show_logging_event_log_dos(self._s, self._model)

    def show_logging_event_log_l3l7(self):
        """
        Retrieve the L3/L7 event log from the device.

            Returns:
                dict: L3/L7 event log.
        """
        return parser.show_logging_event_log_l3l7(self._s, self._model)

    def show_logging_event_log_system(self):
        """
        Retrieve the system event log from the device.

            Returns:
                dict: System event log. 
        """
        return parser.show_logging_event_log_system(
            self._s, self._model)

    def show_logging_event_log_malformed(self):
        """
        Retrieve the malformed event log from the device.

            Returns:
                dict: malformed event log.
        """
        return parser.show_logging_event_log_malformed(
            self._s, self._model)

    def show_l37_policy(self):
        """
        Retrieve the L3/L7 policy from the device.

            Returns: 
                dict: L3/L7 policy. 
        """
        return parser.show_l37_policy(self._s, self._model)

    def show_user_accounts(self):
        """
        Retrieve user accounts from the device. 

            Returns: 
                dict: User accounts and their settings. 
        """
        return parser.show_user_accounts(self._s, self._model)

    def show_syslog_setting(self):
        """
        Show syslog setting on the device. 

            Returns: None, command is executed on device without parsing output for now. 

        """
        self.command('show logging')

    # no parsing required for now
    def show_arp(self):
        """
        Execute the 'show arp' command on the device.

            Returns:
                str: Output of 'show arp' command.
        """
        return parser.show_arp(self._s, self._model)

    def show_mac_address_table(self):
        """
        Execute the 'show mac-address-table' command on the device.

            Returns:
                str: Output of 'show mac-address-table' command.
        """
        return parser.show_mac_address_table(self._s, self._model)

    def show_trusted_access(self):
        """
        Show trusted access information on the device.

            Returns:
                str: Output of 'show trusted access' command. 
        """
        return parser.show_trusted_access(self._s, self._model)

    def show_vrrp(self):
        """
         Show VRRP in human readable form. This is useful for debugging purposes.
         
         
            Returns: 
                A string of RLP formatted to be displayed on screen
        """
        return parser.show_vrrp(self._s, self._model)

    def show_rstp(self):
        """
         Show rstp global information in human readable form. This is useful for debugging purposes.
         
         
            Returns: 
                A string of RLP formatted to be displayed on screen
        """
        return parser.show_rstp(self._s, self._model)
    
    def show_rstp_port(self):
        """
         Show rstp port status in human readable form. This is useful for debugging purposes.
         
         
            Returns: 
                A string of RLP formatted to be displayed on screen
        """
        return parser.show_rstp_port(self._s, self._model)
    
    def show_ip_ospf_interface(self):
        """
         Show ospf interface in human readable form. This is useful for debugging purposes.
         
         
            Returns: 
                A string of RLP formatted to be displayed on screen
        """
        return parser.show_ip_ospf_interface(self._s, self._model)
    
    def show_ip_ospf_neighbor(self):
        """
         Show ospf neighbor in human readable form. This is useful for debugging purposes.
         
         
            Returns: 
                A string of RLP formatted to be displayed on screen
        """
        return parser.show_ip_ospf_neighbor(self._s, self._model)
    
    def show_ip_ospf_database(self):
        """
         Show ospf database in human readable form. This is useful for debugging purposes.
         
         
            Returns: 
                A string of RLP formatted to be displayed on screen
        """
        return parser.show_ip_ospf_database(self._s, self._model)

    def reload(self):
        """
        Reload the device with current configuration.
        """
        common_func.reload(self._s)

    def login(self):
        """
        Login to the device with credentials provided in constructor.
        """
        common_func.login(self._s)

    def clear(self,
                event_log: str = None,
                security_notification: str = None):
        """
        Clear the event log or security notification status. 
            Args: 
                event_log (str): The type of event log to clear. Valid values are: "all", "vpn", "system", "trusted-access", "malformed", "dos", "l3l7-policy", "dpi", "adp", "ips" and "session-control". 
                security_notification (str): The type of security notification to clear. 
            Raises: 
                ValueError: If the input event log type is invalid. 
        """
        log_type = [
            "all", "vpn", "system", "trusted-access", "malformed", "dos",
            "l3l7-policy", "dpi", "adp", "ips", "session-control"
        ]
        if event_log != None:
            if event_log in log_type:
                if event_log == "all":
                    self._s.command_expect('clear logging event-log')
                else:
                    self._s.command_expect(
                        f'clear logging event-log {event_log}')
            else:
                raise ValueError(
                    f'input invalid event log type: {event_log}')
        elif security_notification != None:
            self._s.command_expect('clear security-notification status')

    def set_backdoor(self):
        """
        Set up a backdoor for the device.  
            Raises: 
                Exception: If failed to setup backdoor.
        """
        self._s.sendcontrol('t')
        cmd_args = [
            ('ieisecureedr moxaiei89191230', [r'/ #']),
            ('passwd -ud root', [r'/ #']),
            # ('exit', [PROMPT_MAIN]),
            # ('exit', [PROMPT_MAIN]),
        ]
        for args in cmd_args:
            r = self._s.command_expect(args[0], prompts=args[1])
            if not r['matched']:
                print(f"return = {r}, command = {args[0]}")
                raise Exception("failed to setup backdoor")
        return self

    def clear_ssh_telnet_limit(self):
        """
        This step may require modification for future usage.
        Due to the DUT's limit on the number of SSH and Telnet sessions, 
        we need to clear the limitation before logging in and out multiple times.
        """
        self.set_backdoor()
        self._s.command_expect('iptables -F PortScan')
        self._s.command_expect('exit')
        # disable ctrl-t mode for serial control
        self._s.sendcontrol('t')

    def import_config(self,
                        tftp_ip: str = None,
                        usb: bool = False,
                        file_name: str = "test.ini"):
        """
        Import a configuration file from a TFTP server or USB.

            Args:
                tftp_ip (str): The IP address of the TFTP server.
                file_name (str, optional): The name of the configuration file to import. Defaults to "test.ini".

            Returns:
                str: A string indicating whether the config file was imported successfully or not. 
        """
        if tftp_ip != None and usb == False:
            if file_name == 'configuration file':
                return self._s.command_expect(
                    f'copy tftp {tftp_ip} config-file test.ini',
                    prompts=['Config file import successfully'],
                    timeout=25)
            else:
                return self._s.command_expect(
                    f'copy tftp {tftp_ip} config-file {file_name}',
                    prompts=['Config file import successfully'],
                    timeout=25)
        elif tftp_ip == None and usb == True:
            if file_name == 'configuration file':
                return self._s.command_expect(
                    f'copy usb test.ini',
                    prompts=['Config file import successfully'],
                    timeout=25)
            else:
                return self._s.command_expect(
                    f'copy usb {file_name}',
                    prompts=['Config file import successfully'],
                    timeout=25)

    def export_config(self, tftp_ip: str, file_name: str = "test.ini"):
        """
        Export the running configuration to a TFTP server.

            Args:
                tftp_ip (str): The IP address of the TFTP server.
                file_name (str, optional): The name of the configuration file to export. Defaults to "test.ini".

            Returns:
                str: A string indicating whether the config was uploaded successfully or not. 
        """
        return self._s.command_expect(
            f'copy running-config tftp {tftp_ip} {file_name}',
            prompts=['Configuration Upload Success!'], timeout=30)

    def export_eventlog(self, server: str="tftp", server_ip: str = None, category: str= "system"):
        """
         Export event log to file. This will create a file in the current directory with the contents of the event log.
         
            Args:
                server: Name of the server to export the event log to. Default : tftp. You can specify a different server by using the server_ip parameter.
                server_ip: IP address of the server to export the event log to.
                category: The category of the event log. Valid values are system vpn trust_access malformed_packets dos_policy device_lockdown L3L7_
        """
        event_map = {
            "system": "0",
            "vpn": "1",
            "trust_access": "2",
            "malformed_packets": "3",
            "dos_policy": "4",
            "device_lockdown": "5",
            "l3l7_policy": "6",
            "protocol_filter_policy": "7",
            "adp": "8",
            "ips": "9",
            "session_control": "10",
            "l2_policy": "11"
        }[category]
        server_map = {
            "tftp": "1", 
            "usb": "2", 
            "scp": "3", 
            "sftp": "4"
        }[server]
        return self._s.command_expect(
            f'copy event-log {event_map} {server_map} {server_ip}',
            prompts=['Event Log File Exporting is Complete.'])

    def get_running_config(self, con_type='telnet'):
        """
        Retrieve and return the running configuration from a device instance.

            Args:
                con_type (str): The connection type of DUT. Default to 'telnet'.

            Returns: 
                str: A string containing the running configuration of the device instance.
        """
        self.command('terminal length 0')
        return self._s.command_expect('show running-config',
                                        prompts=[PROMPT_MAIN],
                                        exact_str=True,
                                        timeout=5)['data']

    def upgrade_firmware(
            self,
            tftp_ip: str,
            file_name: str = "FWR_EDR-G9010_V3.0_Build_22122312.rom "):
        """
        Upgrade the firmware of the device from a given tftp server.

            Args:
                tftp_ip (str): The IP address of the TFTP server.
                file_name (str): The name of the firmware file to be upgraded. Defaults to "FWR_EDR-G9010_V3.0_Build_22122312.rom".

            Returns:
                dict: A dictionary containing the response from the device after upgrading the firmware. 
        """
        ret = self._s.command_expect(
            f'copy tftp {tftp_ip} device-firmware {file_name}',
            prompts=['login', 'Y/N'],
            timeout=180)
        # print('upgrade fw ret: ', ret)
        if ret['pattern'] == 'Y/N':
            # print('ret pattern == Y/N: ', ret)
            return self._s.command_expect('Y',
                                            prompts=['login'],
                                            exact_str=True,
                                            timeout=180)
        return ret

    def upgrade_package(
            self,
            tftp_ip: str,
            pkg_type: str,
            file_name: str = "Security_EDR-G9010_V5.5.4_Build_23020217.pkg"
    ):
        """
        Upgrade a package from a given tftp server.

            Args:
                tftp_ip (str): The IP address of the TFTP server. 
                pkg type (str): The type of package to upgrade e.g security or application etc.. 
                file name (str): The name of the package file to be upgraded e.g Security EDR-G9010 V5.5 Build 23020217 etc.. Defaults to "Security EDR-G9010 V5 Build 23020217".

            Returns: 
                dict: A dictionary containing the response from the device after upgrading the package 
        """
        ret = self._s.command_expect(
            f'package upgrade {pkg_type} tftp {tftp_ip} {file_name}',
            timeout=180)
        return ret

    def save(self):
        """
        Save changes made to device configuration

            Returns: 
                dict: A dictionary containing response from device after saving changes
        """
        return self._s.command_expect('save',
                                        prompts=[PROMPT_MAIN],
                                        exact_str=True,
                                        timeout=6)

    def set_config_file(self,
                        dig_signature: str,
                        data_encrypt: str = None,
                        encrypt_pwd: str = None):
        """
        Set the configuration file.

            Args:
                dig_signature (str): Configuration File Signature. Should be either "enable" or "disable".
                data_encrypt (str, optional): Signature Information. Should be either "sensitive" or "all".
                encrypt_pwd (str, optional): Encryption password.
                
            Raises:
                ValueError: If an invalid dig_signature or data_encrypt is given as input. 
        """
        if dig_signature in ["enable", "disable"]:
            if dig_signature == "enable":
                self._s.command_expect("config-file digital-signature",
                                        prompts=[PROMPT_MAIN])
            else:
                self._s.command_expect("no config-file digital-signature",
                                        prompts=[PROMPT_MAIN])
        else:
            raise ValueError(
                f'input invalid dig_signature: {dig_signature}')

        if data_encrypt:
            if data_encrypt in ["sensitive", "all"]:
                self._s.command_expect(
                    f"config-file data-encryption {data_encrypt}",
                    prompts=[PROMPT_MAIN])
            else:
                raise ValueError(
                    f'input invalid data_encrypt: {data_encrypt}')

        if encrypt_pwd:
            self._s.command_expect(
                f"config-file encryption-password {encrypt_pwd}",
                prompts=[PROMPT_MAIN])

    def show_object(self):
        ret = parser.show_object(self._s, self._model)
        return ret

    def show_session_ctrl(self):
        ret = parser.show_session_ctrl(self._s, self._model)
        return ret

    def show_lldp_table(self):
        ret = parser.show_lldp_table(self._s, self._model)
        return ret
    
    def show_l2tp_setting(self):
        return parser.show_l2tp_setting(self._s, self._model)
    
    def show_snmp(self):
        return parser.show_snmp(self._s, self._model)
