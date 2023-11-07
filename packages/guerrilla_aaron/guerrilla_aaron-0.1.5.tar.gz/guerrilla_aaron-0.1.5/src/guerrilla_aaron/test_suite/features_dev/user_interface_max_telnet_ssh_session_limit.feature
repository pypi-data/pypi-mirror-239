Feature: [User Interface]

Topology:
 +-----------------------+
 |  HOST------(LAN)DUT   |
 +-----------------------+
Default SSH + Telnet Thershold 
EDRG9010: 5
    @sanity @user_interface @self_testing @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: Maximum Telnet/ SSH Session Limit
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     clear "DUT" all logging event log
        *     prepare a "HOST" to connect to "DUT" 
        *     set LAN interface on "DUT"
        *     set "HOST" ip address within "DUT"s LAN subnet
        *     enable telnet service on "DUT"
        Then  "HOST" tries to establish 3 ssh and 3 telnet connection to "DUT"s LAN but only default 5 session can be established