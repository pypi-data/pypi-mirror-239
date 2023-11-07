Feature: [SNMP Trap/Infomr] 
Topology:
 +----------------+
 |  HOST------DUT |
 +----------------+

    Background:
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     prepare a "HOST" to connect to "DUT"
        *     set "HOST" ip address within "DUT"s LAN subnet
    
    @sanity @edrg9010_v3 @tn4900_v3 @edr8010_v3 @snmp_trap_inform 
    Scenario Outline: SNMP v1, v2c setting and detection testing
        Given set snmp version to v1-v2c-v3 on "DUT"
        *     enable system-event with "config-changed" for "SNMP Trap Server only" action on "DUT"
        *     set snmp trap/inform trap mode to <Mode> on "DUT"
                  | Inform Retry | Inform Timeout | 
                  | 5            | 1              |
        *     set snmp trap/inform host to receive snmp notification on "DUT"
                  | Host IP         | Community  |
                  | 192.168.127.94  | public     | 
              
        When  starts tshark sniffer on "HOST" for snmp packet
        And   create vlan with id "2" on "DUT"

        Then  "HOST" should receive <Received Packet Number> <Received Packet Name> snmp packet with the following info from "DUT"
                  | info                       | 
                  | 1.3.6.1.4.1.8691.6.100.0.1 |


    Examples:
        | Mode       | Received Packet Name | Received Packet Number |
        | trap-v1    | trap                 | 1                      |
        | trap-v2c   | snmpV2-trap          | 1                      |
        | inform-v2c | informRequest        | 5                      |