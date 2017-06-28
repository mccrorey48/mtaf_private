Feature: As a user I want to keep access to my voicemail after I stop using a VLAN (R2D2-1924)

  Background: I have new and saved voicemails while on a VLAN
    Given [background] I go to the home screen
    When  [background] I touch the Preferences icon
    Then  [background] the Preferences window appears
    When  [background] I touch the "System" menu category
    Then  [background] A submenu appears with a "Network" option
    When  [background] I touch the "Network" option
    Then  [background] I see the Network Settings view
    And   [background] I touch the VLAN Enable button
    And   [background] the Enable button is active
    And   [background] the Disable button is inactive
    When  [background] I enter a VLAN identifier between 1 and 4094
    And   [background] I enter a VLAN priority between 0 and 7
    And   [background] I touch "Save and Reboot"
    Then  [background] The reboot alert window appears
    And   [background] I wait for the phone to restart

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

