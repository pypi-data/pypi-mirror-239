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
    Scenario Outline: SNMP v3 setting and detection testing
        Given set snmp version to v1-v2c-v3 on "DUT"
        *     enable system-event with "config-changed" for "SNMP Trap Server only" action on "DUT"

        ##  setting trap/ inform mode
        *     set snmp trap/inform trap mode to <Mode> on "DUT"
                  | User  | Auth Type | Password  | Priv Key  |  
                  | admin | SHA       | adminpass | adminpriv | 
        *     set snmp trap/inform host to receive snmp notification on "DUT"
                  | Host IP         | Community  |
                  | 192.168.127.94  | public     | 

        Given starts snmptrapd tool on "HOST" to report SNMPv3 inform to get informRequest
        
        When  starts tshark sniffer on "HOST" for snmp packet
        And   create vlan with id "2" on "DUT"
        Then  "HOST" should receive 1 <Encrypt Packet Name> snmp packet with the following info from "DUT"
                  | info           | 
                  | privKey Unknow | 

        When  starts tshark sniffer and decrypt message on "HOST" for snmp packet without verbose
                  | UAT           | username | Auth Type | Password  | Encrypt Method | Encrypt Key |
                  | snmp_users:"" | admin    | SHA1      | adminpass | AES            | adminpriv   |
        And   create vlan with id "2" on "DUT"
        Then  "HOST" should receive 1 <Decrypt Packet Name> snmp packet with the following info from "DUT"
                  | info                       | 
                  | 1.3.6.1.4.1.8691.6.100.0.1 | 
        
        ## check engine id
        When  starts tshark sniffer and decrypt message on "HOST" for snmp packet with verbose
                  | UAT           | username | Auth Type | Password  | Encrypt Method | Encrypt Key |
                  | snmp_users:"" | admin    | SHA1      | adminpass | AES            | adminpriv   |
        And   create vlan with id "2" on "DUT"
        Then  "HOST" should receive snmp packet with engine id that is same as "DUT"s snmp table
        
    Examples:
        | Mode      | Encrypt Packet Name | Decrypt Packet Name |
        | trap-v3   | encryptedPDU        | snmpV2-trap         |
        | inform-v3 | encryptedPDU        | informRequest       |