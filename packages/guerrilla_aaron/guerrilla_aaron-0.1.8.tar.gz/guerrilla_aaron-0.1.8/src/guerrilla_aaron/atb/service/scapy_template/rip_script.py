from scapy.layers.inet import IP, UDP, ICMP, TCP, ARP, Ether
from scapy.all import *

ripentries = {ripentries}
# 建立RIP Request封包
if "{rip_type}" == "request":
    packet = Ether(src="{smac}", dst="{dmac}") / IP(src="{sip}", dst="224.0.0.9") / UDP(dport=520, sport=520) / RIP(cmd=1, version=2,) / RIPEntry(AF=2, addr="0.0.0.0", mask="0.0.0.0", nextHop="0.0.0.0", metric=16)
# 建立RIP Response封包
elif "{rip_type}" == "response":
    ripentry = RIPEntry(AF=2, addr=ripentries[0]["addr"], mask=ripentries[0]["mask"], nextHop=ripentries[0]["nexthop"], metric=int(ripentries[0]["metric"]))
    for i in range(1, len(ripentries)):
        ripentry /= RIPEntry(AF=2, addr=ripentries[i]["addr"], mask=ripentries[i]["mask"], nextHop=ripentries[i]["nexthop"], metric=int(ripentries[i]["metric"]))
    packet = Ether(src="{smac}", dst="{dmac}") / IP(src="{sip}", dst="224.0.0.9") / UDP(dport=520, sport=520) / RIP(cmd=2,version=2) / ripentry

# 發送RIP Request封包
sendp(packet, iface="{iface}")
