Feature: [L37 firewall]
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
    Scenario Outline: deny traffic with specified filter mode <specified filter mode>
        Given set <incoming interface> interface on "DUT"
        *     set <outgoing interface> interface on "DUT"
        *     set "<sender>" ip address within "DUT"s <incoming interface> subnet
        *     set "<receiver>" ip address within "DUT"s <outgoing interface> subnet
        *     add static route for "HOST_A" routing to "HOST_B"
        *     add static route for "HOST_B" routing to "HOST_A"
        *     set a firewall rule on "DUT" to deny TCP and "<specified filter mode>" from <incoming interface> ("<sender>") to <outgoing interface> ("<receiver>") and enable logging flash
        When  disable the firewall rule with index 1 on "DUT"
        And   send traffic with ICMP from "<sender>" to "<receiver>"
        Then  check if "<receiver>" can receive traffic with ICMP from "<sender>"
        When  enable the firewall rule with index 1 on "DUT"
        And   send traffic with TCP from "<sender>" to "<receiver>"
        Then  check if "<receiver>" cannot receive traffic with TCP from "<sender>"
        And   "DUT" can record firewall logs block TCP traffic from <incoming interface> ("<sender>") to <outgoing interface> ("<receiver>")

    @tn5916_v3 @l37 @ssh @self_testing
    Examples:
        | incoming interface | outgoing interface | specified filter mode | sender | receiver |
        | LAN                | WAN                | IP and Port Filtering | HOST_B | HOST_A   |

    @tn5916_v3 @sanity @l37 @ssh
    Examples:
        | incoming interface | outgoing interface | specified filter mode | sender | receiver |
        | WAN                | LAN                | IP and Port Filtering | HOST_A | HOST_B   |
        | LAN                | WAN                | Source MAC            | HOST_B | HOST_A   |
        | BRG                | BRG                | Source MAC            | HOST_A | HOST_B   |