Feature: [User Interface]

Topology:
 +-----------------------------------------+
 |  HOST_B------(LAN)DUT(WAN)------HOST_A  |
 +-----------------------------------------+
    @sanity @user_interface @self_testing @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: Default Enabled User Interface
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     prepare a "HOST_A" to connect to "DUT"
        *     prepare a "HOST_B" to connect to "DUT" 
        *     set WAN interface on "DUT"
        *     set LAN interface on "DUT"
        *     set "HOST_A" ip address within "DUT"s WAN subnet
        *     set "HOST_B" ip address within "DUT"s LAN subnet
        *     enable telnet service on "DUT"
        *     save configuration into flash on "DUT"
        Then  "HOST_B" success to access "DUT" with "protocol" from LAN
              | protocol |
              | HTTP     |
              | HTTPS    |
              | Telnet   |
              | SSH      |
        And   "HOST_A" will ping "DUT WAN" unsuccessfully
        When  enable WAN-Ping-Response on "DUT"
        And   disable trusted access on "DUT"
        And   save configuration into flash on "DUT"
        Then  "HOST_A" will ping "DUT WAN" successfully
        And   "HOST_B" tries to establish 3 ssh and 3 telnet connection to "DUT"s LAN but only default 5 session can be established