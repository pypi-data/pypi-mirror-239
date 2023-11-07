Feature: [Certificate]
Topology:
 +--------------------+
 |  HOST----(LAN)DUT  |
 +--------------------+

    Background:
		Given authorize CLI of "DUT"
		*     reload factory-default "DUT"
		*     prepare a "HOST" to connect to "DUT"
		*     set "HOST" ip address within "DUT"s LAN subnet

    @sanity @certificate @edrg9010_v3 @edr8010_v3 @tn4900_v3
	Scenario: Certificate from CSR
		Given "HOST" login to "DUT" web console from LAN port to get jwt
		*     "HOST" connect "DUT" to generate RSA Key
		*     "HOST" connect "DUT" to generate CSR
		      | country_name | locality_name | org_name | org_unit_name | email_addr    |
			  | TW           | Taipei        | Moxa     | SW3           | moxa@moxa.com |
		*     "HOST" connect "DUT" to download CSR
		*     "HOST" generate signed certificate base on CSR
		*     "HOST" connect "DUT" to import Certificate from CSR
		
		When  "DUT" uses auto-generated default certificate
		Then  "HOST" cannot establish a secure connection to "DUT"
		
		When  "DUT" uses imported certificate from Local Certificate Database
		Then  "HOST" can establish a secure connection to "DUT"

