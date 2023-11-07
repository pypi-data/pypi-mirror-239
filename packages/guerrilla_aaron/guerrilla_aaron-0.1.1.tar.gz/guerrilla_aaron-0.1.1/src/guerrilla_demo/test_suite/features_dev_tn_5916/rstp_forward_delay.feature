Feature: [RSTP]
Topology:
 +----------------+
 |  HOST------DUT |
 +----------------+
    Background:
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     clear "DUT" all logging event log
        *     prepare a "HOST" to connect to "DUT"
        *     set LAN interface on "DUT"
        *     set "HOST" ip address within "DUT"s LAN subnet
    @tn5916_v3 @sanity @rstp
    Scenario: Rstp Forward Delay
        When enable spanning tree on "DUT" with following table
             | brid  | hello_time | fwd_delay | max_age |
             | 32768 | 2          | 15        | 20      | 
        And  enable spanning tree on port 8 of "DUT" with following table
             | edge_port | pid | path_cost |
             | disable   | 128 | 20000     |
        Then "HOST" shall receive rstp packet with the content of the table
             | fwd_delay |
             | 15        |
        When enable spanning tree on "DUT" with following table
             | brid  | hello_time | fwd_delay | max_age |
             | 32768 | 2          | 30        | 20      | 
        Then "HOST" shall receive rstp packet with the content of the table
             | fwd_delay |
             | 30        |