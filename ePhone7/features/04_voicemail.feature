#@regression
Feature: As a user I want to use and manage my voicemail lists

  Background: a new voicemail is shown in the New Voicemails view
    Given I am logged in to the ePhone7
    Then  [user] I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen
    And   I have at least one saved voicemail
    And   I have at least one new voicemail
    When  [user] I touch the Voicemail button
    Then  [voicemail] I see the New, Saved and Trash tabs at the top of the screen
    When  [voicemail] I touch the New tab
    And   I receive a new voicemail
    Then  [voicemail] the new voicemail is the first item listed

  Scenario: I listen to a selected new voicemail
    When  [voicemail] I touch the new voicemail element
    Then  [voicemail] a voicemail detail window appears
    And   [voicemail] the voicemail audio plays back

  Scenario: I call the contact that left a new voicemail
    When  [voicemail] I touch the new voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the handset icon
    Then  [voicemail] the voicemail detail window disappears
    And   my phone calls the voicemail sender

  Scenario: I delete a new voicemail
    When  [voicemail] I touch the new voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the Delete icon
    Then  [voicemail] the voicemail detail window disappears
    And   [voicemail] the voicemail is no longer listed

  Scenario: I save a new voicemail
    When  [voicemail] I touch the new voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the Save icon
    Then  [voicemail] the voicemail detail window disappears
    And   [voicemail] the voicemail is no longer listed
    When  [voicemail] I touch the Saved tab
    Then  [voicemail] the voicemail is the first item listed

  Scenario: I listen to a selected saved voicemail
    When  [voicemail] I touch the new voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the Save icon
    Then  [voicemail] the voicemail detail window disappears
    And   [voicemail] the voicemail is no longer listed
    When  [voicemail] I touch the Saved tab
    Then  [voicemail] the voicemail is the first item listed
    When  [voicemail] I touch the voicemail element
    Then  [voicemail] a voicemail detail window appears
    And   [voicemail] the voicemail audio plays back

  Scenario: I call the contact that left a saved voicemail
    When  [voicemail] I touch the new voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the Save icon
    Then  [voicemail] the voicemail detail window disappears
    And   [voicemail] the voicemail is no longer listed
    When  [voicemail] I touch the Saved tab
    Then  [voicemail] the voicemail is the first item listed
    When  [voicemail] I touch the voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the handset icon
    Then  [voicemail] the voicemail detail window disappears
    And   my phone calls the voicemail sender

  Scenario: I delete a saved voicemail
    When  [voicemail] I touch the new voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the Save icon
    Then  [voicemail] the voicemail detail window disappears
    And   [voicemail] the voicemail is no longer listed
    When  [voicemail] I touch the Saved tab
    Then  [voicemail] the voicemail is the first item listed
    When  [voicemail] I touch the voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the Delete icon
    Then  [voicemail] the voicemail detail window disappears
    And   [voicemail] the voicemail is no longer listed

  Scenario: I delete a saved voicemail
    When  [voicemail] I touch the new voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the Save icon
    Then  [voicemail] the voicemail detail window disappears
    And   [voicemail] the voicemail is no longer listed
    When  [voicemail] I touch the Saved tab
    Then  [voicemail] the voicemail is the first item listed
    When  [voicemail] I touch the voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the Delete icon
    Then  [voicemail] the voicemail detail window disappears
    And   [voicemail] the voicemail is no longer listed

  Scenario: I move a voicemail from the trash list to the saved list
    When  [voicemail] I touch the new voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the Delete icon
    Then  [voicemail] the voicemail detail window disappears
    And   [voicemail] the voicemail is no longer listed
    When  [voicemail] I touch the Trash tab
    Then  [voicemail] the voicemail is the first item listed
    When  [voicemail] I touch the voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the Save icon
    Then  [voicemail] the voicemail detail window disappears
    And   [voicemail] the voicemail is no longer listed
    When  [voicemail] I touch the Saved tab
    Then  [voicemail] the voicemail is the first item listed

  Scenario: I forward a voicemail to a coworker
    When  [voicemail] I touch the new voicemail element
    Then  [voicemail] a voicemail detail window appears
    When  [voicemail] I touch the Forward icon
    Then  [voicemail] a list of Coworker contacts appears
    And   [voicemail] a keypad appears
    When  [voicemail] I use the keypad to filter the list of contacts
    And   [voicemail] I touch a contact element
    Then  [voicemail] I can choose Cancel or OK by touching the corresponding button
    When  [voicemail] I touch OK
    Then  [voicemail] the voicemail is still the first item in the view
    And   [voicemail] the voicemail is also available in the destination contact's new voicemails list

