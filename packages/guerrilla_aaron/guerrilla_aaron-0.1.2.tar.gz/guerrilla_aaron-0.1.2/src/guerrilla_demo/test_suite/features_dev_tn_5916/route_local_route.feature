Feature: [Routing]

Topology:
 +-----------------------------------------+
 |  HOST_B------(LAN)DUT(WAN)------HOST_A  |
 +-----------------------------------------+
    @tn5916_v3 @sanity @route @bvt @ssh @self_testing
    Scenario: Local Routing
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     prepare a "HOST_A" to connect to "DUT"
        *     prepare a "HOST_B" to connect to "DUT" 
        *     set WAN interface on "DUT"
        *     set LAN interface on "DUT"
        When  set "HOST_A" ip address within "DUT"s WAN subnet
        And   set "HOST_B" ip address within "DUT"s LAN subnet
        And   add static route for "HOST_A" routing to "HOST_B"
        And   add static route for "HOST_B" routing to "HOST_A"        
        Then  "HOST_A" will ping "HOST_B" successfully
        And   "HOST_B" will ping "HOST_A" successfully