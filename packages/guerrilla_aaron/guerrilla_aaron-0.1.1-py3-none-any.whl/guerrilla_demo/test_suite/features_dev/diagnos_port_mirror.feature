Feature: [Diagnostics]

Topology:
+---------------------------------------------------------------------+
|  HOST_B------(LAN, mirror port)DUT(WAN, mirrored port)------HOST_A  |
+---------------------------------------------------------------------+

    @sanity @diagnos @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: Port Mirror
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

        When  set mirrored port and mirror port on "DUT"
              | mirrored | mirror |
              | HOST_A   | HOST_B |
        And   "HOST_B" start capture packet
        And   "HOST_A" arp "DUT"s WAN
        Then  "HOST_B" will receive arp packet sent from "HOST_A"