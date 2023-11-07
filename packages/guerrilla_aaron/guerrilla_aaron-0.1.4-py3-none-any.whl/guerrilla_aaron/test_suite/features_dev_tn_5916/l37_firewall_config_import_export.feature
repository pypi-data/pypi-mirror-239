Feature: [L37 firewall]

Topology:
 +-----------------------------------------------------------+
 |  HOST_B(receiver)------(LAN)DUT(WAN)------HOST_A(sender)  |
 +-----------------------------------------------------------+
    @tn5916_v3 @sanity @l37 @bvt @ssh @self_testing
    Scenario: Configuration Import/Export of Firewall
        Given authorize CLI of "DUT"
       
        *     reload factory-default "DUT"
        *     clear "DUT" all logging event log
        *     set WAN interface on "DUT"
        *     set LAN interface on "DUT"
        *     prepare a "HOST_A" to connect to "DUT"
        *     prepare a "HOST_B" to connect to "DUT" 
        *     set "HOST_A" ip address within "DUT"s WAN subnet
        *     set "HOST_B" ip address within "DUT"s LAN subnet
        *     add static route for "HOST_A" routing to "HOST_B"
        *     add static route for "HOST_B" routing to "HOST_A"
        *     set a firewall rule on "DUT" to deny TCP and "IP and Port Filtering" from WAN ("HOST_A") to LAN ("HOST_B") and enable logging flash
        *     enable the firewall rule with index 1 on "DUT"
        
        When  send traffic with TCP from "HOST_A" to "HOST_B"
        Then  "HOST_B" cannot receive traffic with TCP from "HOST_A"
        And   "DUT" can record firewall logs block TCP traffic from WAN ("HOST_A") to LAN ("HOST_B")

        When  get running config from "DUT"
        And   export "DUT" configuration file to tftp server
        Then  the comparison between running config and exported config must be the same

        Given reload factory-default "DUT"
        And   clear "DUT" all logging event log
        When  import configuration file to "DUT" from tftp server
        And   get running config from "DUT"
        Then  the comparison between running config and exported config must be the same

        When  send traffic with TCP from "HOST_A" to "HOST_B"
        Then  "HOST_B" cannot receive traffic with TCP from "HOST_A"
        And   "DUT" can record firewall logs block TCP traffic from WAN ("HOST_A") to LAN ("HOST_B")