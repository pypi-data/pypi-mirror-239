Feature: [Authentication] RADIUS/local authentication redundency
Topology:
 +------------------------------------------+
 | (RADIUS1)HOST_A------DUT------HOST(USER) |
 | (RADIUS2)HOST_B------/                   |
 +------------------------------------------+

    Background:
        Given authorize CLI of "DUT"
	  *     reload factory-default "DUT"
	  *     prepare a "HOST" to connect to "DUT"
        *     prepare a "HOST_A" to connect to "DUT"
        *     prepare a "HOST_B" to connect to "DUT"
	  *     set "HOST_A" ip address within "DUT"s LAN subnet
              | lan            | mask          |
              | 192.168.127.94 | 255.255.255.0 |
        *     set "HOST_B" ip address within "DUT"s LAN subnet
              | lan            | mask          |
              | 192.168.127.93 | 255.255.255.0 |
        *     modify RADIUS config on "HOST_A"
              | username | password | service_type |
              | alice    | test     | Shell-User   |
              | bob      | test     | Shell-User   |
        *     modify RADIUS config on "HOST_B"
              | username | password | service_type |
              | bob      | test     | Shell-User   |

    @sanity @authentication @edrg9010_v3 @tn4900_v3
    Scenario:
        When  start RADIUS server on "HOST_A"
        When  start RADIUS server on "HOST_B"
        And   set RADIUS server on "DUT"
              | idx | ip             | port | share_key  | 
              | 1   | 192.168.127.94 | 1812 | testing123 |
              | 2   | 192.168.127.93 | 1812 | testing123 |
        And   set Login Authentication as RADIUS_Local on "DUT"
        Then  "HOST" "action" to login "DUT" as alice with password test via "console_type" 
              | console_type | action  |
              | HTTPS        | success |
        And   "HOST" "action" to login "DUT" as bob with password test via "console_type" 
              | console_type | action  |
              | HTTPS        | success |

        When  stop RADIUS server on "HOST_A"
        Then  "HOST" "action" to login "DUT" as alice with password test via "console_type"
              | console_type | action | wait_time |
              | HTTPS        | fail   | 6         |
        Then  "HOST" "action" to login "DUT" as bob with password test via "console_type" 
              | console_type | action  | wait_time |
              | HTTPS        | success | 6         |
        
        When  stop RADIUS server on "HOST_B"
        Then  "HOST" "action" to login "DUT" as bob with password test via "console_type"
              | console_type | action | wait_time |
              | HTTPS        | fail   | 11        |
        Then  "HOST" "action" to login "DUT" as admin with password moxa via "console_type" 
              | console_type | action  | wait_time |
              | HTTPS        | success | 9         |
        
        When  set Login Authentication as Local on "DUT"
        Then  "HOST" "action" to login "DUT" as bob with password test via "console_type"
              | console_type | action |
              | HTTPS        | fail   |
