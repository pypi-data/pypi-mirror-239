Feature: [Authentication] RADIUS authentication operation (HTTP/HTTPS/SSH/Telnet)
Topology:
 +---------------------------------------+
 | (RADIUS)HOST------DUT------HOST(USER) |
 +---------------------------------------+

    Background:
        Given authorize CLI of "DUT"
	  *     reload factory-default "DUT"
	  *     prepare a "HOST" to connect to "DUT"
	  *     set "HOST" ip address within "DUT"s LAN subnet
              | lan            | mask          |
              | 192.168.127.94 | 255.255.255.0 |
        *     modify RADIUS config on "HOST"
              | username | password | service_type |
              | bob      | test     | Shell-User   |

    @sanity @authentication @edrg9010_v3 @tn4900_v3
    Scenario Outline:
        When  start RADIUS server on "HOST"
        And   set authentication type as <auth_type> for the RADIUS server on "DUT"
        And   set RADIUS server on "DUT"
              | idx | ip             | port | share_key  | 
              | 1   | 192.168.127.94 | 1812 | testing123 |
        And   set Login Authentication as RADIUS on "DUT"
        And   enable telnet service on "DUT"
        Then  "HOST" "action" to login "DUT" as bob with password test via "console_type" 
              | console_type | action  |
              | SSH          | success |
              | HTTPS        | success |
        And   "HOST" "action" to login "DUT" as admin with password moxa via "console_type"
              | console_type | action |
              | SSH          | fail   |
              | Telnet       | fail   |
              | HTTP         | fail   |
              | HTTPS        | fail   |

        When  stop RADIUS server on "HOST"
        Then  "HOST" "action" to login "DUT" as admin with password moxa via "console_type"
              | console_type | action |
              | SSH          | fail   |
              | Telnet       | fail   |
              | HTTP         | fail   |
              | HTTPS        | fail   |
        
        When  set Login Authentication as Local on "DUT"
        Then  "HOST" "action" to login "DUT" as bob with password test via "console_type" 
              | console_type | action |
              | SSH          | fail   |
              | HTTPS        | fail   |

    Examples:
	| auth_type     |
      | pap           |
	| chap          |
      | peap-mschapv2 |