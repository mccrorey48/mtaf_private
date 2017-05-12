@required @regression
Feature: The version of the software should be correct

  Scenario: I want to be using the correct version of the ePhone7 software
    Given I am logged in to the ePhone7
    When  [user] I touch the Preferences icon
    Then  [prefs] the Preferences window appears
    When  [prefs] I touch the "System" menu category
    And   [prefs] I touch the "About ePhone7" menu item
    Then  [prefs] I read the displayed versions for the app and AOSP
    When  [prefs] I touch the "X" icon
    Then  [prefs] the Preferences window disappears
    And   [prefs] I upgrade the phone if the versions are not correct

