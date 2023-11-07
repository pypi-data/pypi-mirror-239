Feature: [SW Package]
Topology:
+-------------------------------+
|  HOST_A------(LAN)DUT  |
+-------------------------------+
    Background:
        Given prepare "default" topology
        *     authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     clear "DUT" all logging event log
        *     prepare a "HOST_A" to connect to "DUT"
    @sw_pkg @sanity @self_testing @edrg9010_v3 @edr8010_v3 @tn4900_v3 @skip
    Scenario: Package Status Checking
        Then  displayed pacakge version should be consistent with "DUT"s default version
            | security  | mxsecurity |
            | v6.0.0009 | v2.0.0008  |