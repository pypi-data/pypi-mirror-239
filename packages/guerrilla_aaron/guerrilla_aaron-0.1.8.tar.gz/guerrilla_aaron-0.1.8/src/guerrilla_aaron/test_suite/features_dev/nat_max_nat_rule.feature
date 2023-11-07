Feature: [NAT]

	#Purpose: 在DUT存在最大組數的NAT rule情況下，trigger第一條、中間、最後一條的firewall rule
	#
	#e.g 假設目前存在1024條NAT rule，而打的封包只match第1, 512, 1024條NAT rule
	#
	#Checkpoint:
	#
	## 確保match第1條NAT Rule的Traffic可以通過DUT
	## 確保match第1條NAT Rule的Traffic有成功被轉址
	## 確保match第512條NAT Rule的Traffic可以通過DUT
	## 確保match第512條NAT Rule的Traffic有成功被轉址
	## 確保match第1024條NAT Rule的Traffic可以通過DUT
	## 確保match第1024條NAT Rule的Traffic有成功被轉址
	Background:
		Given authorize CLI of "DUT"
		And   reload factory-default "DUT"
		And   set WAN interface on "DUT"
		    | wan_vlan | wan             | mask          |
		    | 2        | 192.168.128.253 | 255.255.255.0 |
		And   prepare a "HOST_A" to connect to "DUT"
		And   prepare a "HOST_B" to connect to "DUT"
		And   set "HOST_A" ip address within "DUT"s WAN subnet
		    | wan             | mask          |
		    | 192.168.128.100 | 255.255.255.0 |
		And   set "HOST_B" multiple ip address within "DUT"s LAN subnet
		    | lan            | mask          |
		    | 192.168.127.10 | 255.255.255.0 |
		    | 192.168.127.20 | 255.255.255.0 |
		    | 192.168.127.30 | 255.255.255.0 |
		And   add static route for "HOST_A" routing to "HOST_B"
		And   add static route for "HOST_B" routing to "HOST_A"

	@sanity @nat @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
	Scenario: Max NAT Rule
		# Topology:
		#     +-------------------------------------+
		#     |  HOST_A--(WAN)--dut--(LAN)--HOST_B  |
		#     +-------------------------------------+
		#     dut WAN IP addr: 192.168.128.254/24
		#     dut LAN IP addr: 192.168.127.254/24
		Given set 1-1 nat rule on "DUT"
		    | nat_indexes | nat_iface | nat_dest_ip    | real_dest_ip   |
		    | 1           | WAN       | 192.168.128.10 | 192.168.127.10 |
		    | 2-255       | WAN       | 192.168.128.66 | 192.168.127.66 |
		    | 256         | WAN       | 192.168.128.20 | 192.168.127.20 |
		    | 257-511     | WAN       | 192.168.128.66 | 192.168.127.66 |
		    | 512         | WAN       | 192.168.128.30 | 192.168.127.30 |
		And   starts tshark sniffer on "HOST_B"
		When  "HOST_A" send some icmp echo request packets for each destination IP
		    | pkt_num | nat_dest_ip    |
		    | 5       | 192.168.128.10 |
		    | 10      | 192.168.128.20 |
		    | 15      | 192.168.128.30 |
		Then  check "HOST_B" receive some icmp echo request packets with destination IP
		    | pkt_num | real_dest_ip   |
		    | 5       | 192.168.127.10 |
		    | 10      | 192.168.127.20 |
		    | 15      | 192.168.127.30 |
