Feature: [Password Policy] 

    @sanity @paswd_policy @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: Minimum Length Policy
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        When  set password mininum length as 6 on "DUT"
        Then  create user account on "DUT" will fail
                | username | password | privilege |
                | user1    | mooxa    | user      |
        Then  create user account on "DUT" will succeed
                | username | password | privilege |
                | user2    | moooxa   | user      |
                | user3    | mooooxa  | user      |

        Given logout "DUT"
        Then  login "DUT" as user2 with password moooxa successfully
        Given logout "DUT"
        Then  login "DUT" as user3 with password mooooxa successfully