Feature: [NTP]
    Purpose: 
        * Check if local clock source works on DUT.
    Topology: N/A

    Background:
        Given authorize CLI of "DUT"
        * reload factory-default "DUT"
        * clear "DUT" all logging event log

    @tn5916_v2 @tn5916_v3 @sanity @ntp @self_testing
    Scenario: Verify NTP clock source is Local
        When set clock source to "Local" on "DUT"
        And set current time to "DUT"
        Then "DUT" displays current time with accuracy in minute

        When set "2" days prior to current time on "DUT"
        Then "DUT" displays correct date with "2" days prior to current date
