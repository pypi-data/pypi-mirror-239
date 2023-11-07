Feature: [SNMP] setting & version detection testing
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
        When  set snmp version to v3 on "DUT"
        And   set snmp user authentication and privacy method on "DUT"
                | User  | Security level | Auth Type | Priv Method | Priv Key |
                | admin | authPriv       | SHA       | DES         | priv_key |
        And   set snmp engineid to "800021f3051234"
        And   set password for the following account on the "DUT"
                | User  | Password  |
                | admin | adminuser |

        Then  the following rule should be on "DUT"s snmp setting table
                | Version | Engine ID      | Admin Auth. Type | Auth status | Auth passwd |
                | v3      | 800021f3051234 | md5              | Enable      | *********   |

        When  get the sysname from "DUT"
        Then  "HOST" can get "DUT"s sysname by SNMP version 3
        And   "HOST" can not get "DUT"s sysname by SNMP version 2c

        Given "HOST" send snmp set request to set "DUT"s sysnem as "snmp_check_v3" by SNMP version 3
        Then  "DUT"s sysname can be set to "snmp_check_v3"

        Given "HOST" send snmp set request to set "DUT"s sysnem as "snmp_check_v2" by SNMP version 2c
        Then  "DUT"s sysname can not be set to "snmp_check_v2c"

        Given  set password and sysname to default on the "DUT"