Feature: [Config BR]

    @sanity @config_br @self_testing @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: Encrypt Sensitive Information
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     clear "DUT" all logging event log
        *     prepare a "HOST_EXECUTOR" to connect to "DUT"
        *     run tftp service on "HOST_EXECUTOR"
        
        When  create NTP Authentication Keys on "DUT"
                | key_id | key_type | key  |
                | 1      | SHA512   | moxa |
        And   enable PPTP Dialup on "DUT"
                | ip             | username | password |
                | 192.168.128.10 | admin    | moxa     |
        And   configure Dynamic DNS on "DUT"
                | username | password |
                | admin    | moxa     |
        And   add OSPF area on "DUT"
                | router_id | area_id |
                | 0.0.0.0   | 1.1.1.1 |
        And   create interface for ospf on "DUT"
                | interface | area_id | auth_type | auth_key |
                | LAN       | 1.1.1.1 | simple    | moxa     |
        And   set WAN interface on "DUT"
        And   set IPSec tunnel on "DUT"
                | vpn_name | remote-gateway | startup-mode | local-multi-network | remote-multi-network | identity | ike-mode | ike-version | auth-mode psk | encryption | life-time | pfs  | dpd-action | dpd-delay | dpd-timeout |
                | testVPN  | 0.0.0.0        | wait         | 192.168.129.254/24  | 192.168.130.254/24   | address  | main     | ikev2       | xyz123!@#$%^GO| aes256     | 43200     | 2048 | hold       | 30        | 120         |
        And   create account for L2TP on "DUT"
                | username | password |
                | admin    | moxa     |
        And   set IEEE 802.1X radius 1st-server on "DUT"
                | share_key |
                | moxa      |
        And   set IEEE 802.1X Local Database on "DUT"
                | username | password |
                | admin    | moxa     |
        And   set RADIUS server on "DUT"
                | idx | ip            | port | share_key | 
                | 1   | 192.168.127.2 | 1    | moxa1     |
        And   set email account on "DUT"
                | username | password |
                | admin    | moxa2    |
        
        And   enable file encryption with signature information as "Encrypt sensitive information only" and key string as "test" on "DUT"
        And   export "DUT" configuration file to tftp server
        Then  the following sensitive information in running config on "DUT" is encrypted
                | information           | original_value |
                | ntp authentication    | moxa           |
                | ip pptp               | moxa           |
                | ip ddns password      | moxa           |
                | ip ospf auth          | moxa           |
                | l2tp user             | moxa           |
                | dot1x local-userdb    | moxa           |
                | auth radius server    | moxa1          |
                | email-warning account | moxa2          |

        When  create vlan with id "3" on "DUT"
        And   save configuration into flash on "DUT"
        And   clear "DUT" all logging event log
        And   enable file encryption with signature information as "Encrypt all information" and key string as "test" on "DUT"
        
        Then  import configuration file to "DUT" from tftp server failed
        And   vlan id "3" is on "DUT"
        And   "DUT" record event log "Config. Import Fail"

        Given clear "DUT" all logging event log
        When  enable file encryption with signature information as "Encrypt sensitive information only" and key string as "test" on "DUT"
        Then  import configuration file to "DUT" from tftp server successfully
        And   vlan id "3" is not on "DUT"
        And   "DUT" record event log "Config. Import Success"