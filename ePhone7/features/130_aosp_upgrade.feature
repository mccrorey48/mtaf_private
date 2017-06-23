@regression
Feature: As a user I want to to update my phone's software to the latest version

  Scenario: Performing an online upgrade from 2.1.3/1.0.10 to alpha
    Given I am logged in to the ePhone7
    And   I downgrade my aosp to 2.1.3 and app to 1.0.10
    Then  I perform an OTA upgrade

