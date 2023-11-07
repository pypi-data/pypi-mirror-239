Feature: [Netintf]
Topology:
 +---------------------+
 |  HOST------(LAN)DUT |
 +---------------------+
    Background:
        Given prepare "network_interface" topology
        *     authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     clear "DUT" all logging event log
        *     prepare a "HOST" to connect to "DUT"
        *     set LAN interface on "DUT"
        *     set "HOST" ip address within "DUT"s LAN subnet
    @sanity @netintf @bvt @self_testing @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: LAN Interface - Configuration Import/Export 
        When  modify LAN ip address on "DUT"
              | lan             | mask          |
              | 192.168.127.253 | 255.255.255.0 |
        And   set "HOST" ip address within "DUT"s LAN subnet
              | lan             | mask          |
              | 192.168.127.94  | 255.255.255.0 |
        Then  "HOST" will ping "DUT LAN" successfully

        When  get running config from "DUT"
        And   export "DUT" configuration file to tftp server
        Then  the comparison between running config and exported config must be the same

        When  reload factory-default "DUT"
        Then  "HOST" will ping "DUT LAN" failed
        When  import configuration file to "DUT" from tftp server
        And   get running config from "DUT"
        Then  the comparison between running config and exported config must be the same
        And   "HOST" will ping "DUT LAN" successfully