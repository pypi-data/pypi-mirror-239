Feature: [NTP]
    Purpose: 
        * Check if local clock source works on DUT.
    Topology: N/A

    Background:
        Given authorize CLI of "DUT"
        * reload factory-default "DUT"
        * clear "DUT" all logging event log

    @sanity @ntp @self_testing @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: Verify NTP clock source is Local
        When set clock source to "Local" on "DUT"
        And set current time to "DUT"
        Then "DUT" displays current time with accuracy in minute

        When set "2" days prior to current time on "DUT"
        Then "DUT" displays correct date with "2" days prior to current date
