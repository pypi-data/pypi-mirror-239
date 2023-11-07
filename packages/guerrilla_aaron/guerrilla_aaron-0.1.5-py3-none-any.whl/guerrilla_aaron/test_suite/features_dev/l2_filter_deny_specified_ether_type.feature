Feature: [Firewall - L2 Policy]

	#Purpose: 確保ether type可正常作用
	#
	#Checkpoint:
	#
	## 當traffic的ether type符合設定的ether type時，可成功被filter
	## 當traffic的ether type不符合設定的ether type時，不會被filter
	@sanity @l2-filter @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
	Scenario: Deny Specified Ether Type
		# Topology:
		#     +-------------------------------------------------------+
		#     |  HOST_A--(Bridge-Port8)--dut--(Bridge-Port1)--HOST_B  |
		#     +-------------------------------------------------------+
		#     DUT Bridge IP address: 192.168.126.254/24

		# Background
		Given authorize CLI of "DUT"
		And   reload factory-default "DUT"
		And   set BRG interface on "DUT"
		And   prepare a "HOST_A" to connect to "DUT"
		And   prepare a "HOST_B" to connect to "DUT"
		And   set "HOST_A" ip address within "DUT"s BRG subnet
		And   set "HOST_B" ip address within "DUT"s BRG subnet

		# Scenario for TCR-678
		## make sure network works
		When  starts tshark sniffer on "HOST_B"
		And   "HOST_A" send 5 ICMP ping to "HOST_B"
		Then  "HOST_B" shall receive 5 ICMP request from "HOST_A"

		Given l2-policy install on "DUT"
		      | src_mac  | dst_mac  | ethertype | action |
		      | all      | all      | 0x0800    | drop   |

		## check point 1
		When  starts tshark sniffer on "HOST_B"
		And   "HOST_A" send 5 ICMP ping to "HOST_B"
		Then  "HOST_B" shall receive 0 ICMP request from "HOST_A"

		## check point 2
		When  starts tshark sniffer on "HOST_B"
		And   "HOST_A" send 5 ARP probe to "HOST_B"
		Then  "HOST_B" shall receive 5 ARP probe from "HOST_A"
