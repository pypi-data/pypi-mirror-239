Feature: [Config BR]

    @sanity @config_br @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: Encrypt All Information
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     clear "DUT" all logging event log
        *     prepare a "HOST_EXECUTOR" to connect to "DUT"
        *     run tftp service on "HOST_EXECUTOR"
        
        When  enable file encryption with signature information as "Encrypt all information" and key string as "test" on "DUT"
        And   export "DUT" configuration file to tftp server
        And   create vlan with id "3" on "DUT"
        And   save configuration into flash on "DUT"
        And   clear "DUT" all logging event log
        And   enable file encryption with signature information as "Encrypt sensitive information only" and key string as "test1" on "DUT"
        
        Then  import configuration file to "DUT" from tftp server failed
        And   vlan id "3" is on "DUT"
        And   "DUT" record event log "Config. Import Fail"

        When  clear "DUT" all logging event log
        And   enable file encryption with signature information as "Encrypt all information" and key string as "test" on "DUT"
        Then  import configuration file to "DUT" from tftp server successfully
        And   vlan id "3" is not on "DUT"
        And   "DUT" record event log "Config. Import Success"