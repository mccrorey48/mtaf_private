#@regression
Feature: As a user, I should be able to change the settings on my ePhone7 using control buttons on the display

  Background: I am logged in and at the Home view
    Given I am logged in to the ePhone7
    Then  [user] I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen

  Scenario: I want to activate Do Not Disturb
    Given [user] the Do Not Disturb icon is blue
    When  [user] I touch the Do Not Disturb icon
    Then  [user] the Do Not Disturb icon turns red
    When  Someone calls me
    Then  the caller gets a voicemail prompt
    When  the caller leaves a message
    And   [user] I touch the Voicemail button
    Then  [voicemail] I see the New, Saved and Trash tabs at the top of the screen
    When  [voicemail] I touch the New tab
    Then  [voicemail] the new voicemail is the first item listed

  Scenario: I want to deactivate Do Not Disturb
    Given [user] the Do Not Disturb icon is red
    When  [user] I touch the Do Not Disturb icon
    Then  [user] the Do Not Disturb icon turns blue
    When  Someone calls me
    Then  the incoming call window appears

  Scenario: I want to pick up a parked incoming call
    Given A call between two other accounts has been parked by the called account
    When  [user] I touch the Call Park icon
    Then  [user] A keypad appears
    When  [user] I enter the call park queue number
    Then  the caller is connected to my phone


  Scenario: I want to forward all incoming calls to a Coworker
    Given [user] the Call Forward icon is blue
    When  [user] I touch the Call Forward icon
    Then  [user] A keypad appears with a list of contacts
    When  [user] I use the keypad to filter the list of contacts
    And   [user] I touch a contact element
    Then  [user] Only the contact I touched is listed
    When  [user] I touch the OK button
    Then  [user] the keypad disappears
    And   [user] the Call Forward icon is red
    When  [user] I go to the Home view
    Then  A message indicates that calls are being forwarded to the contact

  Scenario: I want to forward all incoming calls to voicemail
    Given [user] the Call Forward icon is blue
    When  [user] I touch the Call Forward icon
    Then  [user] A keypad appears with a list of contacts
    When  [user] I touch the Voicemail button
    Then  [user] the keypad disappears
    And   [user] the Call Forward icon is red
    When  [user] I go to the Home view
    Then  A message indicates that calls are being forwarded to voicemail

  Scenario: I want to stop forwarding all calls
    Given [user] the Call Forward icon is red
    When  [user] I touch the Call Forward icon
    Then  [user] the Call Forward icon is blue

