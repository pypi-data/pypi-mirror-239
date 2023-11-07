Feature: OSPF ABR
Topology
+---------------------------------------------+
|  HOST_B------(LAN)DUT-ABR(WAN)------HOST_A  |
+---------------------------------------------+
    Background:
        Given prepare "ospf" topology
        *     authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     prepare a "HOST_A" to connect to "DUT"
        *     prepare a "HOST_B" to connect to "DUT"
        *     set WAN interface on "DUT"
        *     set LAN interface on "DUT"
        *     set "HOST_A" ip address within "DUT"s WAN subnet
              | wan            |
              | 192.168.128.94 |
        *     set "HOST_B" ip address within "DUT"s LAN subnet
              | lan            |
              | 192.168.127.93 |
    @ospf @sanity @edrg9010_v3 @tn4900_v3
    Scenario: OSPF ABR
        When  set ospf config on "DUT" WAN
              | area_id | priority | hello_interval | dead_interval | redistribute |
              | 0.0.0.0 | 1        | 10             | 40            | connected    |
        And   set ospf config on "DUT" LAN
              | area_id | priority | hello_interval | dead_interval | redistribute |
              | 1.1.1.1 | 1        | 10             | 40            | connected    |
        And   run ospf service on "HOST_A"
              | area_id | priority | hello_interval | dead_interval |
              | 0.0.0.0 | 1        | 10             | 40            |
        And   run ospf service on "HOST_B"
              | area_id | priority | hello_interval | dead_interval |
              | 1.1.1.1 | 1        | 10             | 40            |
        Then "HOST_A" should receive Type 3 Summary LSAs