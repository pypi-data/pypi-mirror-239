Feature: [Config BR]
Topology:
 +----------------+
 |  HOST------DUT |
 +----------------+
	Background:
		Given authorize CLI of "DUT"
		*     reload factory-default "DUT"
		*     clear "DUT" all logging event log
        *     prepare a "HOST_EXECUTOR" to connect to "DUT"
		*     run tftp service on "HOST_EXECUTOR"
    @bvt @sanity @config_br @edrg9010_v3 @edr8010_v3 @tn4900_v3
	Scenario: Backup
		When  get running config from "DUT"
		And   export "DUT" configuration file to tftp server
		Then  the comparison between running config and exported config must be the same