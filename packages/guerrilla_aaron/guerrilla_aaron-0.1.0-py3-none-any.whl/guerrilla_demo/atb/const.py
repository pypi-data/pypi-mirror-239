from atb.service import *

def list_control_type_names():
    """
        list_control_type_names() -> list
        Return a list of control type names from the CONTROL_TYPE_MAP.
    """
    return list(CONTROL_TYPE_MAP)


def get_control_class(type_name):
    """
    Returns the control class associated with the given type name.

        Parameters:
            type_name (str): The name of the control type.

        Returns:
            class: The control class associated with the given type name. 
    """
    return CONTROL_TYPE_MAP[type_name]


CONTROL_TYPE_MAP = {
    'shellcmd':    ShellCmdService,
    'hping3':      Hping3Service,
    'tftp':        TftpService,
    'trex':        TrexService,
    'tshark':      TsharkService,
    'tcp_tool':    PktMgmtService,
    'syslog':      SyslogService,
    'trex_console':TrexConsoleService,
    'trex_server': TrexServerService,
    'scapy':       ScapyService,
    'dut_ui':      UICtrlService,
    'ca':          CaService,
    'bird':        BirdService,
    'nmcli':       NetworkManagerService,
    'radius':      RadiusService, 
    'snmp':        SnmpService,
    'mail_server': MailServerService
}