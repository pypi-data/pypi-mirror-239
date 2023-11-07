Feature: [Static Multicast]
Topology:
 +-----------------------------------------------------------------+
 |  HOST_B(receiver)------(port 1)DUT(port 8)------HOST_A(sender)  |
 +-----------------------------------------------------------------+
    Background:
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     clear "DUT" all logging event log
        *     prepare a "HOST_A" to connect to "DUT" 
        *     prepare a "HOST_B" to connect to "DUT" 
    Scenario Outline: Send multicast packets to the <MAC address>.
        When  set "DUT" a static multicast table with <MAC address> and "lan_port"
                | Vlan   |
                | <Vlan> |
        Then  the following rule should be on "DUT"'s static multicast table
                | MAC            | Type      | Port     |
                | <MAC address>  | mcast(s)  | lan_port |

        When  starts tshark sniffer on "HOST_B"
        And   send 10 layer 2 multicast packet from "HOST_A" to <MAC address>
        Then  "HOST_B" shall "success" to receive layer 2 multicast packets from "HOST_A"

        When  set "DUT" a static multicast table with <MAC address> and "wan_port"
                | Vlan   |
                | <Vlan> |
        Then  the following rule should be on "DUT"'s static multicast table
                | MAC            | Type      | Port     |
                | <MAC address>  | mcast(s)  | wan_port |

        When  starts tshark sniffer on "HOST_B"
        And   send 10 layer 2 multicast packet from "HOST_A" to <MAC address>
        Then  "HOST_B" shall "fail" to receive layer 2 multicast packets from "HOST_A"

        @sanity @multicast @edrg9010_v3 @edr8010_v3 @tn4900_v3
        Examples:
        | MAC address       | Vlan |
        | 01-00-5e-01-02-03 | 1    |
        | 01-10-11-03-02-01 | 1    |