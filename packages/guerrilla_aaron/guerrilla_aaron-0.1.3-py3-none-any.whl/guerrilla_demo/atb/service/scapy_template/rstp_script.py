from scapy.all import *
raw_data = bytes.fromhex("00" * {padding_n})
ether = Ether(src="{smac}", dst="{dmac}")

# 建立LLC封包
llc = LLC(dsap=0x42, ssap=0x42, ctrl=3)

# 建立Spanning Tree Protocol (STP)封包
stp = STP(proto=0, version=2, bpdutype=2, bpduflags=62,
          rootid=32768, rootmac="{smac}",
          pathcost=int({path_cost}), bridgeid=int({brid}), bridgemac="{smac}",
          portid=32770, age=0.0, maxage=int({max_age}), hellotime=int({hello_time}), fwddelay=int({fwd_delay}))

# 將封包組合在一起
rstp_packet = ether / llc / stp / Padding(load=raw_data)

# 送出VRRP封包
sendp(rstp_packet, iface="{iface}")