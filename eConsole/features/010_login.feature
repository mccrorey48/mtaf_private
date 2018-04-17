Feature: Log in only allowed with valid user ID and password

  Background: Attempted login scenarios
    Given I go to the portal login page

  @select @premier
  Scenario: Log in with valid select user ID and password
    When I enter a user ID
    And I enter a password
    And I click the Login button
    Then the Home page appears

