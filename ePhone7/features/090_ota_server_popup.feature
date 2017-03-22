Feature: As a user I should be able to see the OTA server setting (R2D2-1881)

  @wip
  Scenario: I want to see the OTA server setting
    Given I am at the Dial view
    When I dial *682#
    And I touch the call button
    Then The Current OTA Server popup appears
    And The popup shows the current OTA environment name
    But The popup does not show the current OTA URL
    When I touch the OK button
    Then The OTA Server popup disappears