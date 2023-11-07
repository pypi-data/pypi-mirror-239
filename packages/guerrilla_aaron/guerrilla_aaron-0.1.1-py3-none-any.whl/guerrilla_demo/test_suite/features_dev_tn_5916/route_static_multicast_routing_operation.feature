Feature: [Routing] 

Topology:
 +-----------------------------------------------------------+
 |  HOST_B(receiver)------(LAN)DUT(WAN)------HOST_A(sender)  |
 +-----------------------------------------------------------+
    @tn5916_v3 @sanity @route
    Scenario: Static Multicast Routing Operation
        # Background
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     set WAN interface on "DUT"
        *     set LAN interface on "DUT"
        *     prepare a "HOST_A" to connect to "DUT"
        *     prepare a "HOST_B" to connect to "DUT"
        *     set "HOST_A" ip address within "DUT"s WAN subnet
        *     set "HOST_B" ip address within "DUT"s LAN subnet
        *     add static route for "HOST_A" routing to "HOST_B"
        *     add static route for "HOST_B" routing to "HOST_A" 

        # Scenario of TCR-945
        ## make sure network works
        When  starts tshark sniffer on "HOST_B"
        And   "HOST_A" send 5 ICMP ping to "HOST_B"
        Then  "HOST_B" shall receive 5 ICMP request from "HOST_A"

        Given enable static multicast route on "DUT"
        *     set a static multicast route rule on "DUT"
              | src_ip | dst_ip    | in_iface | out_iface |
              | ANY    | 239.1.2.3 | WAN      | LAN       |

        When  starts tshark sniffer on "HOST_B"
        And   "HOST_A" send 100 multicast packet with destination ip "239.1.2.3"
        Then  "HOST_B" shall receive multicast packets from "HOST_A"

        When  starts tshark sniffer on "HOST_B"
        And   "HOST_A" send 100 multicast packet with destination ip "225.4.5.6"
        Then  "HOST_B" shall not receive multicast packets from "HOST_A"