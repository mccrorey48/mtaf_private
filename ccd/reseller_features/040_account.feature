Feature: Reseller Account Management

  Background: Account management in a customer domain
    Given I log in as reseller
    And I go to the reseller domains page
    When I select a domain from the table
    Then the selected domain home page will load

  Scenario: Create an always timeframe
    When I go to the timeframes page
    And there are no timeframes listed in the table
    And I click the Add Time Frame button
    Then an Add a Timeframe modal dialog appears
    When I enter a timeframe name
    And I click the Save button
    Then the new timeframe is listed in the table
