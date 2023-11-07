Feature: [Obj Mgmt] 

    @obj @sanity @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Scenario: User-defined Service
        Given authorize CLI of "DUT"
        *     reload factory-default "DUT"
        When  create User-defined Service object with name: "test_TCP_any" on "DUT"
                | IP Protocol | Service Port |
                | TCP         | any          |
        Then  the User-defined Service object is successfully created on "DUT"
        When  create User-defined Service object with name: "test_TCP_single" on "DUT"
                | IP Protocol | Service Port |
                | TCP         | 22           |
        Then  the User-defined Service object is successfully created on "DUT"
        When  create User-defined Service object with name: "test_TCP_range" on "DUT"
                | IP Protocol | Service Port |
                | TCP         | 23-25        |
        Then  the User-defined Service object is successfully created on "DUT"

        When  create User-defined Service object with name: "test_UDP_any" on "DUT"
                | IP Protocol | Service Port |
                | UDP         | any          |
        Then  the User-defined Service object is successfully created on "DUT"
        When  create User-defined Service object with name: "test_UDP_single" on "DUT"
                | IP Protocol | Service Port |
                | UDP         | 23           |
        Then  the User-defined Service object is successfully created on "DUT"
        When  create User-defined Service object with name: "test_UDP_range" on "DUT"
                | IP Protocol | Service Port |
                | UDP         | 100-101      |
        Then  the User-defined Service object is successfully created on "DUT"

        When  create User-defined Service object with name: "test_TCPUDP_any" on "DUT"
                | IP Protocol | Service Port |
                | TCP and UDP | any          |
        Then  the User-defined Service object is successfully created on "DUT"
        When  create User-defined Service object with name: "test_TCPUDP_single" on "DUT"
                | IP Protocol | Service Port |
                | TCP and UDP | 24           |
        Then  the User-defined Service object is successfully created on "DUT"
        When  create User-defined Service object with name: "test_TCPUDP_range" on "DUT"
                | IP Protocol | Service Port |
                | TCP and UDP | 1001-1003    |
        Then  the User-defined Service object is successfully created on "DUT"

        When  create User-defined Service object with name: "test_ICMP_any" on "DUT"
                | IP Protocol | ICMP type | ICMP code |
                | ICMP        | any       | any       |
        Then  the User-defined Service object is successfully created on "DUT"
        When  create User-defined Service object with name: "test_ICMP" on "DUT"
                | IP Protocol | ICMP type | ICMP code |
                | ICMP        | 100       | 23        |
        Then  the User-defined Service object is successfully created on "DUT"

        When  create User-defined Service object with name: "test_Custom" on "DUT"
                | IP Protocol | Service Port |
                | Custom      | 255          |
        Then  the User-defined Service object is successfully created on "DUT"