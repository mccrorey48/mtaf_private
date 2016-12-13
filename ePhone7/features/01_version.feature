Feature: The version of the software should be correct

  Scenario: I want to be using the correct version of the ePhone7 software
    Given I go to the Preferences view
    When I touch the "System" menu category
    And I touch the "About" menu item
    Then The correct version is displayed