Feature: [Obj Mgmt] 

    @obj @sanity @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: IP Address and Subnet
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        When  create Network Service: "Remote-Access" object with name: "test_Remote-Access" on "DUT"
        Then  the Network Service object is successfully created on "DUT"
        When  create Network Service: "Remote-Desktop" object with name: "test_Remote-Desktop" on "DUT"
        Then  the Network Service object is successfully created on "DUT"
        When  create Network Service: "Email" object with name: "test_Email" on "DUT"
        Then  the Network Service object is successfully created on "DUT"
        When  create Network Service: "File-Transfer" object with name: "test_File-Transfer" on "DUT"
        Then  the Network Service object is successfully created on "DUT"
        When  create Network Service: "Web-Access" object with name: "test_Web-Access" on "DUT"
        Then  the Network Service object is successfully created on "DUT"
        When  create Network Service: "Network-Service" object with name: "test_Network-Service" on "DUT"
        Then  the Network Service object is successfully created on "DUT"
        When  create Network Service: "Authentication" object with name: "test_Authentication" on "DUT"
        Then  the Network Service object is successfully created on "DUT"
        When  create Network Service: "VOIP-and-Streaming" object with name: "test_VOIP-and-Streaming" on "DUT"
        Then  the Network Service object is successfully created on "DUT"
        When  create Network Service: "SQL-Server" object with name: "test_SQL-Server" on "DUT"
        Then  the Network Service object is successfully created on "DUT"