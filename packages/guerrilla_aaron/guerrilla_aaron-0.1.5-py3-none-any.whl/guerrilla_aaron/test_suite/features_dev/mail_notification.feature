Feature:
Topology:
 +----------------+
 |  HOST------DUT |
 +----------------+
	Background:
		Given authorize CLI of "DUT"
		*     reload factory-default "DUT"
		# Because the services required to set up the mail server take a longer time, the auto logout is turned off to avoid logging out
		*     disable auto-logout on "DUT"
		*     clear "DUT" all logging event log
        *     set LAN interface on "DUT"
        *     prepare a "HOST_A" to connect to "DUT"
		*     set "HOST_A" ip address within "DUT"s LAN subnet
        *     "HOST_A" will ping "DUT LAN" successfully
    @sanity @mail_notify @edrg9010_v3 @edr8010_v3 @tn4900_v3
	Scenario:
		When  set email settings on "DUT" with following configuration
			  | server | mail_address          | account               | paswd     | sender        | port |
			  | HOST_A | mutt@mail.example.com | test@mail.example.com | adminmoxa | moxa@moxa.com | 587  |
		And   run email server on "HOST_A" with following configuration
			  | user  | paswd     |
			  | test  | adminmoxa |
			  | mutt  | adminmoxa |
		And   run mutt client on "HOST_A" with following configuration
			  | hostname   | user  | paswd     | imap_port |
			  | mail.local | mutt  | adminmoxa | 143       |
		And   send test email from "DUT" to mutt client
		Then  test email can be received by mutt client on "HOST_A"