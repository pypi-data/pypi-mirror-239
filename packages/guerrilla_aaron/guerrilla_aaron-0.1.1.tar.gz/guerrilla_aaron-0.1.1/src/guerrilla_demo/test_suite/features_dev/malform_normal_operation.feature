Feature: [Malform]


    @sanity @malform @self_testing @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: Malform Normal Operation
        # Background
        Given authorize CLI of "DUT"
        And   reload factory-default "DUT"
        *     set WAN interface on "DUT"
        *     set LAN interface on "DUT"
        *     prepare a "HOST_A" to connect to "DUT"
        *     prepare a "HOST_B" to connect to "DUT"
        *     set "HOST_A" ip address within "DUT"s WAN subnet
        *     set "HOST_B" ip address within "DUT"s LAN subnet
        *     add static route for "HOST_A" routing to "HOST_B"
        *     add static route for "HOST_B" routing to "HOST_A" 

        # # Scenario for TCR-947
        # ## make sure network works
        When  starts tshark sniffer on "HOST_B"
              | iface | filter | display |
              | eth1  | icmp   | icmp    |
        And   "HOST_A" send 5 ICMP ping to "HOST_B"
        Then  "HOST_B" shall receive 5 ICMP request from "HOST_A"

        Given clear "DUT" all logging event log
        When  malformed packets is "Disabled" on "DUT"
        And   malformed packets logging is "Disabled" on "DUT"
        And   starts tshark sniffer on "HOST_A"
              | iface | filter | display |
              | eth1  | icmp   | icmp    |
        And   "HOST_B" send 5 ICMP response to "HOST_A" through "DUT"
        Then  "HOST_A" shall receive 5 ICMP reponse from "HOST_B"
        And   malformed event log shall not be recorded on "DUT"

        Given clear "DUT" all logging event log
        When  malformed packets is "Enabled" on "DUT"
        And   malformed packets logging is "Enabled" on "DUT"
        And   starts tshark sniffer on "HOST_A"
              | iface | filter | display |
              | eth1  | icmp   | icmp    |
        And   "HOST_B" send 5 ICMP response to "HOST_A" through "DUT"
        Then  "HOST_A" shall receive 0 ICMP reponse from "HOST_B"
        And   5 malformed event log shall be recorded on "DUT"