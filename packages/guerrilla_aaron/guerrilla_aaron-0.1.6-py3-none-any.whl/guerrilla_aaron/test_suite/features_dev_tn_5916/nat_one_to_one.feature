Feature: [NAT] 
    Topology:
        +-------------------------------------+
        |  HOST_A--(WAN)--dut--(LAN)--HOST_B  |
        +-------------------------------------+
        dut WAN IP addr: 192.168.128.254/24
        dut LAN IP addr: 192.168.127.254/24
    Background:
        Given authorize CLI of "DUT"
        And   reload factory-default "DUT"
        And   set WAN interface on "DUT"
            | wan_vlan | wan             | mask          |
            | 2        | 192.168.128.254 | 255.255.255.0 |
        And   prepare a "HOST_A" to connect to "DUT"
        And   prepare a "HOST_B" to connect to "DUT"
        And   set "HOST_A" ip address within "DUT"s WAN subnet
            | wan            | mask          |
            | 192.168.128.94 | 255.255.255.0 |
        And   set "HOST_B" ip address within "DUT"s LAN subnet
            | lan            | mask          |
            | 192.168.127.10 | 255.255.255.0 |
        And   add static route for "HOST_A" routing to "HOST_B"
        And   add static route for "HOST_B" routing to "HOST_A"

    @tn5916_v3 @sanity @nat @ssh @self_testing
    Scenario: 1 to 1 NAT
        Given set 1-1 nat rule on "DUT"
            | nat_indexes | nat_iface | nat_dest_ip    | real_dest_ip   |
            | 1           | WAN       | 192.168.128.10 | 192.168.127.10 |
        And   starts tshark sniffer on "HOST_B"
        When  "HOST_A" send some icmp echo request packets for each destination IP
            | pkt_num | nat_dest_ip    |
            | 5       | 192.168.128.10 |
        Then  check "HOST_B" receive some icmp echo request packets with destination IP
            | pkt_num | real_dest_ip   |
            | 5       | 192.168.127.10 |
