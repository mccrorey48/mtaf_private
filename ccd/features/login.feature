Feature: Log in only allowed with valid user ID and password

  Background: Attempted login scenarios
    Given I go to the portal login page

  Scenario: Log in with valid user ID and password
    When I enter a valid user ID
    And I enter a valid password
    And I click the Login button
    Then the Manager Home page will load

  Scenario: Log in with valid user ID and invalid password
    When I enter a valid user ID
    And I enter a bad password
    And I click the Login button
    Then the invalid alert will appear

  Scenario: Log in with valid user ID and no password
    When I enter a valid user ID
    And I enter no password
    And I click the Login button
    Then the invalid alert will appear

  Scenario: Log in with bad user ID and valid password
    When I enter a bad user ID
    And I enter a valid password
    And I click the Login button
    Then the invalid alert will appear

  Scenario: Log in with no user ID and valid password
    When I enter no user ID
    And I enter a valid password
    And I click the Login button
    Then the invalid alert will appear

  Scenario: Log in with no user ID and no password
    When I enter no user ID
    And I enter a valid password
    And I click the Login button
    Then the invalid alert will appear
