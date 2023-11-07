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
    And  enable trusted access on "DUT"
    And  enable telnet service on "DUT"
    Then "HOST_A" <action1> to access "DUT" with "protocol" from WAN
            | protocol |
            | HTTP     |
            | HTTPS    |
            | Telnet   |
            | SSH      |

    When delete rule "<Trusted IP>" with "<Netmask>" on "DUT"
    Then "HOST_A" <action2> to access "DUT" with "protocol" from WAN
            | protocol |
            | HTTP     |
            | HTTPS    |
            | Telnet   |
            | SSH      |
    @tn5916_v3 @sanity @trusted_access @ssh @self_testing
    Examples:
        | Trusted IP     | Netmask         | action1 | action2 |
        | 192.168.129.94 | 255.255.255.255 | fail    | fail    |
        | 192.168.128.94 | 255.255.255.255 | success | fail    |