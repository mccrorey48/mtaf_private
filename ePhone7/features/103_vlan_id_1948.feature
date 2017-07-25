@regression
Feature: As a user I want to set up the VLAN (R2D2-1948)

  Background: I am at the Network Settings view and VLAN is enabled
    Given I go to the home screen
    When  [user] I touch the Preferences icon
    And   [prefs] I close all open submenus
    Then  [prefs] the Preferences window appears
    When  I touch the "System" menu category
    Then  [prefs] A submenu appears with a "Network" option
    When  I touch the "Network" option
    Then  [network] I see the Network Settings view
    And   [network] I touch the VLAN Enable button
    And   [network] the Enable button is active
    And   [network] the Disable button is inactive

  Scenario: I set a valid VLAN ID and priority
    When  [network] I enter a VLAN identifier between 1 and 4094
    And   [network] I enter a VLAN priority between 0 and 7
    And   I touch "SAVE AND REBOOT"
    Then  [network] The reboot alert window appears
    And   I wait for the phone to restart

  Scenario: I can't set an invalid VLAN ID
    When  [network] I enter a VLAN identifier greater than 4094
    And   [network] I enter a VLAN priority between 0 and 7
    And   I touch "SAVE AND REBOOT"
    Then  [network] I see an "Invalid VLAN Identifier" alert
    When  I touch "OK" on the Invalid VLAN Identifier alert
    Then  [network] I see the Network Settings view
    And   [network] I touch the back arrow at the top of the Network Settings view
    Then  [prefs] the Preferences window appears
    When  [prefs] I touch the "X" icon
    Then  [prefs] the Preferences window disappears

  Scenario: I can't set an invalid VLAN prority
    When  [network] I enter a VLAN identifier between 1 and 4094
    And   [network] I enter a VLAN priority greater than 7
    And   I touch "SAVE AND REBOOT"
    Then  I see an "Invalid VLAN Priority" alert
    When  I touch "OK" on the Invalid VLAN Priority alert
    Then  [network] I see the Network Settings view
    And   [network] I touch the back arrow at the top of the Network Settings view
    Then  [prefs] the Preferences window appears
    When  [prefs] I touch the "X" icon
    Then  [prefs] the Preferences window disappears

  Scenario: I disable VLAN
    When  [network] I touch the VLAN Disable button
    And   [network] the Disable button is active
    And   [network] the Enable button is inactive
    And   I touch "SAVE AND REBOOT"
    Then  [network] The reboot alert window appears
    And   I wait for the phone to restart
