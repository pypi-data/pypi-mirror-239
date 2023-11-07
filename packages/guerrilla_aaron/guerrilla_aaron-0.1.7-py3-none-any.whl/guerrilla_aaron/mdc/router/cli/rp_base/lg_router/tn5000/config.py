from guerrilla_aaron.utils.input_chk import chk_valid_ip
from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000 import cli
from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000.cli import PROMPT_CONFIG

class Config(cli.Cli):
    """
    Class for configuring a device through the command line interface.

        Args:
            session (Session): A Session object used to communicate with the device.

        Attributes:
            _s (Session): A Session object used to communicate with the device.
    """

    def __init__(self, session):
        super().__init__(session)
        # back to main
        self._back_to_main()
        # jumpt to config terminal
        self.getin_cfg()

    def get_session(self):
        return self._s

    def _set_default_prompts_cfg(self):
        self._s.set_default_prompts([PROMPT_CONFIG])

    def _getin_cfg(self):
        self._s.command_expect('configure terminal')

    # function override is allowed
    def getin_cfg(self):
        self._set_default_prompts_cfg()
        self._getin_cfg()
        return self

    # ======== dhcp feature ========
    class DhcpService:

        def __init__(self, session):
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
            '''
            Args
                mode: dhcp server mode (pool or static pool).
                name: dhcp server name. Defaults to "dhcp_server".
                index: dhcp server index. Defaults to "1".
                action: dhcp server action (enable or disable).
            '''
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

        def __init__(self, session):
            self._s = session
            self._cmd = 'login-lockout'

        def lockout_toggle(self, toggle):
            if toggle is True:
                self._s.command_expect(f'{self._cmd}')
            else:
                self._s.command_expect(f'no {self._cmd}')

        def lockout_retryThreshold(self, retry):
            self._s.command_expect(f'{self._cmd} retry-threshold {retry}')

        def lockout_lockoutTime(self, duration):
            self._s.command_expect(f'{self._cmd} lockout-time {duration}')

    # ======== End of login lockout feature ========
    # ======== System Information feature ========
    class system_information:

        def __init__(self, session):
            self._s = session

    # ======== End of System Information feature ========
    # ======== time sync feature ========
    class TimeSync:

        def __init__(self, session):
            self._s = session

        def clock_source(self, clk_src, remote_server=None):
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
            if toggle is True:
                self._s.command_expect(f'ntp server')
            else:
                self._s.command_expect(f'no ntp server')

        def set_time_manually(self, year, month, day, hour, min, sec):
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

    def set_hostname(self, hostname):
        """
        Sets the hostname of the device.

            Args:
                hostname (str): The name of the device. 
        """
        self._s.command_expect(command=f'hostname {hostname}')

    def set_login_account(self, action, username, password, privilege=None):
        cmd = ""
        if username:
            cmd += f"username {username} "
        if password:
            cmd += f"password {password} "

        if privilege != None:
            if privilege == "admin":
                cmd += "privilege 1"
            elif privilege == "user":
                cmd += "privilege 2"
            elif privilege == "no login":
                cmd += "privilege 3"
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
                            min_len=None,
                            action=None,
                            global_complexity_check=None,
                            complexity_item=None):
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

    def set_log(self, log_item=None):
        log_list = ["trusted-access", "dos", "firewall"]
        if log_item in log_list:
            self._s.command_expect(f"logging {log_item}",
                                    prompts=[PROMPT_CONFIG])
        else:
            raise ValueError(f'input invalid log item: {log_item}')
        return self

    def set_syslog_server(self, action, ip, port=514):
        if action == "create":  # create server will enable itself as well
            ret = self._s.command_expect(f"logging {ip} {port}",
                                            prompts=['#'])
            if "Server list is full." in ret['data']:
                raise ValueError(f'Server list is full.')
        elif action in ["enable", "disable"]:
            self._s.command_expect(f"logging {ip} {port} {action}",
                                    prompts=[PROMPT_CONFIG])
        else:
            raise ValueError(f'input invalid action: {action}')

    def set_warning_notification(self,
                                    event,
                                    action=None,
                                    severity=None,
                                    active=None):
        action_type = {
            "Trap only": 1,
            "Email only": 2,
            "Trap+Email": 3,
            "Syslog only": 4,
            "Trap+Syslog": 5,
            "Email+Syslog": 6,
            "Trap+Email+Syslog": 7,
            "Relay1 only": 8,
            "Trap+Relay1": 9,
            "Email+Relay1": 10,
            "Trap+Email+Relay1": 11,
            "Syslog+Relay1": 12,
            "Trap+Syslog+Relay1": 13,
            "Email+Syslog+Relay1": 14,
            "Trap+Email+Syslog+Relay1": 15
        }  # the list goes on...
        event_type = [
            "cold-start", "warm-start", "pwr1-trans-on", "pwr2-trans-on",
            "pwr1-trans-off", "pwr2-trans-off", "auth-fail",
            "config-changed"
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
                            ip=None,
                            mask=None,
                            action=None,
                            global_toggle=None):
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
                self.command(f"interface trusted-access {ip} {mask}")
            elif action == "delete":
                self.command(f"no interface trusted-access {ip} {mask}")
            else:
                raise ValueError(f'input invalid action: {action}')

    def set_vlan_id(self, vlan_id):
        self._s.command_expect(f"vlan create {vlan_id}")
        return self

    def set_ip_ping_response(self):
        self._s.command_expect("ip ping-response")
        return self

    def set_ip_http_max_login_users(self, max_users):
        self._s.command_expect(
            f"ip http-server max-login-users {max_users}")
        return self

    def set_global_telnet(self, port=None, max_login_users=None):
        if port != None:
            self._s.command_expect(f"ip telnet port {port}")
        if max_login_users != None:
            self._s.command_expect(
                f"ip telnet max-login-users {max_login_users}")

    def set_firewall_rule_status(self, context, index, status):
        """
        Modify the status of a specified firewall rule.

        Args:
            index (int): The index of the firewall rule to modify.
            status (str): The status to set for the firewall rule. "enable" to enable the rule, "disable" to disable it.
        """
        self._s.command_expect(f"firewall {index} {status}")
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
            self._s.command_expect(f"vrrp 1 enable")
        else:
            raise ValueError(f"Input invalid status: {status}")
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

    class IgmpSnooping:
        """Class to configure Igmp Snooping.

            Args:
                session (object): An instance of the Session class.
        """

        def __init__(self, session: object):
            self._s = session

        def set_igmp_snooping_vlan(self, action: str, vid: str):
            """
             Enable or disable snooping for a VLAN.
             
             Args:
             	 action: 'enable'or'disable'.
             	 vid: VLAN ID.
            """
            if action == 'enable':
                self._s.command_expect(f"ip igmp-snooping vlan {vid}")
            elif action == 'disable':
                self._s.command_expect(f"no ip igmp-snooping vlan {vid}")
            else:
                raise ValueError(f'input invalid action')
            return self

        def set_igmp_snooping_querier(self, action: str, vid: str):
            """
             Enable or disable igmp snooping querier on a VLAN.
             
             Args:
             	 action: 'enable'or'disable'.
             	 vid: VLAN ID.
            """
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
            """
             Set IGMP snooping interval. Valid values are 20 - 600 seconds.
             
             Args:
             	 interval: interval in seconds between IGMP queries.
            """
            if 20 <= int(interval) <= 600:
                self._s.command_expect(
                    f"ip igmp-snooping query-interval {interval}")
            else:
                raise ValueError(f'input interval out of range')
            return self

        def set_global_igmp_snooping(self, action: str):
            """
             Enable / Disables global igmp snooping.
             
             Args:
             	 action: 'enable'or'disable'.
            """
            if action == 'enable':
                self._s.command_expect(f"ip igmp-snooping")
            elif action == 'disable':
                self._s.command_expect(f"no ip igmp-snooping")
            else:
                raise ValueError(f'input invalid action')
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
                vlan (str): Invalid for TN-5916.
        """
        self._s.command_expect(f'ip igmp static-group {mac} interface 1/{port}')
        return self   