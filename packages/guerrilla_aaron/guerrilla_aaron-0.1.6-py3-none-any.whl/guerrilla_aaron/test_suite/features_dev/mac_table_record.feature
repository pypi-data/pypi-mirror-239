Feature: [MAC Table]
# Topology:
#  +----------------+
#  |  HOST------DUT |
#  +----------------+

	Background:
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     prepare a "HOST" to connect to "DUT"

    @sanity @mac_table @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: MAC table record
        # Note: Using ARP packet to trigger MAC address learning process in DUT. However, it is not the only method to verify the functionality of the MAC table.
        When  send 5 arp packet from "HOST" to "DUT"
        Then  mac entry should be recorded on "DUT" 

