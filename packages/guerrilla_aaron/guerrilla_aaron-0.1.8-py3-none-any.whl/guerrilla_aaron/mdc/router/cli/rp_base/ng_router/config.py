from guerrilla_aaron.utils.input_chk import chk_valid_ip
from guerrilla_aaron.mdc.router.cli.rp_base.ng_router import cli
from guerrilla_aaron.mdc.router.cli.rp_base.ng_router.cli import PROMPT_CONFIG

class Config(cli.Cli):
    """
    Class for configuring a device through the command line interface.

        Args:
            session (Session): A Session object used to communicate with the device.

        Attributes:
            _s (Session): A Session object used to communicate with the device.
    """

    def __init__(self, session: object):
        super().__init__(session)
        # back to main
        self._back_to_main()
        # jumpt to config terminal
        self.getin_cfg()

    def get_session(self):
        """
        Return the Session object used to communicate with the device.

            Returns: 
                Session: The Session object used to communicate with the device.
        """
        return self._s

    def _set_default_prompts_cfg(self):
        """
        Set default prompts for configuration mode.
        """
        self._s.set_default_prompts([PROMPT_CONFIG])

    def _getin_cfg(self):
        """
        Enter configuration mode.
        """
        self._s.command_expect('configure terminal')

    # function override is allowed
    def getin_cfg(self):
        """
        Enter configuration mode and set default prompts for configuration mode. 

            Returns: 
                Session: The Session object used to communicate with the device in configuration mode.
        """
        self._set_default_prompts_cfg()
        self._getin_cfg()
        return self

    class MailServer:
        """
        A class representing a mail server.

            Attributes:
                _s (object): The session object used to interact with the mail server.

            Methods:
                set_server(server: str, port: int): Sets the server and port for the mail server.
                set_mail_address(mail_address: str): Sets the mail address for the mail server.
                set_account(account: str, paswd: str): Sets the account and password for the mail server.
                set_sender(mail_address: str): Sets the sender mail address for the mail server.
                send_test(self): Sends a test email from the mail server.
        """
        def __init__(self, session: object):
            self._s = session
        def set_server(self, server, port):
            """
            Sets the server and port for the email-warning command.

                Args:
                    server (str): The server to set.
                    port (int): The port to set.
            """
            self._s.command_expect(f'email-warning server {server} {port}')
        def set_mail_address(self, mail_address):
            """
            Sets the email address for receiving warnings.

                Args:
                    mail_address (str): The email address to set.
            """
            self._s.command_expect(f'email-warning mail-address 1 {mail_address}')
        def set_account(self, account, paswd):
            """
            Sets the account and password for the router.

                Args:
                    account (str): The account to set.
                    paswd (str): The password to set.
            """
            self._s.command_expect(f'email-warning account {account} {paswd}')
        def set_sender(self, mail_address):
            """
            Sets the sender email address for email warnings.

                Args:
                    mail_address (str): The email address to set as the sender.
            """
            self._s.command_expect(f'email-warning sender {mail_address}')
        def send_test(self):
            """
            Sends a test email warning using the `_s` instance.
            """
            self._s.command_expect(f'email-warning send')

    # ======== dhcp feature ========
    class DhcpService:
        """Class to configure DHCP service.

            Args:
                session (object): An instance of the Session class.
        """

        def __init__(self, session: object):
            self._s = session

        def set_global_dhcp_service(self,
                                    action: str = "enable",
                                    mode: str = ""):
            """
            Configure global DHCP service.
            
                Args
                    mode: global dhcp mode ("" or auto-assign).
                    action: global dhcp action (enable or disable).
            """
            cmd = "service dhcp"
            if action == "enable":
                cmd = f"{cmd} {mode}"
            elif action == "disable":
                cmd = f"no {cmd} {mode}"
            else:
                raise ValueError(f"input invalid action: {action}")

            self._s.command_expect(cmd)

        def set_global_dhcp_server(self,
                                    mode: str = "pool",
                                    action: str = "enable",
                                    index: str = "1",
                                    name: str = "dhcp_server"):
            """
            Configure global DHCP server.

            Args
                mode: dhcp server mode (pool or static pool).
                name: dhcp server name. Defaults to "dhcp_server".
                index: dhcp server index. Defaults to "1".
                action: dhcp server action (enable or disable).
            """
            cmd = "ip dhcp"
            if mode == "pool":
                cmd = f"{cmd} {mode} {index} {action}"
            elif mode == "static pool":
                cmd = f"{cmd} {mode} {name} {action}"
            else:
                raise ValueError(f"input invalid dhcp mode: {mode}")

            self._s.command_expect(cmd)

    # ======== End of dhcp feature ========
    # ======== login lockout feature ========
    class LoginLockout:
        """
        Class to configure login lockout settings on a device.

            Args:
                session (Session): Instance of Session class to communicate with the device.

            Attributes:
                _s (Session): Instance of Session class to communicate with the device.
                _cmd (str): Command used to configure login lockout settings.
        """

        def __init__(self, session: object):
            self._s = session
            self._cmd = 'login-lockout'

        def lockout_toggle(self, toggle: bool):
            """
            Enable or disable login lockout on the device.

                Args:
                    toggle (bool): True to enable, False to disable. 
            """
            if toggle is True:
                self._s.command_expect(f'{self._cmd}')
            else:
                self._s.command_expect(f'no {self._cmd}')

        def lockout_retryThreshold(self, retry: str):
            """
            Configure the number of failed login attempts before locking out an account.

                Args: 
                    retry (str): Number of failed login attempts before locking out an account. 
            """
            self._s.command_expect(f'{self._cmd} retry-threshold {retry}')

        def lockout_lockoutTime(self, duration: str):
            """
            Configure the duration for which an account is locked out after exceeding the maximum number of failed login attempts. 

                Args: 
                    duration (str): Duration in minutes for which an account is locked out after exceeding the maximum number of failed login attempts.  
            """
            self._s.command_expect(f'{self._cmd} lockout-time {duration}')

    # ======== End of login lockout feature ========
    # ======== time sync feature ========
    class TimeSync:
        """
        Class for synchronizing time with a remote server or manually setting the time.

            Args:
                session (object): Session object to send commands to the device.
        """

        def __init__(self, session: object):
            self._s = session

        def clock_source(self, clk_src: str, remote_server: str = None):
            """
            Set the clock source for the device.

                Args:
                    clk_src (str): Clock source to set, either 'local', 'ntp' or 'sntp'.
                    remote_server (str): IP address of the remote server to sync with. Required if clk_src is 'ntp' or 'sntp'.

                Raises:
                    Exception: If an unsupported clock source is provided. 
            """
            if clk_src.lower() == "local":
                self._s.command_expect(f'no ntp remote-server')
            elif clk_src.lower() == "ntp" or clk_src.lower() == "sntp":
                chk_valid_ip(remote_server)
                cmd = f'ntp remote-server {remote_server}'
                if clk_src.lower() == "sntp":
                    cmd += ' simple'
                self._s.command_expect(cmd)
            else:
                raise Exception(f"Unsupported Clock Source: {clk_src}")

        def ntp_server_toggle(self, toggle):
            """
            Toggle the NTP server on or off.

                Args:
                    toggle (bool): True to turn on the NTP server, False to turn it off.
            """
            if toggle is True:
                self._s.command_expect(f'ntp server')
            else:
                self._s.command_expect(f'no ntp server')

        def set_time_manually(self, year: str, month: str, day: str,
                                hour: str, min: str, sec: str):
            """
            Set the time manually for the device.

                Args: 
                    year (str): The year to set the time to. 
                    month (str): The month to set the time to. 
                    day (str): The day to set the time to. 
                    hour (str): The hour to set the time to. 
                    min (str): The minute to set the time to. 
                    sec (str): The second to set the time to. 
            """
            self._s.command_expect(
                f'clock set {hour}:{min}:{sec} {month} {day} {year}')

    # ======== End of time sync feature ========

    def set_clock_summer_time(self,
                                start_date: str = None,
                                end_date: str = None,
                                offset: str = None):
        """
        Set the Daylight Saving for the device.
            Args: 
                start_date (str): The Date when Summer Time Offset Start. The format should be "{month} {week} {day} {hour} {min}" 
                end_date (str): The Date when Summer Time Offset End. The format should be "{month} {week} {day} {hour} {min}"
                offset (str): Summer Time Offset. (1 - 12)
            Explanation of the Time format:
                month: From 'Jan', 'January' or '1' to 'Dec', 'December', or '12'
                week: From '1st' or '1' to 'Last' or '6'
                day: From 'Sun', 'Sunday' or '1' to 'Sat', 'Saturday' or '7'
                hour: 0 - 23
                min: 0 - 59
        """
        if start_date:
            self._s.command_expect(
                f'clock summer-time start-date {start_date}')
        if end_date:
            self._s.command_expect(f'clock summer-time end-date {end_date}')
        if offset:
            self._s.command_expect(f'clock summer-time offset {offset}')

    def set_hostname(self, hostname: str):
        """
        Sets the hostname of the device.

            Args:
                hostname (str): The name of the device. 
        """
        self._s.command_expect(command=f'hostname {hostname}')

    def set_login_account(self,
                            action: str,
                            username: str,
                            password: str,
                            privilege: str = None):
        """
        Sets the login account for the device.

            Args: 
                action (str): The action to be taken on the login account. Can be either "create", "modify" or "delete". 
                username (str): The username of the login account. 
                password (str): The password of the login account. 
                privilege (str, optional): The privilege level of the login account. Can be either "system admin", "configuration admin", "user" or "no login". Defaults to None.
        """
        cmd = ""
        if username:
            cmd += f"username {username} "
        if password:
            cmd += f"password {password} "

        if privilege != None:
            if privilege == "system admin":
                cmd += "privilege 1"
            elif privilege == "configuration admin":
                cmd += "privilege 2"
            elif privilege == "user":
                cmd += "privilege 3"
            elif privilege == "no login":
                cmd += "privilege 4"
            else:
                raise ValueError(f'input invalid privilege: {privilege}')

        if action != None:
            if action == "delete":
                cmd = f"no {cmd}"
            elif action in ["create", "modify"]:
                pass
            else:
                raise ValueError(f'input invalid action: {action}')
        return self._s.command_expect(cmd, prompts=["#"], exact_str=True)

    def set_password_policy(self,
                            min_len: str = None,
                            action: str = None,
                            global_complexity_check: bool = None,
                            complexity_item: str = None):
        """
        Set password policy.

            Args:
                min_len (str): Minimum length of the password.
                action (str): Enable or disable the password policy.
                global_complexity_check (bool): Enable or disable the global complexity check of the password.
                complexity_item (str): Complexity item of the password.

            Returns:
                str: The output of command execution. 
        """
        cmd = "password-policy "
        if min_len:
            cmd += f"minimum-length {min_len}"
        elif global_complexity_check:
            cmd += f"complexity-check"

        if complexity_item != None:
            if complexity_item == "digit":
                cmd += f"complexity-check digit"
            elif complexity_item == "alphabet":
                cmd += f"complexity-check alphabet"
            elif complexity_item == "special-characters":
                cmd += f"complexity-check special-characters"
            else:
                raise ValueError(
                    f'input invalid complexity item: {complexity_item}')

        if action != None:
            if action == "disable":  # can only disable complexity
                cmd = f"no {cmd}"
            elif action == "enable":
                pass
            else:
                raise ValueError(f'input invalid action: {action}')

        return self._s.command_expect(cmd, prompts=["#"], exact_str=True)

    def set_global_l3l7_policy(self,
                                global_action: str = None,
                                default_action: str = None,
                                index: str = None,
                                index_action: str = None):
        """
        Set global l3l7 policy.

            Args:
                global_action (str): Global action.
                default_action (str): Default action.
                index (str): Index of the policy.
                index_action (str): Action of the policy with given index. 
            Returns:
                self: The instance itself. 
        """
        cmd = "l3l7-policy "
        if global_action:
            cmd += global_action
        elif default_action:
            cmd += f"default-action {default_action}"
        elif index:
            cmd += f"{index} {index_action}"
        self._s.command_expect(cmd, prompts=[PROMPT_CONFIG])
        return self

    def set_log(self, log_item: str = None):
        """
        Set log item for logging. 
            Args: 
                log_item (str): Log item to be set for logging, valid items are "trusted-access", "dos", "ipsec", "firewall", and "l3l7-policy". 
            Returns: 
                self: The instance itself.
        """
        log_list = [
            "trusted-access", "dos", "ipsec", "firewall", "l3l7-policy"
        ]
        if log_item in log_list:
            self._s.command_expect(f"logging {log_item}",
                                    prompts=[PROMPT_CONFIG])
        else:
            raise ValueError(f'input invalid log item: {log_item}')
        return self

    def set_syslog_server(self,
                            action: str,
                            ip: str,
                            port: str = '514',
                            index: str = '1'):
        """
        Set the syslog server configuration.

            Args:
                action (str): The action to perform on the syslog server. Can be either "create", "enable" or "disable".
                ip (str): The IP address of the syslog server. 
                port (str, optional): The port number of the syslog server. Defaults to 514. 
                index (str, optional): The index of the syslog server. Defaults to 1. 
                
            Raises:
                ValueError: If an invalid action is given as input. 
        """
        if action == "create":  # create server will enable itself as well
            self._s.command_expect(f"logging {ip} {port} {index}",
                                    prompts=[PROMPT_CONFIG])
        elif action in ["enable", "disable"]:
            self._s.command_expect(f"logging {ip} {port} {action}",
                                    prompts=[PROMPT_CONFIG])
        else:
            raise ValueError(f'input invalid action: {action}')

    def set_warning_notification(self,
                                    event: str,
                                    action: str = None,
                                    severity: str = None,
                                    active: bool = None):
        """
        Set warning notification for system events.

            Args:
                event (str): System event type. Valid types are cold-start, warm-start, pwr1-trans-on, pwr2-trans-on, pwr1-trans-off, pwr2-trans-off, auth-fail, topology-changed, coupling-changed, master-changed, di1-trans-on, di1-trans-off, fiber-warning, vrrp-state changed, dot1x auth fail, firewall policy changed and config changed.
                action (str): Action type for the system event. Valid types are SNMP Trap Server only, Email only , SNMP Trap Server+Email , Syslog only , SNMP Trap Server+Syslog Server , Email+Syslog Server , SNMP Trap Server+Email+Syslog Server , Relay1 only , SNMP Trap Server+Relay1 , Email+Relay1 , SNMP Trap Server+Email+Relay1 , Syslog+Relay1 , SNMP Trap Server+Syslog Server+Relay1 , Email+Syslog Server+Relay1 and SNMP Trap Server +Email +Syslog Server +Relay1. 
                severity (str): Severity type for the system event. Valid types are Emergency 0 Alert 1 Critical 2 Error 3 Warning 4 Notice 5 Information 6 Debug 7 
                active (bool): Whether to enable the warning notification for the system event or not. 
                
            Raises:
                ValueError: If input invalid event type. 
        """
        action_type = {
            "SNMP Trap Server only": 1,
            "Email only": 2,
            "SNMP Trap Server+Email": 3,
            "Syslog only": 4,
            "SNMP Trap Server+Syslog Server": 5,
            "Email+Syslog Server": 6,
            "SNMP Trap Server+Email+Syslog Server": 7,
            "Relay1 only": 8,
            "SNMP Trap Server+Relay1": 9,
            "Email+Relay1": 10,
            "SNMP Trap Server+Email+Relay1": 11,
            "Syslog+Relay1": 12,
            "SNMP Trap Server+Syslog Server+Relay1": 13,
            "Email+Syslog Server+Relay1": 14,
            "SNMP Trap Server+Email+Syslog Server+Relay1": 15
        }
        event_type = [
            "cold-start", "warm-start", "pwr1-trans-on", "pwr2-trans-on",
            "pwr1-trans-off", "pwr2-trans-off", "auth-fail",
            "topology-changed", "coupling-changed", "master-changed",
            "di1-trans-on", "di1-trans-off", "fiber-warning",
            "vrrp-state-changed", "dot1x-auth-fail",
            "firewall-policy-changed", "config-changed"
        ]
        severity_type = {
            "Emergency": 0,
            "Alert": 1,
            "Critical": 2,
            "Error": 3,
            "Warning": 4,
            "Notice": 5,
            "Information": 6,
            "Debug": 7
        }
        if event in event_type:
            if active == True:
                self.command(
                    f"warning-notification system-event {event} active")
            if action in action_type:
                self.command(
                    f"warning-notification system-event {event} action {action_type[action]}"
                )
            if severity in severity_type:
                self.command(
                    f"warning-notification system-event {event} severity {severity_type[severity]}"
                )
        else:
            raise ValueError(f'input invalid event: {event}')

    def set_trusted_access(self,
                            ip: str = None,
                            mask: str = None,
                            action: str = None,
                            global_toggle: str = None):
        """
        Set trusted access on the device. 

            Args:
                ip (str): IP address of the trusted access.
                mask (str): Mask of the trusted access.
                action (str): Action to be taken on the trusted access. Must be either "enable" or "delete".
                global_toggle (str): Global toggle to enable/disable the trusted access.

            Raises:
                ValueError: If an invalid action is provided.
        """
        if global_toggle:
            if global_toggle == "enable":
                self.command(f"interface trusted-access")
            elif global_toggle == "disable":
                self.command(f"no interface trusted-access")
            else:
                raise ValueError(
                    f'input invalid global_toggle: {global_toggle}')
        if ip and mask:
            if action == "enable":
                self.command(f"interface trusted-access {ip} {mask} enable")
            elif action == "disable":
                self.command(
                    f"interface trusted-access {ip} {mask} disable")
            elif action == "delete":
                self.command(f"no interface trusted-access {ip} {mask}")
            else:
                raise ValueError(f'input invalid action: {action}')

    def set_vlan_id(self, vlan_id: str, delete=False):
        """
        Set VLAN ID on the device.

            Args: 
                vlan_id (str): VLAN ID to be set on the device.
                delete (bool): defualt as False, which means default as creating vlan

            Returns: 
                self: Return self for method chaining. 
        """
        if delete == False:
            self._s.command_expect(f"vlan create {vlan_id}")
        elif delete == True:
            self._s.command_expect(f"no vlan create {vlan_id}")
        return self

    def set_ip_ping_response(self):
        """
        Enable IP ping response on the device.

            Returns: 
                self: Return self for method chaining. 
        """
        self._s.command_expect("ip ping-response")
        return self

    def set_ip_http_max_login_users(self, max_users: str):
        """
        Set maximum login users for HTTP server on the device.

            Args: 
                max_users (str): Maximum login users for HTTP server to be set on the device.

            Returns: 
                self: Return self for method chaining.
        """
        self._s.command_expect(
            f"ip http-server max-login-users {max_users}")
        return self

    def set_global_telnet(self,
                            port: int = None,
                            max_login_users: int = None):
        """
        Set the global telnet configuration.

            Args:
                port (int, optional): The port to use for telnet. Defaults to None.
                max_login_users (int, optional): The maximum number of users allowed to log in via telnet. Defaults to None.
        """
        if port != None:
            self._s.command_expect(f"ip telnet port {port}")
            self._s.command_expect(f"ip telnet")
        if max_login_users != None:
            self._s.command_expect(
                f"ip telnet max-login-users {max_login_users}")

    def set_ntp_auth(self, key_id: str, key_type: str, key: str):
        """
        Create NTP Authentication Keys on the device. 

            Args:
                key_id (str): Key ID (1~65535)
                key_type (str): "MD5" or "SHA512"
                key (str): Key String (max. 32 characters)
        """
        self._s.command_expect(
            f"ntp authentication-key {key_id} {key_type} {key}")
        return self

    def set_l2tp_user(self, name: str, pwd: str):
        self._s.command_expect(f"l2tp user {name} password {pwd}")
        return self

    def set_email(self, name: str = None, pwd: str = None):
        if name and pwd:
            self._s.command_expect(f"email-warning account {name} {pwd}")
        return self

    def set_ddns(self,
                    service: str = None,
                    name: str = None,
                    pwd: str = None,
                    domain: str = None):
        """
        Set the Dynamic Domain Name System (DDNS) service. 

            Args: 
                service (str): The DDNS service to use, defaults to 'no-ip'. 
                name (str): The username for the DDNS service. 
                pwd (str): The password for the DDNS service. 
                domain (str): The domain for the DDNS service. 
                
            Returns: 
                self: Returns itself for chaining purposes.
        """
        if service in ['freedns', '3322', 'dyndns', 'no-ip']:
            self._s.command_expect(f"ip ddns service {service}")
        if name:
            self._s.command_expect(f"ip ddns username {name}")
        if pwd:
            self._s.command_expect(f"ip ddns password {pwd}")
        if domain:
            self._s.command_expect(f"ip ddns domain {domain}")
        return self

    def set_dot1x_radius_server(self,
                                server_idx: int,
                                ip: str = None,
                                port: str = None,
                                key: str = None):
        """
        Set the dot1x radius server. This is a wrapper around the'dot1x radius 1st'or'dot1x radius 2nd'command.
            
            Args:
                server_idx: index of server to set ( 1 or 2 )
                ip: ip address to set ( optional ) defaults to None
                port: port to set ( optional ) defaults to None
                key: shared key to set ( optional ) defaults to None
            
            Returns: 
                self for daisychaining ( self )
        """
        
        # This function is used to generate the dot1x radius 1st server
        if server_idx == 1:
            cmd = "dot1x radius 1st-server"
        elif server_idx == 2:
            cmd = "dot1x radius 2nd-server"
        # expect server ip if ip is not set
        if ip:
            self._s.command_expect(f"{cmd} server-ip {ip}")
        # expect command to be sent to server port
        if port:
            self._s.command_expect(f"{cmd} server-port {port}")
        # expect command shared key if key is not provided
        if key:
            self._s.command_expect(f"{cmd} shared-key {key}")
        return self

    def set_dot1x_local_db(self, name: str, pwd: str):
        """
         Set dot1x local database. This is a shortcut for ` dot1x local - userdb username password `
         
            Args:
                name: Name of the user to set
                pwd: Password of the user to set
            
            Returns: 
                self for daisychaining ( self )
        """
        self._s.command_expect(
            f"dot1x local-userdb username {name} password {pwd}")
        return self

    
    def set_authentication_login_mode(self, auth_mode):
        """
         Select the Authentication login option.

            Args:
                 auth_mode: authentication login option.
                 - local: Authenticated in Local.
                 - radius: Authenticated in radius.
                 - radius local: Authenticated in RADIUS and Local by sequence.
        """
        if auth_mode == 'local':
            cmd = 'auth mode local'
        elif auth_mode == 'radius':
            cmd = 'auth mode radius'
        elif auth_mode == 'radius_local':
            cmd = 'auth mode radius local'
        else:
            raise ValueError(f"input invalid auth_mode: {auth_mode}")

        self._s.command_expect(cmd)
        return self

        
    def set_radius_server(self, server_idx, ip, port, key):
        """
         Set RADIUS server. This is a wrapper around the ` ` auth radius server ` ` command.
         
            Args:
                server_idx: The index of the server to set.
                ip: The IP address of the RADIUS server.
                port: The port of the RADIUS server. If the server is listening on a port other than 6379 this will be ignored.
                key: The key used to authenticate the RADIUS server.
            
            Returns: 
                    self for daisychaining ( self ) 
        """
        self._s.command_expect(
            f"auth radius server {server_idx} {ip} port {port} key {key}")
        return self

    
    def set_radius_server_auth_type(self, auth_type):
        """
         Set radius server auth type to login authentication
             
             Args: 
                 auth_type: RADIUS server auth type
                 - pap
                 - chap
                 - peap-mschapv2
        """
        if auth_type not in ["pap", "chap", "peap-mschapv2"]:
            raise ValueError(f"invalid auth_type: {auth_type}")

        self._s.command_expect(f"auth radius auth-type {auth_type}")
        return self


    def set_port_mirror(self, src: str = None, dst: str = None):
        """
        Configure Port mirror on a device.

            Args:
                src (str): monitorPort ( Port ID. Ex. 1/3, Trk2)
                dst (str): mirrorPort (Port ID. Ex. 1/3, 2/1)
            Returns: 
                self for daisychaining ( self )
        """
        if src:
            self._s.command_expect(f"monitor source interface {src}")
        if dst:
            self._s.command_expect(f"monitor destination interface {dst}")
        return self

    def set_hardware_interface(self, enable: bool = True):
        """
        Enable hardware interface (USB) of DUT.

            Args:
                enable (bool, optional): To decide the hardware interface will be turned-on or not.
        """
        if enable == True:
            self._s.command_expect(f"auto-backup enable")
        else:
            self._s.command_expect(f"no auto-backup enable")
        return self

    def set_l37_rule_status(self, index, status):
        """
        Modify the status of a specified L3/L7 rule.

        Args:
            index (int): The index of the L3/L7 policy rule to modify.
            status (str): The status to set for the L3/L7 policy rule. "enable" to enable the rule, "disable" to disable it.
        """
        self._s.command_expect(f"l3l7-policy {index} {status}")
        return self 

    def set_global_vrrp(self, version: str = "3", status: str = "enable"):
        """
         Sets the VRRP status of the device. This is useful for debugging and to make it easier to use the device in a real - time program
         
         Args:
         	 version: The version of the RTP device
         	 status: The status of the RTP device ( enable|disable )
         
         Returns: 
         	 The self for method chaining ( self. _s )
        """
        # Set vrrp version
        if version:
            self._s.command_expect(f"vrrp version {version}")
        # Enable or disable the vrrp
        if status == "enable":
            self._s.command_expect(f"router vrrp")
        elif status == "disable":
            self._s.command_expect(f"no router vrrp")
        else:
            raise ValueError(f"Input invalid status: {status}")
        return self

    class MulticastRoute:
        """Class to configure Multicast Route.

            Args:
                session (object): An instance of the Session class.
        """

        def __init__(self, session: object):
            self._s = session

        def set_global_multicast_route(self, mode: str = "static"):
            """
            Configure global multicast route.
            
                Args
                    action: global multicast route mode (static or disable).
            """
            if mode == "static":
                cmd = f"ip multicast-routing static"
            elif mode == "disable":
                cmd = "no ip multicast-routing"
            else:
                raise ValueError(f"input invalid mode: {mode}")

            self._s.command_expect(cmd)

        def set_static_multicast_route_rule(self,
                                            action: str = "add",
                                            group_addr: str = None,
                                            src_addr: str = None,
                                            in_itf: str = None,
                                            out_itf: str = None):
            """
            Configure global DHCP server.

            Args
                action: configure static multicast route (add / enable / disable).
                group_addr: multicast group
                src_addr: multicast stream source
                in_itf: Inbound interface
                out_itf: Outbound interface
            """
            if action == "add":
                cmd = f"ip mroute group {group_addr} src {src_addr} in \
                            {in_itf} out {out_itf}"

            elif action == "enable":
                cmd = f"ip mroute group {group_addr} src {src_addr} enable"
            elif action == "disable":
                cmd = f"ip mroute group {group_addr} src {src_addr} disable"
            else:
                raise ValueError(f"input invalid action: {mode}")

            self._s.command_expect(cmd)

    def set_malformed_packet_status(self, status: str):
        """
        Configure Malformed Packets Status on a device.

            Args:
                status (str): To decide the Malformed Packets Drop will be "Enabled" or "Disabled".
        """
        if status == "Enabled":
            self._s.command_expect("firewall malformed")
        elif status == "Disabled":
            self._s.command_expect("no firewall malformed")

    def set_malformed_packet_log(self, status: str, dst: set):
        """
        Configure Malformed Packets Log on a device.

            Args:
                status (str): To decide the Malformed Packets Log will be "Enabled" or "Disabled"
                dst (list): the destination of log, can be "flash", "syslog", or "trap"
        """
        if dst.issubset({"flash", "syslog", "trap"}):
            if status == "Enabled":
                for d in dst:
                    self._s.command_expect(
                        f"firewall malformed logging {d}")
            elif status == "Disabled":
                for d in dst:
                    self._s.command_expect(
                        f"no firewall malformed logging {d}")

    class IgmpSnooping:

        def __init__(self, session: object):
            self._s = session

        def set_igmp_snooping_vlan(self, action: str, vid: str):
            if action == 'enable':
                self._s.command_expect(f"ip igmp-snooping vlan {vid}")
            elif action == 'disable':
                self._s.command_expect(f"no ip igmp-snooping vlan {vid}")
            else:
                raise ValueError(f'input invalid action')
            return self

        def set_igmp_snooping_querier(self, action: str, vid: str):
            if action == 'enable':
                self._s.command_expect(
                    f"ip igmp-snooping querier vlan {vid}")
            elif action == 'disable':
                self._s.command_expect(
                    f"no ip igmp-snooping querier vlan {vid}")
            else:
                raise ValueError(f'input invalid action')
            return self

        def set_igmp_snooping_interval(self, interval: str):
            if 20 <= int(interval) <= 600:
                self._s.command_expect(
                    f"ip igmp-snooping query-interval {interval}")
            else:
                raise ValueError(f'input interval out of range')
            return self

    def set_broadcast_forward_status(self, action: str):
        """
        Configure broadcast forward status on a device.

            Args:
                action (str): To decide the broadcast forward will be "Enabled" or "Disabled".
        
        """
        if action == 'enable':
            self._s.command_expect(f"ip broadcast-forward")
        elif action == 'disable':
            self._s.command_expect(f"no ip broadcast-forward")
        else:
            raise ValueError(f'input invalid action')
        return self
    
    def add_broadcast_forward_rule(self, in_itf: str, out_itf: str, udp_port: str):
        """
        Configure broadcast forward rule on a device.

            Args:
                in_itf (str): Inbound interface
                out_itf (str): Outbound interface
                udp_port (str): UDP port
        
        """
        self._s.command_expect(f"ip broadcast-forward in {in_itf} out {out_itf} udp {udp_port}")
        return self
    
    def set_lldp_status(self, action: str):
        """
        Configure LLDP status on a device.

            Args:
                action (str): To decide the LLDP will be "Enabled" or "Disabled".
        
        """
        if action == 'enable':
            self._s.command_expect(f"lldp enable")
        elif action == 'disable':
            self._s.command_expect(f"no lldp enable")
        else:
            raise ValueError(f'input invalid action')
        return self

    def set_lldp_transmission_freq(self, interval: str):
        """
        Configure LLDP Transmission Frequency on a device.

            Args:
                interval (str): LLDP interval
        
        """
        if 5 <= int(interval) <= 32768:
            self._s.command_expect(f"lldp timer {interval}")
        else:
            raise ValueError(f'input interval out of range')
        return self
        
    class Rstp:
        def __init__(self, session: object):
            """
             Initialize the instance. This is called by __init__ and should not be called directly
             
             Args:
             	 session: The session to use
            """
            self._s = session
        def set_rstp_status(self, action):
            """
             Enable or disable RSTP. Redundancy mode can be enabled or disabled at the same time
             
             Args:
             	 action: " enable " or " disable
            """
            # enable disable or rstp.
            if action == "enable":
                self._s.command_expect('redundancy mode rstp')
            # either "spanning tree" or "turbo ring" must be enabled and cannot be enabled or disabled at the same time
            elif action == "disable":
                self._s.command_expect('redundancy mode turbo-ring-v2')
            else:
                raise ValueError(f"input invalid action: {action}")
        
        def set_rstp_port(self, 
                             port,
                             action: str = "enable", 
                             edge_port: bool = False, 
                             priority: str = None, 
                             cost: str = None
                             ):
            """
            Set RSTP settings for a port. This is useful for port selection and retransmission of packets.
            
                Args:
                    port: port to set RSTP settings for.
                    edge_port: if True set RSTP edge settings for this port
                    priority: priority of the packet ( default : 0 )
                    cost: cost of the packet ( default : None )
                
                Returns: 
                    ` ` True ` ` if successful ` ` False ` `
            """
            self._s.command_expect(f'interface ethernet 1/{port}')
            if action == "enable":
                self._s.command_expect(f'spanning-tree')
            elif action == "disable":
                self._s.command_expect(f'no spanning-tree')
            else:
                raise ValueError(f"input invalid status: {action}")
            # expects panning tree edge port command
            if edge_port:
                self._s.command_expect(f'spanning-tree edge-port')
            # expect priority priority if priority is set
            if priority:
                self._s.command_expect(f'spanning-tree priority {priority}')
            # expect the panning tree cost
            if cost:
                self._s.command_expect(f'spanning-tree cost {cost}')
            return self

    def set_static_multicast_table(self, mac: str, port: str = None, vlan: str = None):
        """
        Configure static multicast table on a device

            Args:
                mac (str): Source MAC address.
                port (str): The port use for multicast group. Defaults to None.
                vlan (str): VLAN ID should belong to all of the selected ports.
        """
        self._s.command_expect(f'ip igmp static-group {mac} interface 1/{port} vlan {vlan}')
        return self


    class L2tp:
        def __init__(self, session: object):
            """
             Initialize the instance. This is called by __init__ and should not be called directly
             
             Args:
             	 session: The session to use
            """
            self._s = session

        def set_l2tp_rule(self, local_ip: str, start_ip: str, end_ip: str):
            """
            Configure l2tp interface setting on a device.

                Args:
                    local_ip (str): l2tp server ip.
                    start_ip (str): Starting IP of the Offer IP.
                    end_ip (str): Ending IP of the Offer IP.
            """
            cmd = 'l2tp interface WAN '
            cmd += f'local-ip {local_ip} '
            cmd += f'offer-ip {start_ip} {end_ip}'
            
            self._s.command_expect(cmd)
            return self
        
        def set_l2tp_user(self, username: str, password: str):
            """
            Configure l2tp user setting on a device.

                Args:
                    username (str): The account used for L2TP client login.
                    password (str): The password used for L2TP client login.
            """
            cmd = 'l2tp '
            cmd += f'user {username} '
            cmd += f'password {password}'
            
            self._s.command_expect(cmd)
            return self

    class Snmp:
        def __init__(self, session: object):
            """
             Initialize the instance. This is called by __init__ and should not be called directly
             
             Args:
             	 session: The session to use
            """
            self._s = session
        def set_snmp_version(self, snmp_version: str = None):
            """
            Set the SNMP version.
             
             Args:
             	 snmp_version (str): The 4 SNMP version categories are (v1, v2c, v3) or (v1, v2c) and (v3 only) or (disable).
                                     Default is disable.
            """
            self._s.command_expect(f'snmp-server version {snmp_version}')
            return self
        
        def set_snmp_user(self, 
                            user: str, 
                            priv_key: str,
                            auth_type: str = 'no-auth',
                            priv_method: str = None):
            """
            Set the SNMP version.
             
             Args:
             	 user (str): SNMP username.
             	 priv_key (str): SNMPv3 privacy key.
             	 auth_type (str): SNMPv3 authentication type. Options: 'no-auth', 'md5', 'sha'. Default is 'no-auth'.
             	 priv_method (str): SNMPv3 privacy protocol. Options: 'des', 'aes'. Default is None.
            """
            cmd = f'snmp-server user {user} auth {auth_type} '
            
            if priv_method:
                cmd += f'priv {priv_method} {priv_key}'

            self._s.command_expect(cmd)
            return self

        def set_engine_id(self, engine_id: str):
            """
            Set the SNMP version.
             
             Args:
             	 engine_id (str): Engine id of SNMP agent. Prefix should be 800021f305.
            """
            self._s.command_expect(f'snmp-server engineid {engine_id}')
            return self
        
        def set_snmp_trap_host(self, host: str, community: str = 'public'):
            """
            Set the SNMP host to receive trap/inform notification.
             
            Args:
                host (str): SNMP Host IP Address.
                community (str): SNMP Host community. Default is 'public'.
            """
            self._s.command_expect(f'snmp-server host {host} {community}')
            return self
    
        def set_snmp_trap_inform_v3(self, 
                                    trap_mode: str,
                                    user: str, 
                                    passwd: str, 
                                    auth_type: str = 'no-auth', 
                                    priv_key: str = None ):
            """
            Set the SNMP host to receive trap/inform notification.
             
            Args:
                mode (str): SNMP v3 trap/ inform. Options: 'trap-v3', 'inform-v3'.
                user (str): SNMP trap user.
                passwd (str): Password for authentication.
                auth_type (str): SNMPv3 authentication type. Options: 'no-auth', 'md5', 'sha'. Default is 'no-auth'.
                priv_key (str): SNMP Host community. Default is None.
            """
            cmd = f'snmp-server {trap_mode} user {user} auth {auth_type} {passwd} '

            if priv_key:
                cmd += f'priv {priv_key}'

            self._s.command_expect(cmd)
            return self
                    
        def set_snmp_trap_mode(self, 
                               trap_mode: str, 
                               retry: str = None,
                               timeout: str = None):
            """
            Set the SNMP trap mode.
             
            Args:
                trap_mode (str): SNMP trap mode. Option: trap-v1, trap-v2c, trap-v3, inform (inform-v2c)
            """
            cmd = f'snmp-server trap-mode {trap_mode}'

            if 'inform' in trap_mode:
                cmd += f' retry {retry} timeout {timeout}'

            self._s.command_expect(cmd)
            return self
        
