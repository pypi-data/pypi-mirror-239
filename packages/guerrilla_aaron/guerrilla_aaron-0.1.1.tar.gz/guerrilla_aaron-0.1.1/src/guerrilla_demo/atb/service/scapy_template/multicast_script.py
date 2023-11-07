from scapy.all import *
import random

pkt = Ether(dst='{dst_mac}', src='{src_mac}')
sendp(pkt, iface='{nic}', count={pkt_count})