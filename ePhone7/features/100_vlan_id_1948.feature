Feature: As a user I want to set up the VLAN (R2D2-1948)

  Background: I am at the Network Settings view and VLAN is enabled
    Given I am logged in to the ePhone7
    Then I go to the Network Settings view
    And I touch the VLAN Enable button

#  @wip
  Scenario: I set a valid VLAN ID and priority
    Given The VLAN Enable button is active
    When I enter a VLAN identifier between 1 and 4094
    And I enter a VLAN priority between 0 and 7
    And I touch "Save and Reboot"
    Then I do not see a warning message and the phone reboots

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