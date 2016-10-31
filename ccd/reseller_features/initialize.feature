Feature: Remove existing test users and conferences

  Background: Navigate to the test domain home view
    Given I log in as reseller
    And I go to the reseller domains page
    When I select a domain from the table
    Then the selected domain home page will load


  Scenario: Remove existing test conferences
    When I go to the domain conferences page
    And  I see if any test conferences are listed
    Then I click the trash can for the first test conference
    And I click Yes on the confirmation popup
    And I see the first test conference has been deleted
    Then I repeat until there are no test conferences listed


  Scenario: Remove existing test users
    When I go to the domain users page
    And I see if any test users are listed
    Then I click the trash can for the first test user
    And I click Yes on the confirmation popup
    And I see the first test user has been deleted
    Then I repeat until there are no test users listed


  Scenario: Delete all timeframes
    When I go to the timeframes page
    And I see if any timeframes are listed
    Then I click the trash can for the first timeframe
    And I click Yes on the confirmation popup
    And I see the first timeframe has been deleted
    Then I repeat until there are no timeframes listed