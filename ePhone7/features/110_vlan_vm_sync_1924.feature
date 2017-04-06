Feature: As a user I want to keep access to my voicemail after I stop using a VLAN (R2D2-1924)

  Background: I have new and saved voicemails while on a VLAN
    Given I am logged in to the ePhone7
    And VLAN is enabled
    When I enter a VLAN identifier between 1 and 4094
    And I enter a VLAN priority between 0 and 7
    And I touch "Save and Reboot"
    Then I do not see a warning message and the phone reboots
    And I have at least one saved voicemail
    And I have at least one new voicemail
    And I go to the New Voicemail view

#  @wip
  Scenario: I have my new and saved voicemails after disabling the VLAN
    Given I go to the New Voicemail view
    Then my new voicemails are listed
    When I go to the Saved Voicemail view
    Then my saved voicemails are listed
    When I touch the VLAN Disable button
    Then the Disable button is active
    When I go to the New Voicemail view
    Then my new voicemails are listed
    When I go to the Saved Voicemail view
    Then my saved voicemails are listed

