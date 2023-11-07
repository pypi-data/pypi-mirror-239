Feature: [Event Log]
Topology:
 +----------------+
 |  HOST------DUT |
 +----------------+
	Background:
		Given authorize CLI of "DUT"
		*     clear "DUT" all logging event log
		*     reload factory-default "DUT"
        *     prepare a "HOST_EXECUTOR" to connect to "DUT"
		*     run tftp service on "HOST_EXECUTOR"
    @sanity @event-log @self_testing @edrg9010_v3 @edr8010_v3 @tn4900_v3
	Scenario: Export event log to tftp server
		When  export "DUT" system eventlog file to tftp server on "HOST_EXECUTOR"
		Then  the comparison between running system eventlog on "DUT" and exported system eventlog must be the same