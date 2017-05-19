@required @regression
Feature: The version of the software should be correct

  Scenario: I upgrade the phone if the versions are not correct
    Given I am logged in to the ePhone7
    Then  I upgrade the phone if the versions are not correct


  Scenario: I want to be using the correct version of the ePhone7 software
    Given I am logged in to the ePhone7
    When  [user] I touch the Preferences icon
    Then  [prefs] the Preferences window appears
    When  [prefs] I touch the "System" menu category
    And   [prefs] I touch the "About ePhone7" menu item
    Then  [prefs] I read the displayed versions for the app and AOSP
    And   [prefs] the installed versions are displayed correctly
    And   [prefs] the current versions are installed
    When  [prefs] I touch the "X" icon
    Then  [prefs] the Preferences window disappears

