Feature: New dialpad for Main and InCall screens (R2D2-1735)

  Scenario: the main dialpad has the new button sizes
    Given I am logged in to the ePhone7
    When  [user] I touch the Dial button
    Then  [dial] I see the keypad
    And   [dial] the buttons are x pixels wide and y pixels high
