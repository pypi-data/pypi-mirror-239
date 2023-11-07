Feature: [Firewall - L37 Policy]
Topology:
 +-----------------------------------------------------------+
 |  HOST_B(receiver)------(LAN)DUT(WAN)------HOST_A(sender)  |
 +-----------------------------------------------------------+
DUT LAN IP ADDR: 192.168.127.254
DUT WAN IP ADDR: 192.168.128.254
HOST_A(sender) IP ADDR: 192.168.128.94
HOST_B(receiver) IP ADDR: 192.168.127.93
    Background: 
        Given prepare "l37" topology
        *     authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     clear "DUT" all logging event log
        *     prepare a "HOST_B" to connect to "DUT"
        *     prepare a "HOST_A" to connect to "DUT"
    Scenario Outline: Deny specific protocols: <specific protocols>
        Given set <incoming interface> interface on "DUT"
        *     set <outgoing interface> interface on "DUT"
        *     set "<sender>" ip address within "DUT"s <incoming interface> subnet
        *     set "<receiver>" ip address within "DUT"s <outgoing interface> subnet
        *     add static route for "HOST_A" routing to "HOST_B"
        *     add static route for "HOST_B" routing to "HOST_A"
        *     set a firewall rule on "DUT" to deny <specific protocols> and "IP and Port Filtering" from <incoming interface> ("<sender>") to <outgoing interface> ("<receiver>") and enable logging flash
        When  disable global firewall rule on "DUT"
        And   send traffic with ICMP from "<sender>" to "<receiver>"
        Then  check if "<receiver>" can receive traffic with ICMP from "<sender>"
        When  enable global firewall rule on "DUT"
        And   send traffic with <specific protocols> from "<sender>" to "<receiver>"
        Then  check if "<receiver>" cannot receive traffic with <specific protocols> from "<sender>"
        And   "DUT" can record firewall logs block <specific protocols> traffic from <incoming interface> ("<sender>") to <outgoing interface> ("<receiver>")

    @l37 @bvt @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Examples:
        | specific protocols | incoming interface | outgoing interface | sender | receiver |
        | UDP                | BRG                | BRG                | HOST_A | HOST_B   |
        
    @l37 @sanity @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Examples:
        | specific protocols | incoming interface | outgoing interface | sender | receiver |
        | ICMP               | WAN                | LAN                | HOST_A | HOST_B   |
        | TCP                | LAN                | WAN                | HOST_B | HOST_A   |
        | UDP                | BRG                | BRG                | HOST_A | HOST_B   |