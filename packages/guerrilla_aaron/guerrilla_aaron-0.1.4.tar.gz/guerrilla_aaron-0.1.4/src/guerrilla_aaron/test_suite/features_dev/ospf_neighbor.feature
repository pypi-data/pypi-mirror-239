Feature: OSPF Neighbor
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
        *     set "HOST_A" ip address within "DUT"s WAN subnet
              | wan            |
              | 192.168.128.94 |
    Scenario Outline: OSPF Neighbor <action> contain HOST_A
        When  set ospf config on "DUT" WAN
              | area_id | priority | hello_interval   | dead_interval   | redistribute |
              | 0.0.0.0 | 1        | <hello_interval> | <dead_interval> | connected    |
        When  run ospf service on "HOST_A"
              | area_id | priority | hello_interval | dead_interval |
              | 0.0.0.0 | 1        | 10             | 40            |
        Then  ospf neighbor <action> contain "HOST_A" on "DUT"
        
        @ospf @sanity @edrg9010_v3 @tn4900_v3
        Examples:
            | hello_interval  | dead_interval | action    |
            | 10              | 40            | should    |
            | 20              | 40            | shouldn't |
            | 10              | 50            | shouldn't |