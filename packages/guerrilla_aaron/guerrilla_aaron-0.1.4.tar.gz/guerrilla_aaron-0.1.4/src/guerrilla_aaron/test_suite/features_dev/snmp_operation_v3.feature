Feature: [SNMP] v3 operation
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
    Scenario Outline: 
        When  set snmp version to v3 on "DUT"
        And   set snmp user authentication and privacy method on "DUT"
                  | User  | Security level   | Auth Type             | Priv Method         | Priv Key         |
                  | admin | <Security level> | <Authentication Type> | <Encryption Method> | <Encryption Key> |
        And   set password for the following account on the "DUT"
                  | User  | Password             |
                  | admin | <Autehntication Key> |

        When  get the sysname from "DUT"
        Then  "HOST" can get "DUT"s sysname by SNMP version 3

        Given "HOST" send snmp set request to set "DUT"s sysnem as "snmp_check" by SNMP version 3
        Then  "DUT"s sysname can be set to "snmp_check"

        Given  set password and sysname to default on the "DUT"

  Examples:
        | Security level | Authentication Type | Autehntication Key | Encryption Method | Encryption Key | 
        | NoAuthNoPriv   | no-auth             | None               | None              | None           |
        | authNoPriv     | MD5                 | adminuser          | None              | None           |
        | authPriv       | MD5                 | adminuser          | DES               | priv_key       |
        | authPriv       | SHA                 | adminuser          | AES               | priv_key       |