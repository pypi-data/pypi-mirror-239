Feature: [Event Notification - Syslog]

    Background:
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     clear "DUT" all logging event log
        *     set WAN interface on "DUT"
        *     prepare a "HOST_A" to connect to "DUT"
        *     set "HOST_A" ip address within "DUT"s WAN subnet
    @tn5916_v3 @sanity @event-notification
    Scenario: Firewall add
        Given set and enable syslog server with HOST_A IP on "DUT"
        *     "DUT" will ping "HOST_A" successfully
        *     "DUT" enable system-event with "config-changed" for syslog action
        *     run syslog service on "HOST_A"
        
        When set a firewall rule on "DUT" to deny TCP and "IP and Port Filtering" from WAN ("HOST_A") to LAN ("HOST_B") and enable logging flash
        Then "DUT" record event log "Filter Configuration Change"
        And  "HOST_A" receive syslog "Filter Configuration Change"