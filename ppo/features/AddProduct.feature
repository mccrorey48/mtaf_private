@regression
Feature: Add product to cart

    Scenario: Login and click summer dresses
    When I open automationpractice website
    And I login with username "martin@xyz.com" and password "00222"
    Then I hover on women menu item and click summer dresses

    Scenario: Click summer dress and add one to cart
    When I open automationpractice website
    And I login with username "martin@xyz.com" and password "00222"
    And I hover on women menu item and click summer dresses
    Then I add a summer dress to cart