Feature: [NAT]
    Topology:
     +------------------------------------------------------+
     |  private subnet                        public subnet |
     |  HOST_B(tftp server)---(LAN)DUT(WAN)-------HOST_A    |
     +------------------------------------------------------+
    Background:
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     prepare a "HOST_B" to connect to "DUT"
        *     prepare a "HOST_A" to connect to "DUT"
        *     set WAN interface on "DUT"
        *     set LAN interface on "DUT"
        *     set "HOST_A" ip address within "DUT"s WAN subnet
        *     set "HOST_B" ip address within "DUT"s LAN subnet
               | lan            | mask          |
               | 192.168.127.60 | 255.255.255.0 |
        *     add static route for "HOST_A" routing to "HOST_B"
        *     add static route for "HOST_B" routing to "HOST_A"
    @sanity @nat @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: N - 1 NAT
        Given set N-1 nat rule on "DUT"
              | nat_indexes | source_ip_start    | source_ip_end    | outgoing_interface  |
              | 1           | 192.168.127.50     | 192.168.127.100  | WAN                 |
        When  send traffic with icmp from "HOST_B" to "HOST_A"
        Then  check if "HOST_A" can receive traffic with "DUT"s WAN ip and icmp