Feature: [VRRP]
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
              | lan              | mask            |
              | 192.168.127.254  | 255.255.255.0   |
        *     set "HOST" ip address within "DUT"s LAN subnet
              | lan             | mask            |
              | 192.168.127.94  | 255.255.255.0   |
    @tn5916_v3 @sanity @vrrp   
    Scenario: Election
        When  set up vrrp on the "DUT" with the content of the table
              | status | version | vrid | vip             | priority | preempt_mode | preempt_delay | accept_mode | interface | adver_interval |
              | enable | 3       | 1    | 192.168.127.253 | 100      | enable       | 120           | enable      | LAN       | 1000           |
        And   wait for 3 advertisement interval
        Then  vrrp status should be "MASTER" on "DUT"
        When  send 1 vrrp packet with the content of the table from "HOST" to "DUT"
              | version | type | vrid | addr_list       | priority |
              | 3       | 1    | 1    | 192.168.127.253 | 101      |
        Then  vrrp status should be "BACKUP" on "DUT"