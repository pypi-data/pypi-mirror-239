Feature: [Login Policy]
    Background:
        Given authorize CLI of "DUT"
        * reload factory-default "DUT"
        * clear "DUT" all logging event log

    @loginLockout @sanity @self_testing @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: Verify login lockout duration
        Given "DUT" enables login lockout toggle
        * "DUT" sets "Login Failure Retry Threshold" to "2" times
        * "DUT" sets "Lockout Duration" to "1" minute
        * "DUT" logins with incorrect password for "2" times

        When "DUT" logins with correct password for one more time after "1" seconds
        Then "DUT" is unable to login with correct password

        When "DUT" logins with correct password for one more time after "40" seconds
        Then "DUT" is unable to login with correct password

        When "DUT" logins with correct password for one more time after "60" seconds
        Then "DUT" is able to login with correct password
        And "DUT" can see system log "Auth Ok, Lockout" for "2" times
