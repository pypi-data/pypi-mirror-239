Feature: [Netintf]
Topology
 +---------------------+
 |  DUT(WAN)------HOST |
 +---------------------+
    Background:
        Given prepare "network_interface" topology
        *     authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     clear "DUT" all logging event log
        *     prepare a "HOST" to connect to "DUT"
    @tn5916_v3 @sanity @netintf @ssh @self_testing
    Scenario: Operation of WAN Interface
        When  set WAN interface on "DUT"
        And   set "HOST" ip address within "DUT"s WAN subnet
        And   disable trusted access on "DUT"
        # please enable the step when it is supported
        # And   "DUT" enable WAN-Ping-Response
        And   save configuration into flash on "DUT"
        Then  "HOST" will ping "DUT WAN" successfully

        When  modify WAN ip address on "DUT"
              | wan             | mask          |
              | 192.168.129.254 | 255.255.255.0 |
        And   set "HOST" ip address within "DUT"s WAN subnet
              | wan             | mask          |
              | 192.168.129.94  | 255.255.255.0 |
        Then  "HOST" will ping "DUT WAN" successfully

        # please enable following two steps when it is supported
        # When  disable WAN interface from "DUT"
        # Then  "HOST" will ping "DUT WAN" failed