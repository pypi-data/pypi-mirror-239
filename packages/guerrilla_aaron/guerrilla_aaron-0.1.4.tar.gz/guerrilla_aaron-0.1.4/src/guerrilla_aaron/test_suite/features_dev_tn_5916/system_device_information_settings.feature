Feature:
Topology:
 +-------------------------+
 |  Eexcutor------(LAN)DUT |
 +-------------------------+
      Background:
            Given prepare "system" topology
            *     authorize CLI of "DUT"
      @v3 @sanity @system @tn-5916
      Scenario:
            When  reload factory-default "DUT"
            Then  default system information of "DUT" is consistent with the spec
            When  modify system information on "DUT"
                  | sys_name     | sys_location  | sys_description |
                  | qq_name_5487 | qq_locat_5487 | qq_dec_5487     |
            Then  system information of "DUT" is consistent with the modified system information
                  | sys_name     | sys_location  | sys_description |
                  | qq_name_5487 | qq_locat_5487 | qq_dec_5487     |