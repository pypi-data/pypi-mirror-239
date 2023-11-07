Feature: [Diagnostics]
Topology:
 +----------------------------------------------------+
 |  HOST_EXEC------(LAN)DUT(WAN)------RD Network      |
 +----------------------------------------------------+
 
  Background: 
    Given authorize CLI of "DUT"
    *     reload factory-default "DUT"
    *     prepare a "HOST" to connect to "DUT"
    *     set LAN interface on "DUT"
    *     set WAN interface on "DUT" with dhcp mode
    *     set "HOST" ip address within "DUT"s LAN subnet
    *     save configuration into flash on "DUT"
  @sanity @diagnos @ping @edrg9010_v3 @edr8010_v3 @tn4900_v3
  Scenario: Ping Valid IP or Domain Name
    Then "DUT" will ping "google.com" successfully
    And  "DUT" will ping "HOST" successfully