# Copyright (C) MOXA Inc. All rights reserved.
#
#This software is distributed under the terms of the MOXA SOFTWARE NOTICE.
#
#See the file MOXA-SOFTWARE-NOTICE for details.
#
#
# Reference: https://moxanbginsngfw.atlassian.net/browse/TCR-683

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

    Scenario Outline: Check every privilege via default account
        When logout "DUT"
        And  login "DUT" via <account>
        Then check account privilege <action1> show system information on "DUT"
        And  check account privilege <action2> enter configure level on "DUT"
        And  check account privilege <action3> add a new user on "DUT"
    @sanity @user_account @edrg9010_v2 @edrg9010_v3 @edr8010_v3 @tn4900_v3
    Examples:
          | account     | action1 | action2 | action3 |
          | admin       | can     | can     | can     |
          | configadmin | can     | can     | can not |
          | user        | can     | can not | can not |
