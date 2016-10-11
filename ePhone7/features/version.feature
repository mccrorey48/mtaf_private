Feature: The version of the software matches the command-line setting

  Scenario: Get version from Preferences->About And Compare
    Given I go to the preferences view
    When I touch the "System" menu category
    And I touch the "About" menu item
    Then The correct version is displayed