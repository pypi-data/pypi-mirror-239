Feature: [Broadcast Forwarding]

Topology:
 +-----------------------------------------+
 |  HOST_B------(LAN)DUT(WAN)------HOST_A  |
 +-----------------------------------------+
    @sanity @broadcast_forwarding @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: Configuration Import Export
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     prepare a "HOST_A" to connect to "DUT"
        *     prepare a "HOST_B" to connect to "DUT" 
        *     set WAN interface on "DUT"
        *     set LAN interface on "DUT"
        *     set "HOST_A" ip address within "DUT"s WAN subnet
        *     set "HOST_B" ip address within "DUT"s LAN subnet
        *     add static route for "HOST_A" routing to "HOST_B"
        *     add static route for "HOST_B" routing to "HOST_A"        
        When  enable broadcast forwarding on "DUT"
        And   add broadcast forwarding rule on "DUT"
              | In_interface | Out_interface | UDP_Port |
              | WAN          | LAN           | 1234     |
        And   starts tshark sniffer on "HOST_B"
        And   "HOST_A" send broadcast packet to its subnet
              | dest_port |
              | 1234      |
        Then  "HOST_B" shall receive broadcast packet from "HOST_A"
        When  get running config from "DUT"
        And   export "DUT" configuration file to tftp server
        Then  the comparison between running config and exported config must be the same

        When  reload factory-default "DUT"
        And   import configuration file to "DUT" from tftp server
        And   get running config from "DUT"
        Then  the comparison between running config and exported config must be the same

        When  starts tshark sniffer on "HOST_B"
        And   "HOST_A" send broadcast packet to its subnet
              | dest_port |
              | 1234      |
        Then  "HOST_B" shall receive broadcast packet from "HOST_A"
