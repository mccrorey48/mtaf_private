#@regression
Feature: As a user I want to use and manage my voicemail lists

  Background: a new voicemail is shown in the New Voicemails view
    Given I go to the home screen
    When  I touch the "Voicemail" button
    Then  the "Voicemail" view is present
    When  I touch the "NEW" tab
    Then  [voicemail] I see my existing new voicemails
    When  I receive a new voicemail
    Then  [voicemail] the new voicemail is the first "NEW" item listed

  @regression
  Scenario: I listen to a selected new voicemail
    When  [voicemail] I touch the top voicemail element
    Then  [voicemail] a voicemail detail window appears
    And   [voicemail] the voicemail audio plays back

  @regression
  Scenario: I call the contact that left a new voicemail
    When  [voicemail] I touch the top voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the handset icon
    Then  [active_call] an "Active Call" window appears
    And   [voicemail] my phone calls the voicemail sender

  @regression
  Scenario: I delete a new voicemail
    When  [voicemail] I touch the top voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the Delete icon
    Then  [voicemail] the voicemail detail window disappears
    And   [voicemail] the new voicemail is no longer listed

  @regression
  Scenario: I save a new voicemail
    When  [voicemail] I touch the top voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the Save icon
    Then  [voicemail] the voicemail detail window disappears
    And   [voicemail] the new voicemail is no longer listed
    When  I touch the "SAVED" tab
    Then  [voicemail] the new voicemail is the first "SAVED" item listed

  @regression
  Scenario: I listen to a selected saved voicemail
    When  [voicemail] I touch the top voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the Save icon
    Then  [voicemail] the voicemail detail window disappears
    And   [voicemail] the new voicemail is no longer listed
    When  I touch the "SAVED" tab
    Then  [voicemail] the new voicemail is the first "SAVED" item listed
    When  [voicemail] I touch the top voicemail element
    Then  [voicemail] a voicemail detail window appears
    And   [voicemail] the voicemail audio plays back

  @regression
  Scenario: I call the contact that left a saved voicemail
    When  [voicemail] I touch the top voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the Save icon
    Then  [voicemail] the voicemail detail window disappears
    And   [voicemail] the new voicemail is no longer listed
    When  I touch the "SAVED" tab
    Then  [voicemail] the new voicemail is the first "SAVED" item listed
    When  [voicemail] I touch the top voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the handset icon
    Then  [active_call] an "Active Call" window appears
    And   [voicemail] my phone calls the voicemail sender

  @regression
  Scenario: I delete a saved voicemail
    When  [voicemail] I touch the top voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the Save icon
    Then  [voicemail] the voicemail detail window disappears
    And   [voicemail] the new voicemail is no longer listed
    When  I touch the "SAVED" tab
    Then  [voicemail] the new voicemail is the first "SAVED" item listed
    When  [voicemail] I touch the top voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the Delete icon
    Then  [voicemail] the voicemail detail window disappears
    And   [voicemail] the new voicemail is no longer listed

  @regression
  Scenario: I move a voicemail from the trash list to the saved list
    When  [voicemail] I touch the top voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the Delete icon
    Then  [voicemail] the voicemail detail window disappears
    And   [voicemail] the new voicemail is no longer listed
    When  I touch the "TRASH" tab
    Then  [voicemail] the new voicemail is the first "TRASH" item listed
    When  [voicemail] I touch the top voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the Save icon
    Then  [voicemail] the voicemail detail window disappears
    And   [voicemail] the new voicemail is no longer listed
    When  I touch the "SAVED" tab
    Then  [voicemail] the new voicemail is the first "SAVED" item listed

  Scenario: I forward a voicemail to a coworker
    When  [voicemail] I touch the top voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the Forward icon
    Then  [voicemail] a list of Coworker contacts appears
    And   [voicemail] a keypad appears
    When  [voicemail] I use the keypad to filter the list of contacts
    And   [voicemail] I touch a contact element
    Then  [voicemail] I can choose Cancel or OK by touching the corresponding button
    When  I touch "OK"
    Then  [voicemail] the voicemail is still the first item in the view
    And   [voicemail] the voicemail is also available in the destination contact's new voicemails list

