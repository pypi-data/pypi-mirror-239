from scapy.all import *
from scapy.contrib.igmp import IGMP
ip_packet = IP(src="{sip}", dst="{dip}")
raw_data = bytes.fromhex("00" * {padding_n})
packet = Ether() / ip_packet / {igmp_type} / Padding(load=raw_data)
packet[IGMP].gaddr = "{igmp_group_addr}"
packet = packet.__class__(bytes(packet))
sendp(packet, iface="{iface}", count={count})