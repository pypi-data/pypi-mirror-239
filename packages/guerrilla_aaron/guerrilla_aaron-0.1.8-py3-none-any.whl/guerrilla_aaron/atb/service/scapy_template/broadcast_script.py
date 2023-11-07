from scapy.all import Ether, IP, UDP, sendp

eth_frame = Ether( dst="ff:ff:ff:ff:ff:ff")

ip_packet = IP(src="{sip}", dst="{dip}")

udp_packet = UDP(dport={dport}) / "Broadcast message yaaaaa"

packet = eth_frame / ip_packet / udp_packet

sendp(packet, iface="{iface}", count={count})