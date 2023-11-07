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
    @tn5916_v3 @sanity @netintf @ssh @self_testing
    Scenario: Operation of BRG Interface
        When  set BRG interface on "DUT"
        And   set "HOST" ip address within "DUT"s BRG subnet
        And   disable trusted access on "DUT"
        Then  "HOST" will ping "DUT BRG" successfully

        When  modify BRG ip address on "DUT"
              | brg             | mask          |
              | 192.168.129.254 | 255.255.255.0 |
        And   set "HOST" ip address within "DUT"s BRG subnet
              | brg             | mask          |
              | 192.168.129.94  | 255.255.255.0 |
        Then  "HOST" will ping "DUT BRG" successfully

        When  disable BRG interface from "DUT"
        Then  "HOST" will ping "DUT BRG" failed