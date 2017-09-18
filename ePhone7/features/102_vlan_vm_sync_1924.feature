@unimplemented
Feature: As a user I want to keep access to my voicemail after I stop using a VLAN (R2D2-1924)

  Background: I have new and saved voicemails while on a VLAN
    Given I go to the home screen
    When  [user] I touch the Preferences icon
    Then  [prefs] the Preferences window appears
    And   [prefs] I close all open submenus
    When  I touch the "System" menu category
    Then  [prefs] A submenu appears with a "Network" option
    When  I touch the "Network" option
    Then  [network] I see the Network Settings view
    And   [network] I touch the VLAN Enable button
    And   [network] the Enable button is active
    And   [network] the Disable button is inactive
    When  [network] I enter a VLAN identifier between 1 and 4094
    And   [network] I enter a VLAN priority between 0 and 7
    And   I touch "Save and Reboot"
    Then  [network] The reboot alert window appears
    And   I wait for the phone to restart

  Scenario: I have my new and saved voicemails after disabling the VLAN
    Given I have at least one saved voicemail
    And   I have at least one new voicemail
    And   I go to the New Voicemail view
    Then  my new voicemails are listed
    When  I go to the Saved Voicemail view
    Then  my saved voicemails are listed
    When  [network] I touch the VLAN Disable button
    Then  [network] the Disable button is active
    When  I go to the New Voicemail view
    Then  my new voicemails are listed
    When  I go to the Saved Voicemail view
    Then  my saved voicemails are listed

