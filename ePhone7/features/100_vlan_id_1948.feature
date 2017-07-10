Feature: As a user I want to set up the VLAN (R2D2-1948)

  Background: I am at the Network Settings view and VLAN is enabled
    Given [background] I go to the home screen
    When  [background] I touch the Preferences icon
    Then  [background] the Preferences window appears
    When  I touch the "System" menu category
    Then  [background] A submenu appears with a "Network" option
    When  I touch the "Network" option
    Then  [background] I see the Network Settings view
    And   [background] I touch the VLAN Enable button
    And   [background] the Enable button is active
    And   [background] the Disable button is inactive

  Scenario: I set a valid VLAN ID and priority
    When  I enter a VLAN identifier between 1 and 4094
    And   [network] I enter a VLAN priority between 0 and 7
    And   I touch "Save and Reboot"
    Then  [network] The reboot alert window appears
    And   I wait for the phone to restart

  Scenario: I can't set an invalid VLAN ID
    When  [network] I enter a VLAN identifier greater than 4094
    And   [network] I enter a VLAN priority between 0 and 7
    And   I touch "Save and Reboot"
    Then  [network] I see an "Invalid VLAN Identifier" alert
    When  I touch "OK" on the Invalid VLAN Identifier alert
    Then  [network] I see the Network Settings view
    And   [network] I touch the back arrow at the top of the Network Settings view
    Then  [prefs] the Preferences window appears
    When  [prefs] I touch the "X" icon
    Then  [prefs] the Preferences window disappears

  Scenario: I can't set an invalid VLAN prority
    When  I enter a VLAN identifier between 1 and 4094
    And   I enter a VLAN priority greater than 7
    And   I touch "Save and Reboot"
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
    Then  [network] I see the Network Settings view
    And   [network] I touch the back arrow at the top of the Network Settings view
    Then  [prefs] the Preferences window appears
    When  [prefs] I touch the "X" icon
    Then  [prefs] the Preferences window disappears
    And   I touch "Save and Reboot"
    Then  [network] The reboot alert window appears
    And   I wait for the phone to restart
    When  [user] I touch the Preferences icon
    Then  [prefs] the Preferences window appears
    And   [prefs] I close all open submenus
    When  I touch the "System" menu category
    Then  [prefs] A submenu appears with a "Network" option
    When  I touch the "Network" option
    Then  [network] I see the Network Settings view
    And   [network] the Disable button is active
    And   [network] the Enable button is inactive
    When  [network] I touch the back arrow at the top of the Network Settings view
    Then  [prefs] the Preferences window appears
    When  [prefs] I touch the "X" icon
    Then  [prefs] the Preferences window disappears
