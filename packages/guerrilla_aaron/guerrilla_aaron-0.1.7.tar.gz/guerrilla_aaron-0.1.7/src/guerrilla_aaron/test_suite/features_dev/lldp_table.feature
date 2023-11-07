Feature: [LLDP]

Topology:
 +----------------------+
 | HOST_B------(LAN)DUT |
 +----------------------+
    @sanity @lldp @edrg9010_v3 @edr8010_v3 @tn4900_v3 @skip
    Scenario: LLDP table
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     prepare a "HOST_B" to connect to "DUT"
        *     set LAN interface on "DUT"
        *     set "HOST_B" ip address within "DUT"s LAN subnet
        When  enable LLDP on "DUT"
        And   "HOST_B" send 1 LLDP packet with extentions and following values
              | Chasis_id | Port_id |
              | test001   | tPortId |
        Then  the LLDP table on "DUT" should contain an entry with corresponding port, neighbor id, and neighbor port