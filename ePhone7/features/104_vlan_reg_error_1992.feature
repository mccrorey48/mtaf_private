Feature: As a user I want to enable VLAN (R2D2-1992)

  Background: I am at the Network Settings view and VLAN is disabled
    Given I go to the home screen
    When  [user] I touch the Preferences icon
    And   [prefs] I close all open submenus
    Then  [prefs] the Preferences window appears
    When  I touch the "System" menu category
    Then  [prefs] A submenu appears with a "Network" option
    When  I touch the "Network" option
    Then  [network] I see the Network Settings view
    And   [network] I touch the VLAN Disable button
    And   [network] the Disable button is active
    And   [network] the Enable button is inactive

  Scenario: I set a valid VLAN ID and priority
    When  [network] I touch the VLAN Enable button
    And   [network] the Enable button is active
    And   [network] the Disable button is inactive
    When  [network] I enter a valid VLAN identifier
    And   I touch "SAVE AND REBOOT"
    Then  [network] The reboot alert window appears
    And   the phone restarts without a register retry message

