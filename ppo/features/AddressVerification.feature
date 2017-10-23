@regression
Feature: Address verification

    Scenario: Verify summary and verify address
    When I open automationpractice website
    And I login with username "martin@xyz.com" and password "00222"
    And I hover on women menu item and click summer dresses
    And I add a summer dress to cart
    And verify the item and price
    Then I verify the address and proceed