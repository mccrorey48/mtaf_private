Feature: The version of the software should be correct

  Scenario: I have to OK the Attention alert
    Given I see the Attention Alert Message
    When I touch OK
    Then The Attention Alert Message disappears

  Scenario: I have to OK the Battery Usage alert
    Given I see the Battery Usage Alert Message
    When I touch YES
    Then The Battery Usage Alert Message disappears

  Scenario: I have to allow Phone Permissions
    Given I see the Phone Permission Message
    When I touch ALLOW
    Then The Phone Permission Message disappears

  Scenario: I have to allow Audio Recording
    Given I see the Record Audio Permission Message
    When I touch ALLOW
    Then The Record Audio Permission Message disappears
#  Scenario: I have to accept the terms and conditions the first time I log in
#    Given I see the terms and conditions screen
#    When I touch the checkbox
#    Then A check mark appears in the box
#    When I touch the Continue button
#    Then The login screen appears


