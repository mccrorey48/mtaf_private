# @regression
Feature: As a user I want to to update my phone's software to the latest version

  Scenario: Performing an online upgrade from 2.3.12 to alpha
    Given I go to the home screen
    And   I downgrade my aosp to 2.3.12
    Then  I perform an OTA upgrade

