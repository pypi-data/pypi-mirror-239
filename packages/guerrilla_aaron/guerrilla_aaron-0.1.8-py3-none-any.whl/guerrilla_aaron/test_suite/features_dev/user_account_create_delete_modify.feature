Feature: [User Account]

Topology:
 +-------------------------+
 |  Eexcutor------(LAN)DUT |
 +-------------------------+
    @sanity @user_account @self_testing @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: Create/ Delete/ Modify account
        Given login "DUT" as Admin
        *     reload factory-default "DUT"
        *     enable telnet service on "DUT"
        *     clear ssh and telnet limit on "DUT"
        
        #  create account
        When  create user account on "DUT"
                | username | password | privilege |
                | user1    | moxa     | user      |
        And   logout "DUT"
        Then  login "DUT" as user1 with password moxa successfully

        # modify password
        Given logout "DUT"
        *     login "DUT" as Admin
        When  modify user account on "DUT"
                | username | password  |
                | user1    | adminmoxa |
        And   logout "DUT"
        Then  unable to login "DUT" as user1 with password moxa
        And   login "DUT" as user1 with password adminmoxa successfully

        # modify privilege
        Given logout "DUT"
        *     login "DUT" as Admin
        When  modify user account on "DUT"
                | username | password  | privilege |
                | user1    | moxa      | no login  |
        And   logout "DUT"
        Then  unable to login "DUT" as user1 with password moxa

        # delete account
        Given login "DUT" as Admin
        When  delete user account on "DUT"
                | username |
                | user1    |
        Then  no user1 on "DUT" User Accounts
        When  logout "DUT"
        Then  unable to login "DUT" as user1 with password moxa
