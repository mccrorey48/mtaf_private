@regression @critical
Feature: The version of the software should be correct

  Background: I am at the Home screen
    Given I go to the home screen

#  Scenario: I upgrade the phone if the versions are not correct
#    Then  I upgrade the phone if the versions are not correct

  Scenario: I want to be using the correct version of the ePhone7 software
    When  [user] I touch the Preferences icon
    Then  [prefs] the Preferences window appears
    And   [prefs] I close all open submenus
    When  I touch "System"
    And   I touch "About ePhone7"
    Then  [prefs] I read the displayed versions for the app and AOSP
    And   [prefs] the installed versions are displayed correctly
    And   the current versions are installed
    When  [prefs] I touch the "X" icon
    Then  [prefs] the Preferences window disappears

