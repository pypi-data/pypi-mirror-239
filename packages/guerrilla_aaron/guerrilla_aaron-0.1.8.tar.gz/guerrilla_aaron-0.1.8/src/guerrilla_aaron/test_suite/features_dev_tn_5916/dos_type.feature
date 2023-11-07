Feature: [DOS type]
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
    Scenario Outline: deny specific dos type <dos type> from direction <incoming interface> to <outgoing interface>
        Given set <incoming interface> interface on "DUT"
        *     set <outgoing interface> interface on "DUT"
        *     set "<sender>" ip address within "DUT"s <incoming interface> subnet
        *     set "<receiver>" ip address within "DUT"s <outgoing interface> subnet
        *     add static route for "HOST_A" routing to "HOST_B"
        *     add static route for "HOST_B" routing to "HOST_A"
        *     disable all dos rule on "DUT"
        *     set a dos rule to deny <dos type> and enable logging flash on "DUT"
        When  disable dos rule of <dos type> on "DUT" created by previous step
        And   send traffic with dos_type <dos type> from "<sender>" to "<receiver>"
        Then  check if "<receiver>" can receive traffic with dos_type <dos type>
        When  enable dos rule of <dos type> on "DUT" created by previous step
        And   send traffic with dos_type <dos type> from "<sender>" to "<receiver>"
        Then  check if "<receiver>" cannot receive traffic with dos_type <dos type>
        And   check traffic with dos_type <dos type> from <incoming interface> ("<sender>") to <outgoing interface> ("<receiver>") can be blocked and logged by "DUT"
    
    # @v2 @v3 @sanity @dos @self_testing 
    # Examples:
    #     | dos type                  | incoming interface  | outgoing interface | sender | receiver |
    #     | Null Scan                 | WAN                 | LAN                | HOST_A | HOST_B   |

    @tn5916_v2 @tn5916_v3 @sanity @dos
    Examples:
        | dos type                  | incoming interface  | outgoing interface | sender | receiver |
        | Null Scan                 | WAN                 | LAN                | HOST_A | HOST_B   |
        | Xmas Scan                 | LAN                 | WAN                | HOST_B | HOST_A   |
        | Nmap-ID Scan              | BRG                 | BRG                | HOST_A | HOST_B   |
        | SYN/FIN Scan              | WAN                 | LAN                | HOST_A | HOST_B   |
        | FIN Scan                  | LAN                 | WAN                | HOST_B | HOST_A   |
        | SYN/RST Scan              | BRG                 | BRG                | HOST_A | HOST_B   |
        | Nmap-Xmas Scan            | WAN                 | LAN                | HOST_A | HOST_B   | 
        | New-without-SYN Scan      | LAN                 | WAN                | HOST_B | HOST_A   | 