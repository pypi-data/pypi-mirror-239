# Copyright (C) MOXA Inc. All rights reserved.
#
#This software is distributed under the terms of the MOXA SOFTWARE NOTICE.
#
#See the file MOXA-SOFTWARE-NOTICE for details.
#
#
# Reference: https://moxanbginsngfw.atlassian.net/browse/TCR-682

Feature: [User Account]
Topology:
 +-------------------+
 | EXECUTOR------DUT |
 +-------------------+
    Background:
        Given prepare "default" topology
        *     authorize CLI of "DUT"
        *     reload factory-default "DUT"
        *     enable telnet service on "DUT"

    Scenario Outline: Check every default account can login DUT
        When logout "DUT"
        And  login "DUT" via <account>
        Then "DUT" can be login successfully
    @sanity @user_account @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Examples:
          | account     |
          | admin       |
          | configadmin |
          | user        |