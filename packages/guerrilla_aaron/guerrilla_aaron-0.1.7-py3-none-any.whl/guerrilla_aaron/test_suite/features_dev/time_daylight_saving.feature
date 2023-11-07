Feature: [Time]

    Topology:
    +-----------------------------+
    |  HOST_EXEC------(LAN)DUT    |
    +-----------------------------+
    
    @sanity @self_testing @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario Outline: Daylight Saving: Local
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     set summer time to start at "<start_time>" on "DUT"
        *     set summer time to end at "<end_time>" on "DUT"
        *     set summer time offset as "<offset>" hour on "DUT"

        When set the current time on "DUT" 1 minute behind "<real_start_time>"
        And  wait 1 minute until the current time on "DUT" reaches "<start_time>"
        Then the current time on "DUT" should be <offset> hour ahead of "<real_start_time>"

        When wait 2 minute until the current time on "DUT" reaches "<end_time>"
        Then the current time on "DUT" should be <offset> hour behind "<real_end_time>"

        Examples:
            | start_time      | end_time        | offset | real_start_time            | real_end_time              |
            | Mar 2nd Sun 2 0 | Mar 2nd Sun 3 2 | 1      | Sun March 12 02:00:00 2023 | Sun March 12 03:02:00 2023 |