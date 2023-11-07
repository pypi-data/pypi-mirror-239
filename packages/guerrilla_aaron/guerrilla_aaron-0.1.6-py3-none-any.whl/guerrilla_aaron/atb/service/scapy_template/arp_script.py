from scapy.all import *
import random
source_macs = {source_macs}
ips = {ips}
for source_mac, ip in zip(source_macs, ips):
    arp_request = Ether(src=source_mac, dst="ff:ff:ff:ff:ff:ff") / ARP(psrc=ip, pdst="{target_ip}")
    sendp(arp_request, iface='{nic}', count=1)