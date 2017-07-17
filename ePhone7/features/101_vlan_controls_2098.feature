Feature: As a user I want to set up the VLAN (R2D2-2098)

  Background: I am at the Network Settings view and VLAN is enabled
    Given I go to the home screen
    When  [user] I touch the Preferences icon
    Then  [prefs] the preferences window appears
    And   [prefs] I close all open submenus
    When  I touch the "System" menu category
    Then  [prefs] A submenu appears with a "Network" option
    When  I touch the "Network" option
    Then  [network] I see the Network Settings view

  @regression
  Scenario: VLAN controls are present
    Then  [network] I see the VLAN controls
    And   [network] I touch the back arrow at the top of the Network Settings view
    Then  [prefs] the Preferences window appears
    When  [prefs] I touch the "X" icon
    Then  [prefs] the Preferences window disappears
