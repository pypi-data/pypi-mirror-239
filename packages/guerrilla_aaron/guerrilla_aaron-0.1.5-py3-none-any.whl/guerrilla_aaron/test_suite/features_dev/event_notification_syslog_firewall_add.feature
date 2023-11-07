Feature: [Event Notification - Syslog]

Purpose:
  * After Adding DUT Firewall Policy, DUT can record event log: "Firewall Policy Added"
  * Syslog server from WAN side can reveive the event log  

Topology:
 +-------------------------+
 |   DUT(WAN)-----HOST_A   |
 +-------------------------+
HOST_A Service: syslog service

    Background:
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     clear "DUT" all logging event log
        *     set WAN interface on "DUT"
        *     prepare a "HOST_A" to connect to "DUT"
        *     set "HOST_A" ip address within "DUT"s WAN subnet
        
    @sanity @event-notification @edrg9010_v2
    Scenario: Firewall Policy Added (FWR2.0)
        Given set and enable syslog server with HOST_A IP on "DUT"
        *     "DUT" will ping "HOST_A" successfully
        *     "DUT" enable system-event with "firewall-policy-changed" for syslog action
        *     run syslog service on "HOST_A"
        
        When  set a firewall rule on "DUT" to deny TCP and "IP and Port Filtering" from WAN ("HOST_A") to LAN ("HOST_B") and enable logging flash
        Then  "DUT" record event log "Firewall Policy Added"
        And   "HOST_A" receive syslog "Firewall Policy Added"

    @sanity @event-notification @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: Firewall Policy Added
        Given set and enable syslog server with HOST_A IP on "DUT"
        *     save configuration into flash on "DUT"
        *     "DUT" will ping "HOST_A" successfully
        *     "DUT" enable system-event with "firewall-policy-changed" for syslog action
        *     run syslog service on "HOST_A"
        
        When  set a firewall rule on "DUT" to deny TCP and "IP and Port Filtering" from WAN ("HOST_A") to LAN ("HOST_B") and enable logging flash
        Then  "DUT" record event log "Firewall Policy via UI: Serial Console. Added deny_TCP_ip"
        And   "HOST_A" receive syslog "Firewall Policy via UI: Serial Console. Added deny_TCP_ip"


        