Feature: [DDNS]
# Topology:
# +-----------------------------------------------+
# |  HOST_EXEC------(LAN)DUT(WAN)------RD Network |
# +-----------------------------------------------+
    Background:
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     prepare a "HOST_EXECUTOR" to connect to "DUT"

    @sanity @ddns @edrg9010_v3 @edr8010_v3 @tn4900_v3 @autotwo
    Scenario: NO-IP.com
        When  set WAN interface on "DUT" to access internet
              | wan             | mask          | wan_vlan | wan_gw      |
              | 10.123.39.199   | 255.255.255.0 | 2        | 10.123.39.1 |
        And   set dns server on "DUT"
              | dns_server_1    | dns_server_2  | dns_server_3  |
              | 8.8.8.8         | 10.123.200.11 | 10.123.200.12 |
        And   set ddns server with following table on "DUT"
              | service   | username               | password        | domain                |
              | no-ip     | jimmy950583@gmail.com  | Moxa89191230    | moxaautotest.ddns.net |
        Then  dig the domain name from "HOST_EXECUTOR" to check if the domain ip is replaced with "DUT"s WAN ip
              | domain                |
              | moxaautotest.ddns.net |
        When  set WAN interface on "DUT" to access internet
              | wan             | mask          | wan_vlan | wan_gw      |
              | 10.123.39.99    | 255.255.255.0 | 2        | 10.123.39.1 |
        Then  dig the domain name from "HOST_EXECUTOR" to check if the domain ip is replaced with "DUT"s WAN ip
              | domain                |
              | moxaautotest.ddns.net |

    @sanity @ddns @edrg9010_v3 @edr8010_v3 @tn4900_v3 @rdlab
    Scenario: NO-IP.com
        When  set WAN interface on "DUT"
              | wan             | mask          | wan_vlan | wan_port | wan_gw      |
              | 10.123.34.179   | 255.255.255.0 | 2        | 7        | 10.123.34.1 |
        And   set dns server on "DUT"
              | dns_server_1    | dns_server_2  | dns_server_3  |
              | 8.8.8.8         | 10.123.200.11 | 10.123.200.12 |
        And   set ddns server with following table on "DUT"
              | service   | username               | password        | domain                     |
              | no-ip     | jimmy950583@gmail.com  | Moxa89191230    | moxaautotestrdlab.ddns.net |
        Then  dig the domain name from "HOST_EXECUTOR" to check if the domain ip is replaced with "DUT"s WAN ip
              | domain                	   |
              | moxaautotestrdlab.ddns.net |
        When  set WAN interface on "DUT"
              | wan             | mask          | wan_vlan | wan_port | wan_gw      |
              | 10.123.34.99    | 255.255.255.0 | 2        | 7        | 10.123.34.1 |
        Then  dig the domain name from "HOST_EXECUTOR" to check if the domain ip is replaced with "DUT"s WAN ip
              | domain           	   |
              | moxaautotestrdlab.ddns.net |
