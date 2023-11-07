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
		*     get running config from "DUT"
		*     export "DUT" configuration file to tftp server
    @bvt @sanity @config_br @self_testing @edrg9010_v3 @edr8010_v3 @tn4900_v3
	Scenario: Restore
		Given reload factory-default "DUT"
		And   clear "DUT" all logging event log
		When  import configuration file to "DUT" from tftp server
		And   get running config from "DUT"
		Then  the comparison between running config and exported config must be the same