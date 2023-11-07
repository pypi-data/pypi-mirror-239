Feature: [Diagnostics]

Topology:
# Only LAN-to-LAN testing is possible due to a limitation in chip behavior, 
# where mirrored packets will be VLAN tagged by egress rules
+---------------------------------------------------------------------+
|  HOST_B------(LAN, mirror port)DUT(LAN, mirrored port)------HOST_A  |
+---------------------------------------------------------------------+

    @tn5916_v3 @sanity @diagnos
    Scenario: Port Mirror
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     prepare a "HOST_A" to connect to "DUT"
        *     prepare a "HOST_B" to connect to "DUT" 
        *     set LAN interface on "DUT"
        *     set "HOST_A" ip address within "DUT"s LAN subnet
        *     set "HOST_B" ip address within "DUT"s LAN subnet
        *     add static route for "HOST_A" routing to "HOST_B"
        *     add static route for "HOST_B" routing to "HOST_A" 

        When  set mirrored port and mirror port on "DUT"
              | mirrored | mirror |
              | HOST_A   | HOST_B |
        And   "HOST_B" start capture packet
        And   "HOST_A" arp "DUT"s LAN
        Then  "HOST_B" will receive arp packet sent from "HOST_A"