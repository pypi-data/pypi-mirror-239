Feature: [Routing Table]

    @sanity @routing_table @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: local route
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        When  set WAN interface on "DUT"
                | wan             | mask          |
                | 192.168.129.254 | 255.255.255.0 |
        Then  the following rule should be on "DUT"'s routing table
                | Type      | Destination      | Next Hop        | interface |
                | connected | 192.168.129.0/24 | 192.168.129.254 | WAN       |
        When  set LAN interface on "DUT"
                | lan             | mask          |
                | 192.168.128.254 | 255.255.255.0 |
        Then  the following rule should be on "DUT"'s routing table
                | Type      | Destination      | Next Hop        | interface |
                | connected | 192.168.128.0/24 | 192.168.128.254 | LAN       |
        When  set BRG interface on "DUT"
                | brg             | brg_port |
                | 192.168.126.254 | 8        |
        Then  the following rule should be on "DUT"'s routing table
                | Type      | Destination      | Next Hop        | interface |
                | connected | 192.168.126.0/24 | 192.168.126.254 | BRG_LAN   |