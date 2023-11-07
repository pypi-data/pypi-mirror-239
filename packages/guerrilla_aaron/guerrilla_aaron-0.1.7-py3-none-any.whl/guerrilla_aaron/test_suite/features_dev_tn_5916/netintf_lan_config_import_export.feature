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
    @tn5916_v3 @sanity @netintf @bvt @ssh @self_testing
    Scenario: LAN Interface - Configuration Import/Export 
        When  modify LAN ip address on "DUT"
              | lan             | mask          |
              | 192.168.127.253 | 255.255.255.0 |
        And   set "HOST" ip address within "DUT"s LAN subnet
        Then  "HOST" will ping "DUT LAN" successfully

      #   Given login "DUT" with ip "192.168.127.253"
        When  get running config from "DUT"
        And   export "DUT" configuration file to tftp server
        Then  the comparison between running config and exported config must be the same
        
        When  reload factory-default "DUT"
        Then  "HOST" will ping "DUT LAN" failed
        When  import configuration file to "DUT" from tftp server
        And   get running config from "DUT"
        Then  the comparison between running config and exported config must be the same
        And   "HOST" will ping "DUT LAN" successfully
      #   Given modify LAN ip address on "DUT"
      #         | lan             | mask          |
      #         | 192.168.127.254 | 255.255.255.0 |
      #   *     set "HOST" ip address within "DUT"s LAN subnet
      #   *     login "DUT" with ip "192.168.127.254"
      #   *     save configuration into flash on "DUT"
       