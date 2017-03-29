Feature: As a user I should be able to see the OTA server setting (R2D2-1881)

  @sprint
  Scenario: I want to see the OTA server setting
    Given I am logged in to the ePhone7
    Then I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen
    When I touch the Dial button
    Then the Dial view appears
    When I dial the Production OTA Server direct code
    And I touch the Call button
    Then the "OTA Server Update" popup appears
    And the message "Production OTA Server Enabled" is shown
    When I touch "OK" on the popup
    Then the "OTA Server Update" popup disappears
    When I dial the Current OTA Server direct code
    And I touch the Call button
    Then the Current OTA Server popup appears
    And the message "Current OTA Server: Production" is shown
    When I touch "OK" on the popup
    Then the Current OTA Server popup disappears

  @sprint
  Scenario: I want to change the OTA server setting to Alpha
    Given I am logged in to the ePhone7
    Then I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen
    When I touch the Dial button
    Then the Dial view appears
    When I dial the Production OTA Server direct code
    And I touch the call button
    Then the "OTA Server Update" popup appears
    And the message "Production OTA Server Enabled" is shown
    When I touch "OK" on the popup
    Then the "OTA Server Update" popup disappears
    When I dial the Current OTA Server direct code
    And I touch the call button
    Then the Current OTA Server popup appears
    And the message "Current OTA Server: Production" is shown
    When I touch "OK" on the popup
    Then the Current OTA Server popup disappears
    When I dial the Alpha OTA Server direct code
    And I touch the call button
    Then the "OTA Server Update" popup appears
    And the message "Alpha OTA Server Enabled" is shown
    When I touch "OK" on the popup
    Then the "OTA Server Update" popup disappears
    When I dial the Current OTA Server direct code
    And I touch the call button
    Then the Current OTA Server popup appears
    And the message "Current OTA Server: Alpha" is shown
    When I touch "OK" on the popup
    Then the Current OTA Server popup disappears

  @sprint
  Scenario: I want to change the OTA server setting to Beta
    Given I am logged in to the ePhone7
    Then I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen
    When I touch the Dial button
    Then the Dial view appears
    When I dial the Production OTA Server direct code
    And I touch the call button
    Then the "OTA Server Update" popup appears
    And the message "Production OTA Server Enabled" is shown
    When I touch "OK" on the popup
    Then the "OTA Server Update" popup disappears
    When I dial the Current OTA Server direct code
    And I touch the call button
    Then the Current OTA Server popup appears
    And the message "Current OTA Server: Production" is shown
    When I touch "OK" on the popup
    Then the Current OTA Server popup disappears
    When I dial the Beta OTA Server direct code
    And I touch the call button
    Then the "OTA Server Update" popup appears
    And the message "Beta OTA Server Enabled" is shown
    When I touch "OK" on the popup
    Then the "OTA Server Update" popup disappears
    When I dial the Current OTA Server direct code
    And I touch the call button
    Then the Current OTA Server popup appears
    And the message "Current OTA Server: Beta" is shown
    When I touch "OK" on the popup
    Then the Current OTA Server popup disappears

  @sprint
  Scenario: I want to change the OTA server setting to Production
    Given I am logged in to the ePhone7
    Then I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen
    When I touch the Dial button
    Then the Dial view appears
    When I dial the Beta OTA Server direct code
    And I touch the call button
    Then the "OTA Server Update" popup appears
    And the message "Beta OTA Server Enabled" is shown
    When I touch "OK" on the popup
    Then the "OTA Server Update" popup disappears
    When I dial the Current OTA Server direct code
    And I touch the call button
    Then the Current OTA Server popup appears
    And the message "Current OTA Server: Beta" is shown
    When I touch "OK" on the popup
    Then the Current OTA Server popup disappears
    When I dial the Production OTA Server direct code
    And I touch the call button
    Then the "OTA Server Update" popup appears
    And the message "Production OTA Server Enabled" is shown
    When I touch "OK" on the popup
    Then the "OTA Server Update" popup disappears
    When I dial the Current OTA Server direct code
    And I touch the call button
    Then the Current OTA Server popup appears
    And the message "Current OTA Server: Production" is shown
    When I touch "OK" on the popup
    Then the Current OTA Server popup disappears
