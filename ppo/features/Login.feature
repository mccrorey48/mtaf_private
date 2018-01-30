@regression
Feature: Login to portal

  Scenario: Login and logout
    When I open automationpractice website
    And I login with username "martin@xyz.com" and password "00222"
    Then I verify that I successfully logged in bymtaf_logging out
