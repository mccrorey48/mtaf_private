Feature: As a user I want to set up the VLAN (R2D2-1948)

  Background: I am at the Network Settings view and VLAN is enabled
    Given I am logged in to the ePhone7
    When I touch the Preferences icon
    Then the Preferences window appears
    When I touch the "System" menu category
    Then A submenu appears with a "Network" option
    When I touch the "Network" option
    Then I see the Network Settings view
    And I enable VLAN

  @wip @sprint
  Scenario: I set a valid VLAN ID and priority
    When I enter a VLAN identifier between 1 and 4094
    And I enter a VLAN priority between 0 and 7
    And I touch "Save and Reboot"
    Then The reboot alert window appears

#  @wip
  Scenario: I can't set an invalid VLAN ID
    Given The VLAN Enable button is active
    When I enter a VLAN identifier greater than 4094
    And I enter a VLAN priority between 0 and 7
    And I touch "Save and Reboot"
    Then I see a warning message and the phone does not reboot
    When I touch "OK"
    Then I see the Network Settings view

#  @wip
  Scenario: I can't set an invalid VLAN prority
    Given The VLAN Enable button is active
    When I enter a VLAN identifier between 1 and 4094
    And I enter a VLAN priority greater than 7
    And I touch "Save and Reboot"
    Then I see a warning message and the phone does not reboot
    When I touch "OK"
    Then I see the Network Settings view

#  @wip
  Scenario: I disable VLAN
    Given The VLAN Enable button is active
    When I touch the VLAN Disable button
    And the Disable button is active