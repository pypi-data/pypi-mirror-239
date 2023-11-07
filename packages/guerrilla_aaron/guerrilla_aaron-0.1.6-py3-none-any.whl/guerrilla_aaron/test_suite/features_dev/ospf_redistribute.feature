Feature: OSPF Redistribute Connected
Topology
+-----------------------------------------+
|  HOST_B------(LAN)DUT(WAN)------HOST_A  |
+-----------------------------------------+
    Background:
        Given prepare "ospf" topology
        *     authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     prepare a "HOST_A" to connect to "DUT"
        *     set WAN interface on "DUT"
        *     set LAN interface on "DUT"
        *     set "HOST_A" ip address within "DUT"s WAN subnet
              | wan            |
              | 192.168.128.94 |
    @ospf @sanity @edrg9010_v3 @tn4900_v3
    Scenario Outline: OSPF Redistribute {redistribute}
        When  set ospf config on "DUT" WAN
              | area_id | priority | hello_interval | dead_interval | redistribute   |
              | 0.0.0.0 | 1        | 10             | 40            | <redistribute> |
        When  run ospf service on "HOST_A"
              | area_id | priority | hello_interval | dead_interval |
              | 0.0.0.0 | 1        | 10             | 40            |
        Then  ospf database <action> have ospf information from "DUT"s LAN

        @ospf @sanity @edrg9010_v3 @tn4900_v3
        Examples:
            | redistribute | action    |
            | connected    | should    |
            | disable      | shouldn't |