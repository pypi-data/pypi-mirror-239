Feature: [SNMP] v1-v2c operation
Topology:
 +----------------+
 |  HOST------DUT |
 +----------------+

    Background:
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     prepare a "HOST" to connect to "DUT"
        *     set "HOST" ip address within "DUT"s LAN subnet

    @sanity @edrg9010_v3 @tn4900_v3 @edr8010_v3 @snmp
    Scenario: 
        When  set snmp version to v1-v2c on "DUT"
        When  get the sysname from "DUT"

        Then  "HOST" can get "DUT"s sysname by SNMP version 1
        Then  "HOST" can get "DUT"s sysname by SNMP version 2c

        Given "HOST" send snmp set request to set "DUT"s sysnem as "snmp_check_v1" by SNMP version 1
        Then  "DUT"s sysname can be set to "snmp_check_v1"

        Given "HOST" send snmp set request to set "DUT"s sysnem as "snmp_check_v2c" by SNMP version 2c
        Then  "DUT"s sysname can be set to "snmp_check_v2c"