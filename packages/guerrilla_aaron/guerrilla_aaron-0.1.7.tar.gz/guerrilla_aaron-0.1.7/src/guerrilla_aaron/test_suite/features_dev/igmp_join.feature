Feature: [IGMP]
Topology:
 +----------------+
 |  HOST------DUT |
 +----------------+
    Background:
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     clear "DUT" all logging event log
        *     prepare a "HOST" to connect to "DUT"
        *     set "HOST" ip address within "DUT"s LAN subnet
        *     "HOST" will ping "DUT LAN" successfully

    @sanity @igmp @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: Join Groups
        When  enable igmp-snooping v1/v2 with vlan 1 on "DUT"
        And   send igmp join with following format from "HOST" to "DUT"
              | dip       | igmp_group_addr |
              | 224.1.1.1 | 224.1.1.1       |
        Then  igmp group should be added on "DUT"
              | vid       | igmp_group_addr | version |
              | 1         | 224.1.1.1       | V2      |