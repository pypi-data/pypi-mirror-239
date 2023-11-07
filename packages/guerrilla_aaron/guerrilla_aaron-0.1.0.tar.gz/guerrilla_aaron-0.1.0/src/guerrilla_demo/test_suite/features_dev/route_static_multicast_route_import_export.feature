Feature: [Routing] 

Topology:
 +----------------------+
 |  DUT(WAN)------HOST  |
 +----------------------+
    @sanity @route @self_testing @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: Static Multicast Routing Configuration Export / Import
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     set WAN interface on "DUT"
        *     prepare a "HOST" to connect to "DUT"
        *     set "HOST" ip address within "DUT"s WAN subnet

        Given enable static multicast route on "DUT"
        *     set a static multicast route rule on "DUT"
              | src_ip | dst_ip    | in_iface | out_iface |
              | ANY    | 239.1.2.3 | WAN      | LAN       |

        When  get running config from "DUT"
        And   export "DUT" configuration file to tftp server
        Then  the comparison between running config and exported config must be the same

        Given reload factory-default "DUT"
        When  import configuration file to "DUT" from tftp server
        And   get running config from "DUT"
        Then  the comparison between running config and exported config must be the same