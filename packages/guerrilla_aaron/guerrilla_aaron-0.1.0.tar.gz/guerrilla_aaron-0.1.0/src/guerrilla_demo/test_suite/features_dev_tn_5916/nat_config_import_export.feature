Feature: [NAT]
Topology:
 +------------------------------------------------------+
 |  private subnet                        public subnet |
 |  HOST_B(tftp server)---(LAN)DUT(WAN)-------HOST_A    |
 +------------------------------------------------------+
    Background:
        Given prepare "nat" topology
        *     authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     clear "DUT" all logging event log
        *     prepare a "HOST_B" to connect to "DUT"
        *     prepare a "HOST_A" to connect to "DUT"
        *     prepare a "HOST_EXECUTOR" to connect to "DUT"
        *     run tftp service on "HOST_EXECUTOR"
        Given set WAN interface on "DUT"
        *     set LAN interface on "DUT"
        *     set "HOST_A" ip address within "DUT"s WAN subnet
        *     set "HOST_B" ip address within "DUT"s LAN subnet
        *     add static route for "HOST_A" routing to "HOST_B"
        *     add static route for "HOST_B" routing to "HOST_A"
    @tn5916_v3 @sanity @nat @bvt @self_testing
    Scenario: NAT Config Import Export
        Given set N-1 nat rule on "DUT"
              | nat_indexes | source_ip_start    | source_ip_end    | outgoing_interface  |
              | 1           | 192.168.127.1      | 192.168.127.253  | WAN                 |
        When  send traffic with TCP from "HOST_B" to "HOST_A"
        Then  check if "HOST_A" can receive traffic with "DUT"s WAN ip and TCP
        When  get running config from "DUT"
        And   export "DUT" configuration file to tftp server
        Then  the comparison between running config and exported config must be the same
        When  reload factory-default "DUT"
        And   import configuration file to "DUT" from tftp server
        And   get running config from "DUT"
        Then  the comparison between running config and exported config must be the same
        When  send traffic with TCP from "HOST_B" to "HOST_A"
        Then  check if "HOST_A" can receive traffic with "DUT"s WAN ip and TCP