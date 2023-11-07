Feature: [Event Notification - Syslog]

    Background:
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     set system name to "DUT" on "DUT"
        *     clear "DUT" all logging event log
        *     prepare a "HOST_A" to connect to "DUT"
        *     prepare a "HOST_B" to connect to "DUT"
        *     set default network on "LAN" interface and rename it as "HOST_B" on "DUT"
        *     set network "wan_port" on "WAN" interface binding to VLAN "10" on "DUT"
        *     set "HOST_A" ip address within "DUT"s WAN subnet
        *     set "HOST_B" ip address within "DUT"s LAN subnet
        *     add static route for "HOST_A" routing to "HOST_B"
        *     add static route for "HOST_B" routing to "HOST_A"
        *     disable trusted access on "DUT"
        *     save configuration into flash on "DUT"
        
    @tn5916_v3 @sanity @event-notification @self_testing
    Scenario: Login Failure
        Given "DUT" will ping "HOST_A" successfully
        *     set and enable syslog server with "HOST_A" ip on "DUT"
        *     enable system-event with "auth-fail" for syslog action on "DUT"
        *     save configuration into flash on "DUT"
        *     run syslog service on "HOST_A"
        When use "username" with "incorrect password" to login for the "ordinal" time on "DUT"
          | ordinal | username    | incorrect password |
          | first   | admin       | xxx                |
          | second  | user        | xxx                |
          | third   | ghost       | xxx                |
        Then "DUT" record event log "Admin Auth Fail"
        And  "DUT" record event log "User Auth Fail"
        And  "DUT" record event log "User Auth Fail"
        And "HOST_A" receive syslog "Admin Auth Fail"
        And "HOST_A" receive syslog "User Auth Fail"
        And "HOST_A" receive syslog "User Auth Fail"