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
        *     prepare a "HOST_EXECUTOR" to connect to "DUT"
    Scenario Outline: Traffic can be blocked by <specified rule> with maximum number of rules
        Given set virtual interfaces on "DUT" ports
              | virtual interfaces | ports   | virtual ip |
              | WAN                | 3       | 0.0.0.254  |
              | BRG                | 4       | 1.1.1.254  |
        Given import <config> to "DUT" from tftp server
        Given set <incoming interface> interface on "DUT"
        *     set <outgoing interface> interface on "DUT"
        *     set "<sender>" ip address within "DUT"s <incoming interface> subnet
        *     set "<receiver>" ip address within "DUT"s <outgoing interface> subnet
        *     add static route for "HOST_A" routing to "HOST_B"
        *     add static route for "HOST_B" routing to "HOST_A"
        # *     cycle a maximum number of rules with a set of firewall rules and only sepcified index rule mapping the traffic on "DUT"
        #     | specified index   | specific protocols | incoming interface | outgoing interface | sender | receiver |
        #     | 0                 | ICMP               | WAN                | LAN                | HOST_A | HOST_B   |
        #     | 512               | TCP                | LAN                | WAN                | HOST_B | HOST_A   |
        #     | 1023              | UDP                | BRG                | BRG                | HOST_A | HOST_B   |

        When  disable global firewall rule on "DUT"
        And   send traffic with ICMP from "<sender>" to "<receiver>"
        Then  check if "<receiver>" can receive traffic with ICMP from "<sender>"
        When  enable global firewall rule on "DUT"
        And   send traffic with <specific protocols> from "<sender>" to "<receiver>"
        Then  check if "<receiver>" cannot receive traffic with <specific protocols> from "<sender>"
        And   "DUT" can record firewall logs block <specific protocols> traffic from <incoming interface> ("<sender>") to <outgoing interface> ("<receiver>")

    @sanity @l37 @edrg9010 @edrg9010_v2 @edrg9010_v3
    Examples:
        | incoming interface | outgoing interface  | specific protocols | sender | receiver | config                    |
        | WAN                | LAN                 | ICMP               | HOST_A | HOST_B   | edrg9010_max_firewall.ini |        
        | LAN                | WAN                 | TCP                | HOST_B | HOST_A   | edrg9010_max_firewall.ini |
        | BRG                | BRG                 | UDP                | HOST_A | HOST_B   | edrg9010_max_firewall.ini |
    
    @sanity @l37 @tn4916 @tn4900_v3
    Examples:
        | incoming interface | outgoing interface  | specific protocols | sender | receiver | config                  |
        | WAN                | LAN                 | ICMP               | HOST_A | HOST_B   | tn4916_max_firewall.ini |        
        | LAN                | WAN                 | TCP                | HOST_B | HOST_A   | tn4916_max_firewall.ini |
        | BRG                | BRG                 | UDP                | HOST_A | HOST_B   | tn4916_max_firewall.ini |

    @sanity @l37 @edr8010_v3
    Examples:
        | incoming interface | outgoing interface  | specific protocols | sender | receiver | config                    |
        | WAN                | LAN                 | ICMP               | HOST_A | HOST_B   | edr8010_max_firewall.ini  |
        | LAN                | WAN                 | TCP                | HOST_B | HOST_A   | edr8010_max_firewall.ini  |
        | BRG                | BRG                 | UDP                | HOST_A | HOST_B   | edr8010_max_firewall.ini  |