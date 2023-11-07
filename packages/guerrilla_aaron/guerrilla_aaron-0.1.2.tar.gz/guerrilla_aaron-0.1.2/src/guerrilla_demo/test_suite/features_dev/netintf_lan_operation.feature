Feature: [Netintf]
Topology
 +---------------------+
 |  HOST------(LAN)DUT |
 +---------------------+
    Background:
        Given prepare "network_interface" topology
        *     authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     clear "DUT" all logging event log
        *     prepare a "HOST" to connect to "DUT"
    @sanity @netintf @bvt @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: Operation of LAN Interface
        When  set LAN interface on "DUT"
        And   set "HOST" ip address within "DUT"s LAN subnet
        Then  "HOST" will ping "DUT LAN" successfully

        When  modify LAN ip address on "DUT"
              | lan             | mask          |
              | 192.168.129.254 | 255.255.255.0 |
        And   set "HOST" ip address within "DUT"s LAN subnet
              | lan             | mask          |
              | 192.168.129.94  | 255.255.255.0 |
        Then  "HOST" will ping "DUT LAN" successfully