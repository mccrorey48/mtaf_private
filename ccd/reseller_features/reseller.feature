Feature: Reseller Home Page Navigation

  Background: Navigation in the reseller login "All Domains" view
    Given I log in as reseller

  Scenario: Go to reseller domains page
    Given I go to the reseller home page
    When I click the domains tab
    Then the reseller domains page will load

  Scenario: Go to reseller home page
    Given I go to the reseller domains page
    When I click the home tab
    Then the reseller home page will load

  Scenario: Go to reseller inventory page
    Given I go to the reseller home page
    When I click the inventory tab
    Then the reseller inventory page will load

  Scenario: Select domain using domain quick launch
    Given I go to the reseller home page
    When I use the domain quick launch to select a domain
    Then the selected domain home page will load

  Scenario: Select domain from table
    Given I go to the reseller domains page
    When I select a domain from the table
    Then the selected domain home page will load

  Scenario: Select domain using filter entry
    Given I go to the reseller domains page
    When I select a domain using the filter entry
    Then Exactly one domain is shown in the table
    And the selected domain is shown in the first row
    When I click the domain name in the table
    Then the selected domain home page will load

