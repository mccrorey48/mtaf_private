@regression
Feature: New dialpad for InCall screen (R2D2-2143)

  Scenario: the in-call dialpad has the new button sizes
    Given I go to the home screen
    And   I receive a call
    And   I answer the call
    Then  [active_call] an "Active Call" window appears
    When  [active call] I touch "Dial"
    Then  [active_call] I see the keypad
    And   [active_call] the buttons are 150 pixels wide and 57 pixels high

