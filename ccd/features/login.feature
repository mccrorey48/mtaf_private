Feature: Log in only with valid user ID and password

  Scenario: log in with valid user ID and password
    Given I go to the portal login page
    When I enter a valid user ID
    And I enter a valid password
    And I click the Login button
    Then the Manager Home page will load