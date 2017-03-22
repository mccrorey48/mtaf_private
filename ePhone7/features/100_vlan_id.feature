Feature: As a user I want to set up the VLAN

  Background: I am at the Network Settings view
#    Given I am logged in to the ePhone7
#    When I touch the Preferences icon
#    Then the Preferences window appears
#    When I touch the "System" menu category
#    Then A submenu appears with a "Network" option
#    When I touch the "Network" option
#    Then I see the Network Settings view

  @wip
  Scenario: I can set a valid VLAN priority
    Given VLAN is enabled
    When I enter a VLAN identifier between 1 and 4094
    And I enter a VLAN priority between 0 and 7
    And I touch "Save and Reboot"
    Then I do not see a warning message and the phone reboots

  @wip
  Scenario: I can't set an invalid VLAN ID
    Given VLAN is enabled
    When I enter a VLAN identifier greater than 4094
    And I enter a VLAN priority between 0 and 7
    And I touch "Save and Reboot"
    Then I see a warning message and the phone does not reboot
    When I touch "OK"
    Then I see the Network Settings view

  @wip
  Scenario: I can't set an invalid VLAN prority
    Given VLAN is enabled
    When I enter a VLAN identifier between 1 and 4094
    And I enter a VLAN priority greater than 7
    And I touch "Save and Reboot"
    Then I see a warning message and the phone does not reboot
    When I touch "OK"
    Then I see the Network Settings view
