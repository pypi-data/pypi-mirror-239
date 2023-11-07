Feature: [Login Policy]
    Background: 
        Given authorize CLI of "DUT"
        * reload factory-default "DUT"
        * clear "DUT" all logging event log
    Scenario Outline: Login Failure Retry Threshold
        # Purpose:
        #   * Be able to login with correct password when failure tries are less than "threshold" times.
        #   * Be unable to login with correct password when failure tries are equal (or above) to "threshold" times.
        
        Given "DUT" enables login lockout toggle
        * "DUT" sets "Login Failure Retry Threshold" to "2" times
        * "DUT" sets "Lockout Duration" to "1" minute
        
        When "DUT" logins with incorrect password for "<lockout>" times
        And "DUT" logins with correct password for one more time after "1" seconds
        Then "DUT" is <capability> to login with correct password

        # Note: this step is irrelative to test case itself, but to unlock lockout period for following test cases (if any).
        When "DUT" logins with correct password for one more time after "<lockout_period>" seconds
        Then "DUT" is able to login with correct password
        @loginLockout @sanity @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
        Examples:
            | lockout   | capability  | lockout_period | 
            | 1         | able        | 0              | 
            | 2         | unable      | 60             | 