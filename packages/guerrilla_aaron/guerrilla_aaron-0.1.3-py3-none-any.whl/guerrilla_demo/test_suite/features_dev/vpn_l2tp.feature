Feature: [VPN] Establish L2TP server and test connection
Topology:
 +------------------------------------------------------------------------------------------+
 | +--------+                                                 +--------+                    |
 | |        | (L2TP client)10.0.0.2-----10.0.0.1(L2TP server) |        |                    |
 | | HOST_A | (eth1)192.168.128.94-------192.168.128.254(WAN) |  DUT   | (LAN)------HOST_B  |
 | +--------+                                                 +--------+                    |
 +------------------------------------------------------------------------------------------+

    @vpn @sanity @edrg9010_v3 @tn4900_v3
    Scenario:
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     prepare a "HOST_A" to connect to "DUT"
        *     prepare a "HOST_B" to connect to "DUT" 
        *     set WAN interface on "DUT"
        *     set LAN interface on "DUT"
        *     set "HOST_A" ip address within "DUT"s WAN subnet
        *     set "HOST_B" ip address within "DUT"s LAN subnet

        ## check WAN connection
        When  disable trusted access on "DUT"
        And   "DUT" enable WAN-Ping-Response
        Then  "HOST_A" will ping "DUT WAN" successfully

        ## set & check L2TP rule
        When  set l2tp server on "DUT"
              | Local IP | Offered IP: Start | Offered IP: End |
              | 10.0.0.1 | 10.0.0.2          | 10.0.0.2        |
        And   set l2tp user on "DUT"
              | Username | Password  |
              | user     | admin     |
        Then  the following rule should be on "DUT"s l2tp table
              | Server Mode | Local IP | Offered IP Range     | User Name |
              | Enable      | 10.0.0.1 | 10.0.0.2 - 10.0.0.2  | user      | 
        
        ## create VPN connection
        When  "HOST_A" tries to establish l2tp connection to "DUT"s l2tp server
        Then  verify "HOST_A" is assigned the IP "10.0.0.2" with interface "ppp0"
        And   "HOST_A" will ping "10.0.0.1" successfully


        ## set static route from HOST_A(l2tp_client) to HOST_B via VPN tunnel
        When  add static route for "HOST_A" with the following rule
              | Subnet        | Mask          | Gateway  |
              | 192.168.127.0 | 255.255.255.0 | 10.0.0.1 |
        And   add static route for "HOST_B" with the following rule
              | Subnet   | Mask          | Gateway         |
              | 10.0.0.0 | 255.255.255.0 | 192.168.127.254 |
        When  starts tshark sniffer on "HOST_B"
        And   send traffic with ICMP from "l2tp_client" to "HOST_B"
        Then  check if "HOST_B" can receive traffic with ICMP from "l2tp_client"

        ## clean up
        Given  disable and clean up l2tp connection on "HOST_A"