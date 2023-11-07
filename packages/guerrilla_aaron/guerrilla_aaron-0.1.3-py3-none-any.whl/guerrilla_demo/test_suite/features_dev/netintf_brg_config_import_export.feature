Feature: [Netintf]
Topology:
 +---------------------+
 |  DUT(BRG)------HOST |
 +---------------------+
    Background:
        Given prepare "network_interface" topology
        *     authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     clear "DUT" all logging event log
        *     prepare a "HOST" to connect to "DUT"
        *     set BRG interface on "DUT"
              | brg             | brg_port |
              | 192.168.126.254 | 8        |
        *     set "HOST" ip address within "DUT"s BRG subnet
        *     disable trusted access on "DUT"
        Then  "HOST" will ping "DUT BRG" successfully
    @sanity @netintf @bvt @self_testing @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: BRG Interface - Configuration Import/Export 
        When  get running config from "DUT"
        And   export "DUT" configuration file to tftp server
        Then  the comparison between running config and exported config must be the same

        When  reload factory-default "DUT"
        Then  "HOST" will ping "DUT BRG" failed
        When  import configuration file to "DUT" from tftp server
        And   get running config from "DUT"
        Then  the comparison between running config and exported config must be the same
        And   "HOST" will ping "DUT BRG" successfully