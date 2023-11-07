Feature: [Routing Table]

    @sanity @routing_table @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: static route
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     set WAN interface on "DUT"
                | wan             | mask          |
                | 192.168.128.254 | 255.255.255.0 |
        When  set "DUT" a static route rule with parameters and status Enable
                | destination_ip | mask            | next_hop        | metric |
                | 192.168.125.9 | 255.255.255.255 | 192.168.128.125  | 1      |
        Then  the following rule should be on "DUT"'s routing table
                | Type      | Destination       | Next Hop        | interface |
                | static    | 192.168.125.9/32  | 192.168.128.125  | WAN      |