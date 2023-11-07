Feature: [Trusted Access]
Topology:
 +-------------------------------------------+
 |  HOST_B-------(LAN)DUT(WAN)-------HOST_A  |
 +-------------------------------------------+
  Background:
    Given authorize CLI of "DUT"
    *     reload factory-default "DUT"
    *     prepare a "HOST_B" to connect to "DUT"
    *     prepare a "HOST_A" to connect to "DUT"
    Given set WAN interface on "DUT"
    *     set "HOST_A" ip address within "DUT"s WAN subnet
  @sanity @trusted_access @self_testing @edrg9010_v2
  Scenario: Default Setting (FWR2.0)
    When check Trusted Access default setting on "DUT"
         | Trusted Access List | Syslog  | Trap    | Accept All LAN |
         | Enable              | Disable | Disable | Enable         |
    Then "action" to access "DUT" with "protocol" from "interface"
         | interface | protocol  | action  |
         | LAN       | HTTP      | success |
         | LAN       | HTTPS     | success |
         | LAN       | SSH       | success |
         | LAN       | Telnet    | success |
         | WAN       | HTTP      | fail    |
         | WAN       | HTTPS     | fail    |
         | WAN       | Telnet    | fail    |
         | WAN       | SSH       | fail    |
  @sanity @trusted_access @self_testing @edrg9010_v3 @edr8010_v3 @tn4900_v3
  Scenario: Default Setting
    When check Trusted Access default setting on "DUT"
         | Trusted Access List | Syslog  | Trap    | Accept All LAN |
         | Enable              | Disable | Disable | Enable         |
    Then "action" to access "DUT" with "protocol" from "interface"
         | interface | protocol  | action  |
         | LAN       | HTTP      | success |
         | LAN       | HTTPS     | success |
         | LAN       | SSH       | success |
         | LAN       | Telnet    | fail    |
         | WAN       | HTTP      | fail    |
         | WAN       | HTTPS     | fail    |
         | WAN       | Telnet    | fail    |
         | WAN       | SSH       | fail    |