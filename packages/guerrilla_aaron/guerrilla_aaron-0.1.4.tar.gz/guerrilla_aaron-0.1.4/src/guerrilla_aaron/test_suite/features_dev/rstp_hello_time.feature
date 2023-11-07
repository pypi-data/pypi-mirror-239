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
    @sanity @rstp @edrg9010_v3 @tn4900_v3
    Scenario: Rstp Hello Time
        When enable spanning tree on "DUT" with following table
             | brid  | hello_time | fwd_delay | max_age |
             | 32768 | 2          | 15        | 20      | 
        And  enable spanning tree on port 8 of "DUT" with following table
             | edge_port | pid | path_cost |
             | disable   | 128 | 20000     |
        Then "HOST" shall receive 5 hello packet in 11 sec
        When enable spanning tree on "DUT" with following table
             | brid  | hello_time | fwd_delay | max_age |
             | 32768 | 1          | 15        | 20      | 
        Then "HOST" shall receive 10 hello packet in 11 sec

    @sanity @rstp @edr8010_v3
    Scenario: Rstp Hello Time
        When enable spanning tree on "DUT" with following table
             | brid  | hello_time | fwd_delay | max_age |
             | 32768 | 2          | 15        | 20      | 
        And  enable spanning tree on port 8 of "DUT" with following table
             | edge_port | pid | path_cost |
             | disable   | 128 | 200000    |
        Then "HOST" shall receive 5 hello packet in 11 sec
        When enable spanning tree on "DUT" with following table
             | brid  | hello_time | fwd_delay | max_age |
             | 32768 | 1          | 15        | 20      | 
        Then "HOST" shall receive 10 hello packet in 11 sec