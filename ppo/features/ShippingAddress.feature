Feature: Add product to cart

    Scenario: Verify address and verify shipping address
    When I open automationpractice website
    And I login with username "martin@xyz.com" and password "00222"
    And I hover on women menu item and click summer dresses
    And I add a summer dress to cart
    And verify the item and price
    And I verify the address and proceed
    Then I verify shipping address and proceed