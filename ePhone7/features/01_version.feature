Feature: The version of the software should be correct

  @required
  Scenario: I want to be using the correct version of the ePhone7 software
    Given I am logged in to the ePhone7
    When  [user] I touch the Preferences icon
    Then  [prefs] the Preferences window appears
    When  [prefs] I touch the "System" menu category
    And   [prefs] I touch the "About" menu item
    Then  [prefs] the correct version is displayed