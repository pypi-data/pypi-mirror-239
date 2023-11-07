Feature: [Session Control]
Topology:
 +-----------------------------------------------------------+
 |  HOST_B(receiver)------(LAN)DUT(WAN)------HOST_A(sender)  |
 +-----------------------------------------------------------+
DUT LAN IP ADDR: 192.168.127.254
DUT WAN IP ADDR: 192.168.128.254
HOST_A(sender) IP ADDR: 192.168.128.94
HOST_B(receiver) IP ADDR: 192.168.127.93
    @sanity @session_ctrl @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: TCP Traffic Number Can Be Limited By total TCP Connection
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     clear "DUT" all logging event log
        *     prepare a "HOST_A" to connect to "DUT"
        *     prepare a "HOST_B" to connect to "DUT"
        *     set WAN interface on "DUT"
        *     set LAN interface on "DUT"
        *     set "HOST_A" ip address within "DUT"s WAN subnet
        *     set "HOST_B" ip address within "DUT"s LAN subnet
        *     add static route for "HOST_A" routing to "HOST_B"
        *     add static route for "HOST_B" routing to "HOST_A"

        Given create "total_tcp_connection" with destination "HOST_B" and limitation "1" on "DUT"
        Then  the session control rule is successfully created on "DUT"

        When  create "2" TCP connection from "HOST_A" to "HOST_B"
        Then  "1" TCP connection will be established from "HOST_A" to "HOST_B"