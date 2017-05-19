@regression
Feature: [bugfix] user's other phone autoanswering should not cause crash

  Scenario: softphone on same account autoanswers

    Given there is a softphone registered on my ePhone7's user account
    And the softphone is set to autoanswer
    When I receive a call
    And the softphone answers the call
    Then the ePhone7 app should not crash
    And the caller ends the call

