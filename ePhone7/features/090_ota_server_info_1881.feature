Feature: As a user I should be able to see the OTA server setting (R2D2-1881)

  @wip
  Scenario: I want to see the OTA server setting
    Given I am logged in to the ePhone7
    Then I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen
    When I touch the Dial button
    Then The Dial view appears
    When I dial *7763#
    And I touch the call button
    Then the "OTA Server Update" popup appears
    And the message "Production OTA Server Enabled" is shown
    When I touch "OK" on the popup
    Then the "OTA Server Update" popup disappears
    When I dial *682#
    And I touch the call button
    Then The Current OTA Server popup appears
    And The message "Current OTA Server: Production" is shown
    When I touch "OK" on the popup
    Then The Current OTA Server popup disappears
