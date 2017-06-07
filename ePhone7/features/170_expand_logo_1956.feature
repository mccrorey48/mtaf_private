@regression
Feature: the home screen logo width should accomodate the new ePhone7 logo

  Scenario: verify the logo width is at lease 440 pixels
    Given I am logged in to the ePhone7
    When  [user] I get the logo element from the home screen
    Then  [user] the logo width is at least 440 pixels