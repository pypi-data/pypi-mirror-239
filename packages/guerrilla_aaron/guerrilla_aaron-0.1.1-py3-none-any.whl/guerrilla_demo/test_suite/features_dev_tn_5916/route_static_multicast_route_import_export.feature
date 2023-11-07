Feature: [Routing]

Topology:
 +----------------------+
 |  DUT(WAN)------HOST  |
 +----------------------+
    @tn5916_v3 @sanity @route
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