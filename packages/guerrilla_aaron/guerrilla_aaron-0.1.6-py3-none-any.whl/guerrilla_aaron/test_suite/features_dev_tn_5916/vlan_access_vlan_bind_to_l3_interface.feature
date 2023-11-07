Feature: [Vlan] 
Purpose:
* Vlan 2 can be created well
* WAN interface binding vlan 2 can be accessed normally and operate local route well
Topology: 
+-----------------------------------------+
|  HOST_B------(LAN)DUT(WAN)------HOST_A  |
+-----------------------------------------+
| ip name | vlan | port       | ip address      | netmask       | default gateway |
| DUT lan | 1    | 1-7,9-16   | 192.168.127.254 | 255.255.255.0 | na              |
| DUT wan | 2    | 8          | 192.168.128.254 | 255.255.255.0 | na              | 
| HOST_B  | na   | nic-10     | 192.168.127.93  | 255.255.255.0 | 192.168.127.254 |
| HOST_A  | na   | nic-11     | 192.168.128.94  | 255.255.255.0 | 192.168.128.254 |

Background:
	Given authorize CLI of "DUT"
	* reload factory-default "DUT"
	* set system name to "DUT" on "DUT"
	* clear "DUT" all logging event log
	* prepare a "HOST_A" to connect to "DUT"
	* prepare a "HOST_B" to connect to "DUT"
@tn5916_v3 @bvt @sanity @vlan @ssh @self_testing
Scenario: Access Vlan Bind to L3 Interface
	When set default network on "LAN" interface and rename it as "HOST_B" on "DUT"
	And set network "wan_port" on "WAN" interface binding to VLAN "2" on "DUT"
	And set "HOST_A" ip address within "DUT"s WAN subnet
	And set "HOST_B" ip address within "DUT"s LAN subnet
	And add static route for "HOST_A" routing to "HOST_B"
	And add static route for "HOST_B" routing to "HOST_A" 
	# And enable WAN-Ping-Response on "DUT"
	#   *Please apply this step if your DUT support this feature
	# And disable trusted access on "DUT"
	#   *Please apply this step if your DUT's default setting of trusted access is enable
	And save configuration into flash on "DUT"
	Then show vlan including vlan id of "WAN" on "DUT"
	And "HOST_B" will ping "DUT wan" successfully
	And "HOST_A" will ping "DUT wan" successfully
	And "HOST_A" will ping "HOST_B" successfully