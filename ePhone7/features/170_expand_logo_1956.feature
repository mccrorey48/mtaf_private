@regression
Feature: The home screen logo width should accomodate the new ePhone7 logo (R2D2-1956)

  Scenario: verify the logo width is at least 440 pixels
    Given I go to the home screen
    And   [user] I touch the home button
    When  [home] I get the logo element from the home screen
    Then  [home] the logo width is at least 430 pixels