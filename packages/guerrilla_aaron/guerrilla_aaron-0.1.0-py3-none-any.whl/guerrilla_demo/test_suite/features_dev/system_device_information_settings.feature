Feature: [System Device]
Topology:
 +-------------------------+
 |  Eexcutor------(LAN)DUT |
 +-------------------------+
      Background:
            Given prepare "system" topology
            *     authorize CLI of "DUT"
      @sanity @system @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
      Scenario: information setting
            When  reload factory-default "DUT"
            Then  default system information of "DUT" is consistent with the spec
            When  modify system information on "DUT"
                  | sys_name     | sys_location  | sys_description |
                  | qq_name_5487 | qq_locat_5487 | qq_dec_5487     |
            Then  system information of "DUT" is consistent with the modified system information
                  | sys_name     | sys_location  | sys_description |
                  | qq_name_5487 | qq_locat_5487 | qq_dec_5487     |