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
		
	@event-notification @sanity @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3 @skip
	Scenario: Cold Start
		Given "DUT" will ping "HOST_A" successfully
		* set and enable syslog server with "HOST_A" ip on "DUT"
		* enable system-event with "cold-start" for syslog action on "DUT"
		* save configuration into flash on "DUT"
		* run syslog service on "HOST_A"
		When cold start on "DUT"
		Then "DUT" record event log "Cold Start"
		And "HOST_A" receive syslog "Cold Start"
