Feature: The version of the software should be correct

  @required
  Scenario: I want to be using the correct version of the ePhone7 software
    Given I am logged in to the ePhone7
    When I touch the Preferences icon
    Then [prefs] the Preferences window appears
    When I touch the "System" menu category
    And I touch the "About" menu item
    Then The correct version is displayed