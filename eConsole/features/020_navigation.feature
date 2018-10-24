@regression
Feature: Home Page Navigation

  @select @premier @office_mgr
  Scenario: I want to see my Messages page
    Given I log in to the dashboard
    When I click the MESSAGES tab
    Then the "Messages" page appears
    And the MESSAGES tab is selected
    And the content is correct for the "Messages" page

  @select @premier @office_mgr
  Scenario: I want to see my Call History page
    Given I log in to the dashboard
    When I click the CALL HISTORY tab
    Then the "Call History" page appears
    And the CALL HISTORY tab is selected
    And the content is correct for the "Call History" page

  @select @premier @office_mgr
  Scenario: I want to see my Contacts page
    Given I log in to the dashboard
    When I click the CONTACTS tab
    Then the "Contacts" page appears
    And the CONTACTS tab is selected
    And the content is correct for the "Contacts" page

  @select @premier @office_mgr
  Scenario: I want to see my Phones page
    Given I log in to the dashboard
    When I click the PHONES tab
    Then the "Phones" page appears
    And the PHONES tab is selected
    And the content is correct for the "Phones" page

  @select @premier @office_mgr
  Scenario: I want to see my Message Settings page
    Given I log in to the dashboard
    When I click the SETTINGS tab
    Then the Settings Menu appears
    When I click the "Message Settings" menu item
    Then the "Message Settings" page appears
    And the SETTINGS tab is selected
    And the content is correct for the "Message Settings" page

  @premier @office_mgr
  Scenario: I want to see my Allow/Block Numbers page
    Given I log in to the dashboard
    When I click the SETTINGS tab
    Then the Settings Menu appears
    When I click the "Allow/Block Numbers" menu item
    Then the "Allow/Block Numbers" page appears
    And the SETTINGS tab is selected
    And the content is correct for the "Allow/Block Numbers" Page

  @premier @office_mgr
  Scenario: I want to see my Answering Rules page
    Given I log in to the dashboard
    When I click the SETTINGS tab
    Then the Settings Menu appears
    When I click the "Answering Rules" menu item
    Then the "Answering Rules" page appears
    And the SETTINGS tab is selected
    And the content is correct for the "Answering Rules" page

  @premier @office_mgr
  Scenario: I want to see my Music on Hold page
    Given I log in to the dashboard
    When I click the SETTINGS tab
    Then the Settings Menu appears
    When I click the "Music on Hold" menu item
    Then the "Music on Hold" page appears
    And the SETTINGS tab is selected
    And the content is correct for the "Music on Hold" page

  @premier @office_mgr
  Scenario: I want to see my Time Frames page
    Given I log in to the dashboard
    When I click the SETTINGS tab
    Then the Settings Menu appears
    When I click the "Time Frames" menu item
    Then the "Time Frames" page appears
    And the SETTINGS tab is selected
    And the content is correct for the "Time Frames" page

  @select @premier @office_mgr
  Scenario: I want to see my Home page
    Given I log in to the dashboard
    When I click the HOME tab
    Then the "Home" page appears
    And the HOME tab is selected
    And the content is correct for the "Home" page

