Feature: [Event Notification - Syslog]

	Background:	
		Given authorize CLI of "DUT"
		* reload factory-default "DUT"
		* set system name to "DUT" on "DUT"
		* clear "DUT" all logging event log
		* prepare a "HOST_A" to connect to "DUT"
        * prepare a "HOST_B" to connect to "DUT"
        * set default network on "LAN" interface and rename it as "HOST_B" on "DUT"
		* set network "wan_port" on "WAN" interface binding to VLAN "10" on "DUT"
        * set "HOST_A" ip address within "DUT"s WAN subnet
        * set "HOST_B" ip address within "DUT"s LAN subnet
        * add static route for "HOST_A" routing to "HOST_B"
        * add static route for "HOST_B" routing to "HOST_A"
		* enable WAN-Ping-Response on "DUT"
		* disable trusted access on "DUT"
		* save configuration into flash on "DUT"
		
	@event-notification @sanity @edrg9010_v2
	Scenario:  Configuration Changed (FWR2.0)
		Given "DUT" will ping "HOST_A" successfully
		* set and enable syslog server with "HOST_A" ip on "DUT"
		* enable system-event with "config-changed" for syslog action on "DUT"
		* save configuration into flash on "DUT"
		* run syslog service on "HOST_A"
		When set system name to "DUT-changed" on "DUT"
		Then "DUT" record event log "Configuration Change System Info"
		And "HOST_A" receive syslog "Configuration Change System Info"

    @event-notification @sanity @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario:  Configuration Changed
        Given "DUT" will ping "HOST_A" successfully
        * set and enable syslog server with "HOST_A" ip on "DUT"
        * enable system-event with "config-changed" for syslog action on "DUT"
        * save configuration into flash on "DUT"
        * run syslog service on "HOST_A"
        When set system name to "DUT-changed" on "DUT"
        Then "DUT" record event log "Configuration Change via UI: Serial Console. System Info"
        And "HOST_A" receive syslog "Configuration Change via UI: Serial Console. System Info"
