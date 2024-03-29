@select @premier
Feature: Home Page Navigation

  Scenario: I want to see my Messages page
    Given I log in to the dashboard
    When I click the MESSAGES tab
    Then the Messages page appears

  Scenario: I want to see my Call History page
    Given I log in to the dashboard
    When I click the CALL HISTORY tab
    Then the Call History page appears

  Scenario: I want to see my Contacts page
    Given I log in to the dashboard
    When I click the CONTACTS tab
    Then the Contacts page appears

  Scenario: I want to see my Phones page
    Given I log in to the dashboard
    When I click the PHONES tab
    Then the Phones page appears

  Scenario: I want to see my Message Settings page
    Given I log in to the dashboard
    When I click the SETTINGS tab
    Then the Settings Menu appears
    When I click the Message Settings menu item
    Then the Message Settings page appears

