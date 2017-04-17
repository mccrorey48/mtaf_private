@sprint @regression
Feature: As a user I should be able to see the OTA server setting (R2D2-1881)

  Background: I am at the Dial view
    Given [background] I am logged in to the ePhone7
    Then  [background] I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen
    When  [background] I touch the Dial button
    Then  [background] the Dial view appears

  Scenario: I want to see the OTA server setting
    When  I dial the Production OTA Server direct code
    And   I touch the Call button
    Then  the "OTA Server Update" popup appears
    And   the message "Production OTA Server Enabled" is shown
    When  I touch "OK" on the popup
    Then  the "OTA Server Update" popup disappears
    When  I dial the Current OTA Server direct code
    And   I touch the Call button
    Then  the Current OTA Server popup appears
    And   the message "Current OTA Server: Production" is shown
    When  I touch "OK" on the popup
    Then  the Current OTA Server popup disappears

  Scenario: I want to change the OTA server setting to Alpha
    When  I dial the Production OTA Server direct code
    And   I touch the call button
    Then  the "OTA Server Update" popup appears
    And   the message "Production OTA Server Enabled" is shown
    When  I touch "OK" on the popup
    Then  the "OTA Server Update" popup disappears
    When  I dial the Current OTA Server direct code
    And   I touch the call button
    Then  the Current OTA Server popup appears
    And   the message "Current OTA Server: Production" is shown
    When  I touch "OK" on the popup
    Then  the Current OTA Server popup disappears
    When  I dial the Alpha OTA Server direct code
    And   I touch the call button
    Then  the "OTA Server Update" popup appears
    And   the message "Alpha OTA Server Enabled" is shown
    When  I touch "OK" on the popup
    Then  the "OTA Server Update" popup disappears
    When  I dial the Current OTA Server direct code
    And   I touch the call button
    Then  the Current OTA Server popup appears
    And   the message "Current OTA Server: Alpha" is shown
    When  I touch "OK" on the popup
    Then  the Current OTA Server popup disappears

  Scenario: I want to change the OTA server setting to Beta
    When  I dial the Production OTA Server direct code
    And   I touch the call button
    Then  the "OTA Server Update" popup appears
    And   the message "Production OTA Server Enabled" is shown
    When  I touch "OK" on the popup
    Then  the "OTA Server Update" popup disappears
    When  I dial the Current OTA Server direct code
    And   I touch the call button
    Then  the Current OTA Server popup appears
    And   the message "Current OTA Server: Production" is shown
    When  I touch "OK" on the popup
    Then  the Current OTA Server popup disappears
    When  I dial the Beta OTA Server direct code
    And   I touch the call button
    Then  the "OTA Server Update" popup appears
    And   the message "Beta OTA Server Enabled" is shown
    When  I touch "OK" on the popup
    Then  the "OTA Server Update" popup disappears
    When  I dial the Current OTA Server direct code
    And   I touch the call button
    Then  the Current OTA Server popup appears
    And   the message "Current OTA Server: Beta" is shown
    When  I touch "OK" on the popup
    Then  the Current OTA Server popup disappears

  Scenario: I want to change the OTA server setting to Production
    When  I dial the Beta OTA Server direct code
    And   I touch the call button
    Then  the "OTA Server Update" popup appears
    And   the message "Beta OTA Server Enabled" is shown
    When  I touch "OK" on the popup
    Then  the "OTA Server Update" popup disappears
    When  I dial the Current OTA Server direct code
    And   I touch the call button
    Then  the Current OTA Server popup appears
    And   the message "Current OTA Server: Beta" is shown
    When  I touch "OK" on the popup
    Then  the Current OTA Server popup disappears
    When  I dial the Production OTA Server direct code
    And   I touch the call button
    Then  the "OTA Server Update" popup appears
    And   the message "Production OTA Server Enabled" is shown
    When  I touch "OK" on the popup
    Then  the "OTA Server Update" popup disappears
    When  I dial the Current OTA Server direct code
    And   I touch the call button
    Then  the Current OTA Server popup appears
    And   the message "Current OTA Server: Production" is shown
    When  I touch "OK" on the popup
    Then  the Current OTA Server popup disappears
