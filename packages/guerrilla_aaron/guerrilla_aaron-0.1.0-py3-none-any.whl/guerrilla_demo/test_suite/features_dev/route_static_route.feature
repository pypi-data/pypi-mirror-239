# Copyright (C) MOXA Inc. All rights reserved.
#
#This software is distributed under the terms of the MOXA SOFTWARE NOTICE.
#
#See the file MOXA-SOFTWARE-NOTICE for details.
#
#
# Reference: https://moxanbginsngfw.atlassian.net/browse/TCR-664

Feature: [Routing]
Topology1:
 +-------------------------------------------------------------+
 |  HOST_B(receiver)------(LAN)DUT(WAN)------HOST_A(sender)  |
 +-------------------------------------------------------------+
    Background:
        Given prepare "route" topology
        *     authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     clear "DUT" all logging event log
        *     prepare a "HOST_B" to connect to "DUT"
        *     prepare a "HOST_A" to connect to "DUT"
        *     set WAN interface on "DUT"
        *     set LAN interface on "DUT"
        *     set "HOST_A" ip address within "DUT"s WAN subnet
        *     set "HOST_B" ip address within "DUT"s LAN subnet
        *     add a static route with unknown destination ip for "HOST_A"
              | st_route_dip   | st_route_next_hop |
              | 192.168.129.30 | 192.168.128.254   |

    Scenario Outline: Static route rule enable/disable test
        Given set "DUT" a static route rule with parameters and status <status>
              | destination_ip | mask            | next_hop       | metric |
              | 192.168.129.30 | 255.255.255.255 | 192.168.127.93 | 1      |
        When  send test packet with the destination ip form "HOST_A" to "HOST_B"
              | dip            |
              | 192.168.129.30 |
        Then  check if "HOST_B" <action> receive test packet from "HOST_A"
    @sanity @route @bvt @self_testing @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Examples:
          | status  | action  |
          | Enable  | can     |
          | Disable | can not |
