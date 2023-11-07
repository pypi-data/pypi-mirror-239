Feature: [DHCP]
Topology:
 +----------------+
 |  HOST------DUT |
 +----------------+
	Background:
		Given prepare "default" topology
		*     authorize CLI of "DUT"
		*     reload factory-default "DUT"
		*     prepare a "HOST" to connect to "DUT"
	Scenario Outline: DHCP/MAC-based/Port-based assignment
		Given enable dhcp service on "DUT"
		*     set configuration of <mode> dhcp server on "DUT" for dispatching ip to "HOST"
		      | mode       | pool_ip_begin  | pool_ip_end     | ip_host        | mask          | default_gw      | lease_time | port |
		      | dhcp       | 192.168.127.1  | 192.168.127.92  | N/A            | 255.255.255.0 | 192.168.127.254 | 1440       | N/A  |
		      | mac-based  | N/A            | N/A             | 192.168.127.94 | 255.255.255.0 | 192.168.127.254 | 1440       | N/A  |
		When  enable dhcp client in "HOST"
		Then  "HOST" can receive ip address from <mode> server
              | pool_ip_begin | pool_ip_end    | ip_host        |
              | 192.168.127.1 | 192.168.127.92 | 192.168.127.94 |
		And   "DUT" can ping "HOST"s received ip address 
	
    @sanity @dhcp @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Examples:
	| mode       |
	| dhcp       |
	| mac-based  |
