Feature: [Trusted Access]

Topology:
 +-------------------------+
 |   DUT(WAN)-----HOST_A   |
 +-------------------------+

  Background:
    Given authorize CLI of "DUT"
    *     reload factory-default "DUT"
    *     set WAN interface on "DUT"
    *     prepare a "HOST_A" to connect to "DUT"
    *     set "HOST_A" ip address within "DUT"s WAN subnet
            | wan            | mask          |
            | 192.168.128.94 | 255.255.255.0 |
  Scenario Outline: Trusted IP List
    When add and enable rule "<Trusted IP>" with "<Netmask>" on "DUT" trusted-access list
    And  add and enable rule for "HOST_EXECUTOR" on "DUT" trusted-access list
    And  enable telnet service on "DUT"
    Then "HOST_A" <action1> to access "DUT" with "protocol" from WAN
            | protocol |
            | HTTP     |
            | HTTPS    |
            | Telnet   |
            | SSH      |

    When disable rule "<Trusted IP>" with "<Netmask>" on "DUT"
    Then "HOST_A" <action2> to access "DUT" with "protocol" from WAN
            | protocol |
            | HTTP     |
            | HTTPS    |
            | Telnet   |
            | SSH      |
    @sanity @trusted_access @self_testing @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Examples:
        | Trusted IP     | Netmask         | action1 | action2 |
        | 192.168.129.94 | 255.255.255.255 | fail    | fail    |
        | 192.168.128.94 | 255.255.255.255 | success | fail    |