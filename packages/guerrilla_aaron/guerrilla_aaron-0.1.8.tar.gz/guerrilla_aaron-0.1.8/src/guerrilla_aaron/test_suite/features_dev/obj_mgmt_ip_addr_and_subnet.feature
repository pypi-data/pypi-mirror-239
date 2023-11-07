Feature: [Obj Mgmt] 

    @obj @sanity @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: IP Address and Subnet
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        When  create IP Address and Subnet object with single IP on "DUT"
                | Name        | IP Address      |
                | test_single | 192.168.127.254 |
        Then  the single IP object is successfully created on "DUT"
        When  create IP Address and Subnet object with range IP on "DUT"
                | Name       | IP Address1    | IP Address2    |
                | test_range | 192.168.127.20 | 192.168.127.30 |
        Then  the range IP object is successfully created on "DUT"
        When  create IP Address and Subnet object with subnet IP on "DUT"
                | Name        | Subnet IP     | Subnet Mask |
                | test_subnet | 192.168.127.0 | 24          |
        Then  the subnet IP object is successfully created on "DUT"