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
              | wan_vlan | wan             | mask          |
              | 2        | 192.168.128.254 | 255.255.255.0 |
        *     set LAN interface on "DUT"
        *     set "HOST_A" ip address within "DUT"s WAN subnet
        *     set "HOST_B" ip address within "DUT"s LAN subnet
               | lan            | mask          |
               | 192.168.127.60 | 255.255.255.0 |
        *     add static route for "HOST_A" routing to "HOST_B"
        *     add static route for "HOST_B" routing to "HOST_A"
    @sanity @nat @self_testing @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: PAT rule
        Given set PAT nat rule on "DUT"
              | nat_indexes | nat_iface | nat_dest_port | real_dest_ip   | real_dest_port | protocol |
              | 1           | WAN       | 3889          | 192.168.127.60 | 3388           | UDP      |
        And   starts tshark sniffer on "HOST_B"
        When  "HOST_A" send UDP traffic to destination ip and port
              | nat_dest_ip     | nat_dest_port |
              | 192.168.128.254 | 3889          |
        Then  check "HOST_B" receive UDP traffic with destination IP and port
              | real_dest_ip   | real_dest_port |
              | 192.168.127.60 | 3388           |