import os
import time
import textfsm

from guerrilla_aaron.mdc.router.cli.rp_parser.edrg9010_v2_0.parser import parse_colon_fields
# execute __init__.py for inheritance
from guerrilla_aaron.mdc.router.cli.rp_parser import edrg9010_v3_0, edrg9010_v2_0, oncellg4302_v3_0, tn5916_v3_0, tn5916_v3_0_27, edr810_v5_0, edr8010_v3_0
from session import PROMPTS

dirname = os.path.dirname(__file__)

def ping(session: object, host, model: str):
    """
    Execute the 'ping' command on a Moxa NG router and parse the output using TextFSM.

        Args:
            session (object): The session object to use for the ping command.
            host (str): The host to ping.
            model (str): The model of the device.
            
        Returns: 
            dict: A dictionary containing the parsed output of the ping command. 
    """
    filename = os.path.join(
        dirname, f'{model.__name__}/moxa_ng_router_show_ping.textfsm')
    ret = session.command_expect(f'ping {host}',
                                 prompts=["Lost"],
                                 exact_str=True,
                                 timeout=30)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    return res[0]


def show_version(session: object, model: str):
    """
    Execute the 'show version' command on a Moxa NG router and parse the output using TextFSM.

        Args: 
            session (object): The session object to use for connecting to the device. 
            model (str): The model of the device. 
            
        Returns: 
            res (list): A list of dictionaries containing the version information. 
    """
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_version.textfsm')
    ret = session.command_expect('show version',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 exact_str=True,
                                 timeout=1)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    return res


def show_system(session: object, model: str):
    """
    Execute the 'show system' command on a Moxa NG router and parse the output using TextFSM.

        Args:
            session (object): An instance of Session object.
            model (str): The model of the Moxa NG router.

        Returns:
            list: A list of dictionaries containing the parsed output from the 'show system' command. 
    """
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_system.textfsm')
    ret = session.command_expect('show system',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 exact_str=True,
                                 timeout=1)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    return res


def show_package(session: object, model: str):
    """
    Execute the 'show package' command on a Moxa NG router and parse the output using TextFSM.

        Args:
            session (object): An instance of Session object.
            model (str): The model of the Moxa NG router.

        Returns:
            list: A list of dictionaries containing the parsed output from the 'show system' command. 
    """
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_package.textfsm')
    ret = session.command_expect('show package',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 exact_str=True,
                                 timeout=1)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    return res


def show_dos(session: object, model: str):
    """
    Execute the 'show dos' command on a Moxa NG router and parse the output using TextFSM.

        Args:
            session (object): An instance of Session object.
            model (str): The model of the Moxa NG router.

        Returns:
            list: A list of dictionaries containing the parsed output from the 'show dos' command.
    """
    filename = os.path.join(
        dirname, f'{model.__name__}/moxa_ng_router_show_dos.textfsm')
    ret = session.command_expect('show dos',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 exact_str=True,
                                 timeout=1)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    return res


def show_interface(session: object, name: str, model: str, vid=None):
    """
    Execute the 'show interface' command on a Moxa NG router and parse the output using TextFSM.

        Args:
            session (object): An instance of the Netmiko class.
            name (str): The name of the interface to show.
            model (str): The model of the router.
            vid (int, optional): The VLAN ID associated with the interface. Defaults to None. 
            
        Returns:
            list: A list of dictionaries containing the parsed output from the router. 
    """
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_interface_{name.lower()}.textfsm'
    )
    if vid == None:
        ret = session.command_expect(f'show interface {name.lower()}',
                                     prompts=PROMPTS["ALL"]["MAIN"],
                                     exact_str=True,
                                     timeout=5)
    else:
        ret = session.command_expect(f'show interface {name.lower()} {vid}',
                                     prompts=PROMPTS["ALL"]["MAIN"],
                                     exact_str=True,
                                     timeout=5)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    return res


# this just only router v1.2 can use so create new show_vlan function and use textfsm
# def show_vlan(session: object, model: str):
#     ret = session.command_expect('show vlan', parse_colon_fields_structure)
#     return ret['data']

def show_arp(session: object, model: str):
    """
    Execute the 'show vlan' command on a Moxa NG router and parse the output using TextFSM.

        Args: 
            session (object): Session object to execute the command on. 
            model (str): Model of the device for which to use the TextFSM template. 
            
        Returns: 
            dict: Parsed data from 'show vlan' command in form of a dictionary. 
    """
    filename = os.path.join(
        dirname, f'{model.__name__}/moxa_ng_router_show_arp.textfsm')
    session.command('terminal length 0')
    ret = session.command_expect('show arp',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 exact_str=True,
                                 timeout=5)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    return res


def show_mac_address_table(session: object, model: str):
    """
    Execute the 'show mac-address-table' command on a Moxa NG router and parse the output using TextFSM.

        Args: 
            session (object): Session object to execute the command on. 
            model (str): Model of the device for which to use the TextFSM template. 
            
        Returns: 
            dict: Parsed data from 'show mac-address-table' command in form of a dictionary. 
    """
    filename = os.path.join(
        dirname, f'{model.__name__}/moxa_ng_router_show_mac_address_table.textfsm')
    ret = session.command_expect('show mac-address-table',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 exact_str=True,
                                 timeout=5)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    return res


def show_vlan(session: object, model: str):
    """
    Execute the 'show vlan' command on a Moxa NG router and parse the output using TextFSM.

        Args: 
            session (object): Session object to execute the command on. 
            model (str): Model of the device for which to use the TextFSM template. 
            
        Returns: 
            dict: Parsed data from 'show vlan' command in form of a dictionary. 
    """
    filename = os.path.join(
        dirname, f'{model.__name__}/moxa_ng_router_show_vlan.textfsm')
    # session.command('terminal length 0')
    ret = session.command_expect('show vlan',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 exact_str=True,
                                 timeout=5)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    return res


def show_clock(session: object, model: str):
    """
    Execute the 'show clock' command on a Moxa NG router and parse the output using TextFSM.

        Args:
            session (Session): An established session object to the device.
            model (str): The device model type.

        Returns:
            dict: A dictionary containing the system clock information. 
    """
    ret = session.command_expect('show clock', parse_colon_fields)
    return ret['data']

def show_ip_route(session: object, model: str):
    """
    Execute the 'show ip route' command on a Moxa NG router and parse the output using TextFSM.

        Args:
            session (Session): An established session object to the device.
            model (str): The device model type.

        Returns:
            list[dict]: A list of dictionaries containing the IP routing table information. 
    """
    from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000.base import Base as tn5000
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_ip_route.textfsm')
    if issubclass(model, tn5000):
        ret = session.command_expect('show ip route',
                                     prompts=PROMPTS["ALL"]["MAIN"],
                                     timeout=5)
        with open(filename) as template:
            fsm = textfsm.TextFSM(template)
            res = fsm.ParseTextToDicts(ret['data'])
    else:
        session.command('terminal length 0')
        ret = session.command_expect('show ip route',
                                     prompts=PROMPTS["ALL"]["MAIN"],
                                     exact_str=True,
                                     timeout=5)
        with open(filename) as template:
            fsm = textfsm.TextFSM(template)
            res = fsm.ParseTextToDicts(ret['data'])
    return res

def show_ip_igmp(session: object, model: str):
    """
    Execute the 'show ip igmp' command on a Moxa NG router and parse the output using TextFSM.

        Args:
            session (Session): An established session object to the device.
            model (str): The device model type.

        Returns:
            list[dict]: A list of dictionaries containing the IP routing table information. 
    """
    from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000.base import Base as tn5000
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_ip_igmp.textfsm')
    if issubclass(model, tn5000):
        ret = session.command_expect('show ip igmp',
                                     prompts=PROMPTS["ALL"]["MAIN"],
                                     timeout=5)
        with open(filename) as template:
            fsm = textfsm.TextFSM(template)
            res = fsm.ParseTextToDicts(ret['data'])
    else:
        ret = session.command_expect('show ip igmp',
                                     prompts=PROMPTS["ALL"]["MAIN"],
                                     exact_str=True,
                                     timeout=5)
        with open(filename) as template:
            fsm = textfsm.TextFSM(template)
            res = fsm.ParseTextToDicts(ret['data'])
    return res

def show_trusted_access(session: object, model: str):
    """
    Execute the 'show interface trusted-access' command on a Moxa NG router and parse the output using TextFSM.

        Args:
            session (object): The session object to connect to the device.
            model (str): The model of the device.

        Returns:
            res (dict): A dictionary containing the trusted access information. 
    """
    from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000.base import Base as tn5000
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_trusted_access.textfsm'
    )
    if issubclass(model, tn5000):
        ret = session.command_expect('show interface trusted-access',
                                    prompts=PROMPTS["ALL"]["MAIN"],
                                    exact_str=True,
                                    timeout=5)
        with open(filename) as template:
            fsm = textfsm.TextFSM(template)
            res = fsm.ParseTextToDicts(ret['data'])
    else:
        # session.command('terminal length 0')
        ret = session.command_expect('show interface trusted-access',
                                    prompts=PROMPTS["ALL"]["MAIN"],
                                    exact_str=True,
                                    timeout=5)
        with open(filename) as template:
            fsm = textfsm.TextFSM(template)
            res = fsm.ParseTextToDicts(ret['data'])
    return res


def show_l37_policy(session: object, model: str):
    """
    Execute the 'show l3l7-policy' command on a Moxa NG router and parse the output using TextFSM.

        Args:
            session (object): The session object to connect to the device.
            model (str): The model of the device.

        Returns:
            res (dict): A dictionary containing the L3/L7 policy information. 
    """
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_l3l7-policy.textfsm')
    session.command('terminal length 0')
    ret = session.command_expect('show l3l7-policy',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 exact_str=True,
                                 timeout=5)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    return res

def show_vrrp(session: object, model: str):
    """
    Execute the 'show vrrp detail' command on a Moxa NG router and parse the output using TextFSM.

        Args:
            session (object): The session object to connect to the device.
            model (str): The model of the device.

        Returns:
            res (dict): A dictionary containing the vrrp information. 
    """
    from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000.base import Base as tn5000
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_vrrp.textfsm')
    if issubclass(model, tn5000):
        ret = session.command_expect('show ip vrrp',
                                    prompts=PROMPTS["ALL"]["MAIN"],
                                    exact_str=True,
                                    timeout=5)
    else:
        ret = session.command_expect('show vrrp detail',
                                    prompts=PROMPTS["ALL"]["MAIN"],
                                    exact_str=True,
                                    timeout=5)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    return res

def show_logging_event_log_dos(session: object, model: str):
    """
    Execute the 'show logging event-log dos' command on a Moxa NG router and parse the output using TextFSM.

        Args:
            session (object): The session object to connect to the device.
            model (str): The model of the device.

        Returns:
            res (dict): A dictionary containing DOS event log information.
    """
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_logging_event_log_dos.textfsm'
    )
    session.command('terminal length 0')
    ret = session.command_expect('show logging event-log dos',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 exact_str=True,
                                 timeout=5)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    return res


def show_logging_event_log_l3l7(session: object, model: str):
    """
    Execute the 'show logging event-log l3l7-policy' command on a Moxa NG router and parse the output using TextFSM.

    Args: 
        session (object): The session object used to execute the command. 
        model (str): The model of the router. 

    Returns: 
        res (dict): A dictionary containing the parsed output of the command.
    """
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_logging_event_log_l3l7-policy.textfsm'
    )
    session.command('terminal length 0')
    ret = session.command_expect('show logging event-log l3l7-policy',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 exact_str=True,
                                 timeout=5)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    session.command_expect('', prompts=PROMPTS["ALL"]["MAIN"])
    return res


def show_logging_event_log_firewall(session: object, model: str):
    """
    Execute the 'show logging event-log firewall' command on a Moxa NG router and parse the output using TextFSM.

        Args:
            session (object): A Session object to execute commands on.
            model (class): The model class to use for the device.
            
        Returns:
            list: A list of dictionaries containing the parsed output from the command. 
    """
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_logging_event_log_firewall.textfsm'
    )
    ret = session.command_expect('show logging event-log firewall',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 timeout=5)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    session.command_expect('', prompts=PROMPTS["ALL"]["MAIN"])
    return res


def show_logging_event_log_system(session: object, model: str):
    """
    Execute the 'show users' command on a Moxa NG router and parse the output using TextFSM.

        Args: 
            session (object): Paramiko SSH session object. 
            model (str): Model of the Moxa NG router. 
            
        Returns: 
            res (dict): A dictionary containing the user accounts information. 
    """
    from guerrilla_aaron.mdc.router.cli.rp_base.lg_router.tn5000.base import Base as tn5000
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_logging_event_log_system.textfsm'
    )
    time.sleep(5)
    if issubclass(model, tn5000):
        logs = ""
        ret = session.command_expect('show logging event-log system',
                                     prompts=PROMPTS["ALL"]["MAIN"],
                                     timeout=5)
        logs += ret['data']
        while ret['matched'] == False:
            ret = session.command_expect('',
                                         prompts=PROMPTS["ALL"]["MAIN"],
                                         timeout=1)
            logs += ret['data']
        with open(filename) as template:
            fsm = textfsm.TextFSM(template)
            res = fsm.ParseTextToDicts(logs.replace('\r\n--More--', '\n'))
    else:
        session.command('terminal length 0')
        ret = session.command_expect('show logging event-log system',
                                     prompts=PROMPTS["ALL"]["MAIN"],
                                     exact_str=True,
                                     timeout=5)
        with open(filename) as template:
            fsm = textfsm.TextFSM(template)
            res = fsm.ParseTextToDicts(ret['data'])
    return res


def show_logging_event_log_malformed(session: object, model: str):
    """
    Execute the 'show logging event-log malformed' command on a Moxa NG router and parse the output using TextFSM.

        Args:
            session (object): A Session object to execute commands on.
            model (class): The model class to use for the device.
            
        Returns:
            list: A list of dictionaries containing the parsed output from the command. 
    """
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_logging_event_log_malformed.textfsm'
    )
    ret = session.command_expect('show logging event-log malformed',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 exact_str=True,
                                 timeout=5)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    return res
    

def show_user_accounts(session: object, model: str):
    """
    Execute the 'show users' command on a Moxa NG router and parse the output using TextFSM.

        Args: 
            session (object): Paramiko SSH session object. 
            model (str): Model of the Moxa NG router. 
            
        Returns: 
            res (dict): A dictionary containing the user accounts information. 
    """
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_user_accounts.textfsm')
    ret = session.command_expect('show users',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 exact_str=True,
                                 timeout=5)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    return res


def show_object(session: object, model: str):
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_object.textfsm')
    ret = session.command_expect('show object',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 exact_str=True,
                                 timeout=5)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    res = list(map(lambda x: dict(x, **{'detail': x['detail'].rstrip()}), res))
    return res


def show_session_ctrl(session: object, model: str):
    filename = os.path.join(dirname,
        f'{model.__name__}/moxa_ng_router_show_session_ctrl.textfsm')
    ret = session.command_expect('show session-control',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 exact_str=True,
                                 timeout=5)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
        res = list(
            map(lambda x: dict(x, **{'session_name': x['session_name'].rstrip(), 'index': x['index'].rstrip()}), res))
    return res

def show_lldp_table(session: object, model:str):
    filename = os.path.join(dirname,
        f'{model.__name__}/moxa_ng_router_show_lldp_table.textfsm')
    ret = session.command_expect('show lldp entry',
                                 prompts=[r'# '],
                                 exact_str=True,
                                 timeout=5)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
        res = list(map(lambda item: {k: v.rstrip() for k, v in item.items()}, res))
    return res

def show_rstp(session: object, model: str):
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_rstp.textfsm')
    ret = session.command_expect('show redundancy spanning-tree',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 exact_str=True,
                                 timeout=5)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    return res

def show_rstp_port(session: object, model: str):
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_rstp_port.textfsm')
    ret = session.command_expect('show redundancy spanning-tree',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 exact_str=True,
                                 timeout=5)
    # spilt ret to parse port information
    split_index = ret['data'].find("Int#")
    ret['data'] = ret['data'][split_index:]

    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    return res

def show_ip_ospf_interface(session: object, model: str):
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_ip_ospf_interface.textfsm')
    ret = session.command_expect('show ip ospf interface',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 exact_str=True,
                                 timeout=5)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    return res

def show_ip_ospf_neighbor(session: object, model: str):
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_ip_ospf_neighbor.textfsm')
    ret = session.command_expect('show ip ospf neighbor',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 exact_str=True,
                                 timeout=5)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    return res

def show_ip_ospf_database(session: object, model: str):
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_ip_ospf_database.textfsm')
    ret = session.command_expect('show ip ospf database',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 exact_str=True,
                                 timeout=5)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    return res

def show_l2tp_setting(session: object, model: str):
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_l2tp.textfsm')
    ret = session.command_expect('show l2tp',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 exact_str=True,
                                 timeout=5)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    return res

def show_snmp(session: object, model: str):
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_snmp.textfsm')
    ret = session.command_expect('show snmp',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 exact_str=True,
                                 timeout=5)
    
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    return res

def show_fast_bootup(session: object, model: str):
    """
    Execute the 'show version' command on a Moxa NG router and parse the output using TextFSM.

        Args: 
            session (object): The session object to use for connecting to the device. 
            model (str): The model of the device. 
            
        Returns: 
            res (list): A list of dictionaries containing the version information. 
    """
    filename = os.path.join(
        dirname,
        f'{model.__name__}/moxa_ng_router_show_fast_bootup.textfsm')
    ret = session.command_expect('show fast-bootup',
                                 prompts=PROMPTS["ALL"]["MAIN"],
                                 exact_str=True,
                                 timeout=1)
    with open(filename) as template:
        fsm = textfsm.TextFSM(template)
        res = fsm.ParseTextToDicts(ret['data'])
    return res