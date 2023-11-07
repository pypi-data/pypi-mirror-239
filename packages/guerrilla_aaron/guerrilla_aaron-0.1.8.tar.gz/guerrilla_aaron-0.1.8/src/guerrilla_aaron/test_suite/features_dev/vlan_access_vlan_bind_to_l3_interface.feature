Feature: [Vlan]

	Background:
		#@PRECOND_TCR-665
		Given authorize CLI of "DUT"
		* reload factory-default "DUT"
		* set system name to "DUT" on "DUT"
		* clear "DUT" all logging event log
        * prepare a "HOST_A" to connect to "DUT"
        * prepare a "HOST_B" to connect to "DUT"
	#[Aaron]
	#
	#Purpose: 確保vlan可以正常被新增
	#Checkpoint:
	#1. vlan有被新增
	#2. 新增的vlan有作用 (例如綁定一個interface，並確保此interface有作用)
	@bvt @sanity @vlan @self_testing @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
	Scenario: Access Vlan Bind to L3 Interface
        When set default network on "LAN" interface and rename it as "HOST_A" on "DUT"
        And  set network "wan_port" on "WAN" interface binding to VLAN "2" on "DUT"
        And  set "HOST_A" ip address within "DUT"s WAN subnet
        And  set "HOST_B" ip address within "DUT"s LAN subnet
        And  add static route for "HOST_A" routing to "HOST_B"
        And  add static route for "HOST_B" routing to "HOST_A"
		And  enable WAN-Ping-Response on "DUT"
		And  disable trusted access on "DUT"
		And  save configuration into flash on "DUT"
		Then show vlan including vlan id of "WAN" on "DUT"  
        And "HOST_B" will ping "DUT wan" successfully
        And "HOST_A" will ping "DUT wan" successfully
        And "HOST_A" will ping "HOST_B" successfully

