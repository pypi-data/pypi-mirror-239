Feature: [Password Policy] 

    @sanity @paswd_policy @self_testing @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: Complexity Policy
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        When  enable password "complexity strength check" policy on "DUT"
        When  enable password "must contain at least one digit" policy on "DUT"
        Then  create user account on "DUT" will fail
                | username | password |
                | user1    | moxa     |
        Then  create user account on "DUT" will succeed
                | username | password |
                | user1    | moxa1    |

        When  enable password "must include both upper and lower case letter" policy on "DUT"
        Then  create user account on "DUT" will fail
                | username | password |
                | user1    | moxa1    |
                | user1    | MOXA1    |
        Then  create user account on "DUT" will succeed
                | username | password |
                | user1    | Moxa1    |

        When  enable password "must contain at least one special character" policy on "DUT"
        Then  create user account on "DUT" will fail
                | username | password |
                | user1    | Moxa1    |
        Then  create user account on "DUT" will succeed
                | username | password |
                | user1    | Moxa1^   |