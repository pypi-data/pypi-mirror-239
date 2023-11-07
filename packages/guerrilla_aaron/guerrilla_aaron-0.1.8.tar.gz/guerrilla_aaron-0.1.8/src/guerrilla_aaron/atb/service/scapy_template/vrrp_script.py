from scapy.all import *
raw_data = bytes.fromhex("00" * {padding_n})
# 建立VRRP封包
vrrp_packet = Ether(src="{smac}", dst="{dmac}") \
            / IP(src="{sip}", dst="{dip}", ttl=255) \
            / VRRPv3(version={version}, priority={priority}) \
            / Padding(load=raw_data)
ip_address = "{ip_address}"  # 要添加的IP地址
vrrp_packet[VRRPv3].addrlist = ip_address.split(",")

# 送出VRRP封包
sendp(vrrp_packet, iface="{iface}")