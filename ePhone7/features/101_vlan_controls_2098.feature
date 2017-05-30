Feature: As a user I want to set up the VLAN (R2D2-1948)

  Background: I am at the Network Settings view and VLAN is enabled
    Given [background] I am logged in to the ePhone7
    When  [background] I touch the Preferences icon
    Then  [background] the Preferences window appears
    When  [background] I touch the "System" menu category
    Then  [background] A submenu appears with a "Network" option
    When  [background] I touch the "Network" option
    Then  [background] I see the Network Settings view

  @regression
  Scenario: VLAN controls are present
    Then  [network] I see the VLAN controls
    And   [network] I touch the back arrow at the top of the Network Settings view
    Then  [prefs] the Preferences window appears
    When  [prefs] I touch the "X" icon
    Then  [prefs] the Preferences window disappears
