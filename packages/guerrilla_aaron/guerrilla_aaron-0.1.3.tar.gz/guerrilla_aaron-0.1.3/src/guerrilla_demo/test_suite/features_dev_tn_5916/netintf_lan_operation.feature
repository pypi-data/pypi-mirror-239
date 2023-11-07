Feature: [Netintf]
Topology
 +---------------------+
 |  HOST------(LAN)DUT |
 +---------------------+
# !!! WARNING: please replace HOST with HOST_EXECUTOR when the con_type is ssh !!!
    Background:
        Given prepare "network_interface" topology
        *     authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     clear "DUT" all logging event log
        *     prepare a "HOST" to connect to "DUT"
    @tn5916_v3 @sanity @netintf @ssh @self_testing
    Scenario: Operation of LAN Interface
        When  set LAN interface on "DUT"
        And   set "HOST" ip address within "DUT"s LAN subnet
        Then  "HOST" will ping "DUT LAN" successfully
        When  modify LAN ip address on "DUT"
              | lan             | mask          |
              | 192.168.129.254 | 255.255.255.0 |
        And   set "HOST" ip address within "DUT"s LAN subnet
              | lan             | mask          |
              | 192.168.129.92  | 255.255.255.0 |
        Then  "HOST" will ping "DUT LAN" successfully
        # please enable follwing steps when the con_type is ssh
      #   Given login "DUT" with ip "192.168.129.254"
      #   *     modify LAN ip address on "DUT"
      #         | lan             | mask          |
      #         | 192.168.127.254 | 255.255.255.0 |
      #   *     set "HOST_EXECUTOR" ip address within "DUT"s LAN subnet
      #   *     login "DUT" with ip "192.168.127.254"