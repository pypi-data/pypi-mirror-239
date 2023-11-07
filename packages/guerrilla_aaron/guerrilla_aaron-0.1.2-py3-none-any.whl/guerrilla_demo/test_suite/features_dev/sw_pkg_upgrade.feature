Feature: [SW Package]
Topology:
+-------------------------------+
|  HOST_A------(LAN)DUT  |
+-------------------------------+
    Background:
        Given prepare "default" topology
        *     authorize CLI of "DUT"
        # *     reload factory-default "DUT"
        *     clear "DUT" all logging event log
        *     prepare a "HOST_A" to connect to "DUT"
    Scenario Outline: Upgrade Software Package
        When  upgrade security package <security_version> on "DUT"
        And   upgrade mxsecurity package <mxsecurity_version> on "DUT"
        Then  displayed security package version should be consistent with "DUT"s <checked_security_version>
        And   displayed mxsecurity package version should be consistent with "DUT"s <checked_mx_security_version>
    @sw_pkg @sanity @edrg9010_v3 @edr8010_v3 @tn4900_v3 @skip
    Examples:
      | security_version | mxsecurity_version | comment | checked_security_version | checked_mx_security_version |
      | Security_EDR-G9010_V5.5.3_Build_22122919.pkg | MXSecurity_EDR-G9010_V1.0.18_Build_22121918.pkg | latest  | v5.5.0003 | v1.0.0018 |
      | Security_EDR-G9010_V5.5.4_Build_23020217.pkg | MXSecurity_EDR-G9010_V1.0.18_Build_22121918.pkg | current | v5.5.0004 | v1.0.0018 |