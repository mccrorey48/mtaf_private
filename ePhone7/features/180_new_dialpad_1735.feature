Feature: New dialpad for Main and InCall screens (R2D2-1735)

  Scenario: the main dialpad has the new button sizes
    Given I go to the home screen
    When  I touch "Dial"
    Then  [dial] I see the keypad
    And   [dial] the buttons are x pixels wide and y pixels high

