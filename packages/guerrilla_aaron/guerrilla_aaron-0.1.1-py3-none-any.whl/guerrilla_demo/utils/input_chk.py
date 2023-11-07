import re

IPV4_REGEXP = r'^([1-9]|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])(\.(0|[1-9]|[1-9]\d|1\d{2}|2[0-4]\d|25[0-5])){3}$'
MAC_REGEXP = r'^[a-fA-F0-9]{2}(?:[:-]?[a-fA-F0-9]{2}){5}(?:,[a-fA-F0-9]{2}(?:[:-]?[a-fA-F0-9]{2}){5})*$'


def chk_valid_ip(ip):
    rtv4 = None
    rtv6 = None
    try:
        chk_valid_ipv4(ip)
    except:
        rtv4 = False
    else:
        rtv4 = True
    try:
        chk_valid_ipv6(ip)
    except:
        rtv6 = False
    else:
        rtv6 = True
    if (rtv4 | rtv6) is False:
        raise ValueError('Invalid IP address')


def chk_valid_ipv4(ipv4):
    if re.search(IPV4_REGEXP, ipv4) is None:
        raise ValueError('Invalid IPv4 address')


def chk_valid_ipv6(ipv6):
    raise ValueError('No implementation yet')


def chk_is_private_ip(ip) -> bool:
    return chk_is_private_ipv4(ip) or chk_is_private_ipv6(ip)


def chk_is_private_ipv4(ipv4) -> bool:
    try:
        chk_valid_ipv4(ipv4)
    except:
        return False
    """
    Private IP range: 
    Class A: 10.0.0.0 ~ 10.255.255.255
    Class B: 172.16.0.0 ~ 172.31.255.255
    Class C: 192.168.0.0 ~ 192.168.255.255
    """
    ipv4_parted = ipv4.split('.')
    if int(ipv4_parted[0]) == 10:
        # Class A
        return True
    elif (int(ipv4_parted[0]) == 172) and (int(ipv4_parted[1]) >= 16 and
                                           int(ipv4_parted[1]) <= 31):
        # Class B
        return True
    elif int(ipv4_parted[0]) == 192 and int(ipv4_parted[1]) == 168:
        # Class C
        return True
    else:
        # non-private IP
        return False


def chk_is_private_ipv6(ipv6) -> bool:
    try:
        chk_valid_ipv6(ipv6)
    except:
        return False

    # TODO
    """
    Private IP block: 
    fd00::/8
    """


def chk_valid_mac(mac_addr):
    if re.search(MAC_REGEXP, mac_addr) is None:
        raise ValueError('Invalid MAC address')
