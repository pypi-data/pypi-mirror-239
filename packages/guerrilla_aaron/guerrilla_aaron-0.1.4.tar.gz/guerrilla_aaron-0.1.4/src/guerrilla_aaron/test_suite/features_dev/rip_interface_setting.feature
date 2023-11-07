Feature: [RIP]
Topology
    Background:
        Given prepare "rip" topology
        *     authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     prepare a "HOST_A" to connect to "DUT"
        *     prepare a "HOST_B" to connect to "DUT" 
        *     set WAN interface on "DUT"
        *     set LAN interface on "DUT"
        *     set "HOST_A" ip address within "DUT"s WAN subnet
        *     set "HOST_B" ip address within "DUT"s LAN subnet
        *     add static route for "HOST_A" routing to "HOST_B"
        *     add static route for "HOST_B" routing to "HOST_A"  
	
     @sanity @rip @edrg9010_v3 @edr8010_v3 @tn4900_v3
     Scenario Outline: <iface> interface setting test
        When set rip with below table on "DUT"
             | network | version | redistribute |
             | <iface> | 2       |              |
        And  save configuration into flash on "DUT"
        And  send 1 rip response packet with the content of the table from "<sender>" to "DUT"
             | addr        | mask          | nexthop     | metric |
             | 10.0.0.0    | 255.255.255.0 | 10.0.0.1    | 2      | 
             | 192.168.0.0 | 255.255.255.0 | 192.168.0.1 | 2      | 
        Then routing table should be updated with response on "DUT"

        Examples:
            | iface | sender |
            | WAN   | HOST_A |
            | LAN   | HOST_B |