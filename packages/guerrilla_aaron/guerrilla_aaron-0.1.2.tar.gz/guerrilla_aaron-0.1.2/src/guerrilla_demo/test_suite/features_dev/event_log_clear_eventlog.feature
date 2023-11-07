Feature: [Event Log]
Topology:
 +----------------+
 |  HOST------DUT |
 +----------------+
	Background:
		Given authorize CLI of "DUT"
		*     clear "DUT" all logging event log
		*     reload factory-default "DUT"
		*     "DUT" records event log "Warm Start Factory Default"
	@sanity @event-log @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: Clear event log
		When  clear "DUT" all logging event log
		Then  "DUT"s event log is cleared