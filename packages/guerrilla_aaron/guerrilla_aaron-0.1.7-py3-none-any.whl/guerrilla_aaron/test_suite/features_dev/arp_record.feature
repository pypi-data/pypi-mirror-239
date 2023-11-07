Feature: [ARP Table]
Topology:
 +----------------+
 |  HOST------DUT |
 +----------------+
	Background: ARP table record
		Given authorize CLI of "DUT"
		*     reload factory-default "DUT"
		*     clear "DUT" all logging event log
        *     prepare a "HOST" to connect to "DUT"
    @sanity @arp @self_testing @edrg9010_v3 @edr8010_v3 @tn4900_v3
	Scenario: ARP table record
		When  send 5 arp packet from "HOST" to "DUT"
		Then  arp entry should be recorded on "DUT"