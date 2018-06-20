@regression @wip
Feature: Log in only allowed with valid user ID and password

  @select
  Scenario: Log in with valid select user ID and password
    When I enter a select user ID
    And I enter a select password
    And I click the Login button
    Then the Home page appears
    And the HOME tab is selected
    And my name is displayed in the upper right corner

  @premier
  Scenario: Log in with valid premier user ID and password
    When I enter a premier user ID
    And I enter a premier password
    And I click the Login button
    Then the Home page appears
    And the HOME tab is selected
    And my name is displayed in the upper right corner

  @office_mgr
  Scenario: Log in with valid office manager user ID and password
    When I enter a office_mgr user ID
    And I enter a office_mgr password
    And I click the Login button
    Then the Home page appears
    And the HOME tab is selected
    And my name is displayed in the upper right corner

