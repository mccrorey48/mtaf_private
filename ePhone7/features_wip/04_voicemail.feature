Feature: As a user I want to use and manage my voicemail lists

  Background: A new voicemail is shown in the New Voicemails view
    Given I am logged in to the ePhone7
    Then I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen
    When I touch the Voicemail button
    Then I see the New, Saved and Trash tabs at the top of the screen
    When I touch the New tab
    And I receive a new voicemail
    Then The new voicemail is the first item listed

  Scenario: I want to listen to a selected new voicemail
    When I touch the new voicemail element
    Then A voicemail detail window appears
    And The voicemail audio plays back

  Scenario: I want to call the contact that left a new voicemail
    When I touch the new voicemail element
    Then A voicemail detail window appears
    When I touch the handset icon
    Then The voicemail detail window disappears
    And My phone calls the voicemail sender

  Scenario: I want to delete a new voicemail
    When I touch the new voicemail element
    Then A voicemail detail window appears
    When I touch the Delete icon
    Then The voicemail detail window disappears
    And The voicemail is no longer listed

  Scenario: I want to save a new voicemail
    When I touch the new voicemail element
    Then A voicemail detail window appears
    When I touch the Save icon
    Then The voicemail detail window disappears
    And The voicemail is no longer listed
    When I touch the Saved tab
    Then The voicemail is the first item listed

  Scenario: I want to listen to a selected saved voicemail
    When I touch the new voicemail element
    Then A voicemail detail window appears
    When I touch the Save icon
    Then The voicemail detail window disappears
    And The voicemail is no longer listed
    When I touch the Saved tab
    Then The voicemail is the first item listed
    When I touch the voicemail element
    Then A voicemail detail window appears
    And The voicemail audio plays back

  Scenario: I want to call the contact that left a saved voicemail
    When I touch the new voicemail element
    Then A voicemail detail window appears
    When I touch the Save icon
    Then The voicemail detail window disappears
    And The voicemail is no longer listed
    When I touch the Saved tab
    Then The voicemail is the first item listed
    When I touch the voicemail element
    Then A voicemail detail window appears
    When I touch the handset icon
    Then The voicemail detail window disappears
    And My phone calls the voicemail sender

  Scenario: I want to delete a saved voicemail
    When I touch the new voicemail element
    Then A voicemail detail window appears
    When I touch the Save icon
    Then The voicemail detail window disappears
    And The voicemail is no longer listed
    When I touch the Saved tab
    Then The voicemail is the first item listed
    When I touch the voicemail element
    Then A voicemail detail window appears
    When I touch the Delete icon
    Then The voicemail detail window disappears
    And The voicemail is no longer listed

  Scenario: I want to delete a saved voicemail
    When I touch the new voicemail element
    Then A voicemail detail window appears
    When I touch the Save icon
    Then The voicemail detail window disappears
    And The voicemail is no longer listed
    When I touch the Saved tab
    Then The voicemail is the first item listed
    When I touch the voicemail element
    Then A voicemail detail window appears
    When I touch the Delete icon
    Then The voicemail detail window disappears
    And The voicemail is no longer listed

  Scenario: I want to move a voicemail from the trash list to the saved list
    When I touch the new voicemail element
    Then A voicemail detail window appears
    When I touch the Delete icon
    Then The voicemail detail window disappears
    And The voicemail is no longer listed
    When I touch the Trash tab
    Then The voicemail is the first item listed
    When I touch the voicemail element
    Then A voicemail detail window appears
    When I touch the Save icon
    Then The voicemail detail window disappears
    And The voicemail is no longer listed
    When I touch the Saved tab
    Then The voicemail is the first item listed

  Scenario: I want to forward a voicemail to a coworker
    When I touch the new voicemail element
    Then A voicemail detail window appears
    When I touch the Forward icon
    Then A list of Coworker contacts appears
    And A keypad appears
    When I use the keypad to filter the list of contacts
    And I touch a contact element
    Then I can choose Cancel or OK by touching the corresponding button
    When I choose OK
    Then The voicemail is still the first item in the view
    And The voicemail is also available in the destination contact's new voicemails list

