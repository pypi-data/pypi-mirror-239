Feature: [LLDP]

Topology:
 +----------------------+
 | DUT(WAN)------HOST_A |
 +----------------------+
    @sanity @lldp @edrg9010_v3 @edr8010_v3 @tn4900_v3 @skip
    Scenario: LLDP Enable / Disable
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     prepare a "HOST_A" to connect to "DUT"
        *     set WAN interface on "DUT"
        *     set "HOST_A" ip address within "DUT"s WAN subnet
        When  enable LLDP on "DUT"
        And   set transmission freqency of LLDP updates to 5 sec on "DUT"
        And   starts tshark sniffer on "HOST_A" for LLDP packet
        Then  "HOST_A" shall receive LLDP packet from "DUT" within 10 sec

        When  disable LLDP on "DUT"
        And   starts tshark sniffer on "HOST_A" for LLDP packet
        Then  "HOST_A" shall not receive LLDP packet from "DUT" within 10 sec