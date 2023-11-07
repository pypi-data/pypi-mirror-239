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
    Scenario: Querier Election
        When  set igmp-snooping query interval to 20 on "DUT"
        And   enable igmp-snooping v1/v2 with vlan 1 on "DUT"
        And   send igmp query with following format from "HOST" to "DUT"
              | dip       | igmp_group_addr |
              | 224.0.0.1 | 0.0.0.0         |
        Then  querier will be changed from "DUT" to "HOST"
        When  modify LAN ip address on "DUT"
              | lan             | mask          |
              | 192.168.127.10  | 255.255.255.0 |
        And   disable igmp-snooping v1/v2 with vlan 1 on "DUT"
        And   enable igmp-snooping v1/v2 with vlan 1 on "DUT"
        And   send igmp query with following format from "HOST" to "DUT"
              | dip       | igmp_group_addr |
              | 224.0.0.1 | 0.0.0.0         |
        Then  querier will be changed from "HOST" to "DUT"