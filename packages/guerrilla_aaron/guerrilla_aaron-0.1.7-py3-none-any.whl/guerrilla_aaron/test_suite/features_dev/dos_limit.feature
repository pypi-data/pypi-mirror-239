    
Feature: [Firewall - DoS Policy]
Topology1:
 +-----------------------------------------------------------+
 |  HOST_B(receiver)------(LAN)DUT(WAN)------HOST_A(sender)  |
 +-----------------------------------------------------------+
DUT LAN IP ADDR: 192.168.127.254
DUT WAN IP ADDR: 192.168.128.254
HOST_A(sender) IP ADDR: 192.168.128.94
HOST_B(receiver) IP ADDR: 192.168.127.93

Topology2:
 +-----------------------------------------------------------+
 |  HOST_B(receiver)------(WAN)DUT(LAN)------HOST_A(sender)  |
 +-----------------------------------------------------------+
DUT LAN IP ADDR: 192.168.127.254
DUT WAN IP ADDR: 192.168.128.254
HOST_A(sender) IP ADDR: 192.168.127.94
HOST_B(receiver) IP ADDR: 192.168.128.93

Topology3:
 +-----------------------------------------------------------+
 |  HOST_B(receiver)------(BRG)DUT(BRG)------HOST_A(sender)  |
 +-----------------------------------------------------------+
DUT BRG IP ADDR: 192.168.126.254
HOST_A(sender) IP ADDR: 192.168.126.94
HOST_B(receiver) IP ADDR: 192.168.126.93

    Background:
        Given prepare "dos" topology
        *     authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     clear "DUT" all logging event log
        *     prepare a "HOST_B" to connect to "DUT"
        *     prepare a "HOST_A" to connect to "DUT"
        *     set WAN interface on "DUT"
        *     set LAN interface on "DUT"
        *     set "HOST_A" ip address within "DUT"s WAN subnet
        *     set "HOST_B" ip address within "DUT"s LAN subnet
        *     add static route for "HOST_A" routing to "HOST_B"
        *     add static route for "HOST_B" routing to "HOST_A"
        *     disable all dos rule on "DUT"
    
    Scenario Outline: Prevent DoS attacks with SYN/RST Scan from WAN to LAN
        When "DUT" SYN-RST Dos Defense turns <defense>
        And  "DUT" Dos Defense flash log turns on
        And  "HOST_B" starts tshark to sniffer
        And  "HOST_A" sends 1000 TCP packets in flag of SYN and RST to "HOST_B"'s port 80
        And  "HOST_B" waits <wait> seconds then stops tshark snifferring
        Then "HOST_B" received <received> packets from "HOST_A"
        And  "DUT" logging <detect> attack events from "HOST_A" to "HOST_B" in the period of testing
    
    @sanity @dos @self_testing @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Examples:
    | defense | wait | received | detect |
    |    off  |  10  |  1000    |   no   |
    |    on   |  10  |     0    |  some  |
