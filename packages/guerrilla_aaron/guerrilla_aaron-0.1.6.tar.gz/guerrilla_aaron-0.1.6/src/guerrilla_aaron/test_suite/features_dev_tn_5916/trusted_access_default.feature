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
  @tn5916_v3 @sanity @trusted_access @ssh @self_testing
  Scenario: Default Setting
    When check Trusted Access default setting on "DUT"
         | Accessible IP List | Log Enable | Syslog  | Trap    | LAN     |
         | Disable            | Disable    | Disable | Disable | Disable |
    Then "action" to access "DUT" with "protocol" from "interface"
         | interface | protocol  | action  |
         | LAN       | HTTP      | success |
         | LAN       | HTTPS     | success |
         | LAN       | SSH       | success |
         | LAN       | Telnet    | success |
         | WAN       | HTTP      | success |
         | WAN       | HTTPS     | success |
         | WAN       | Telnet    | success |
         | WAN       | SSH       | success |