Feature: [ARP Table]
Topology:
 +----------------+
 |  HOST------DUT |
 +----------------+
	Background: aging time
		Given authorize CLI of "DUT"
		*     reload factory-default "DUT"
		*     clear "DUT" all logging event log
		*     set WAN interface on "DUT"
              | wan            | mask          |
              | 192.168.0.254  | 255.255.0.0   |
        *     prepare a "HOST" to connect to "DUT"
		*     set "HOST" ip address within "DUT"s WAN subnet
			  | wan            | mask          |
              | 192.168.0.94   | 255.255.0.0   |

    @sanity @arp @edrg9010_v3 @edr8010_v3 @tn4900_v3
	Scenario: ARP table aging time
		When  send 129 arp packet from "HOST" to "DUT"
		Then  arp entry should be cleared within the aging time on "DUT"
			  | aging_time | remove_thershold |
			  | 70         | 129              |