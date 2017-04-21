Feature: As a user I want to to update my phone's software to the latest version

  @wip
  Scenario: Performing an online upgrade to the Android and ePhone7 software
    Given I am logged in to the ePhone7
    And   my system version needs to be upgraded
    Then  I set the OTA server
    When  [user] I touch the Preferences icon
    Then  [prefs] the Preferences window appears
    When  [prefs] I touch the "System" menu category
    And   [prefs] I touch the "Updates" menu item
    And   [prefs] I touch the "Check for System Update" option

