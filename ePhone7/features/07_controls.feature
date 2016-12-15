Feature: As a user, I should be able to change the settings on my ePhone7 using control buttons on the display

  Background: I am logged in and at the Home view
    Given I am logged in to the ePhone7
    When I go to the Home view
    Then I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen

  Scenario: I want to activate Do Not Disturb
    Given The Do Not Disturb icon is blue
    When I touch the Do Not Disturb icon
    Then The Do Not Disturb icon turns red
    When Someone calls me
    Then The caller gets a voicemail prompt
    When The caller leaves a message
    And I touch the Voicemail button
    Then I see the New, Saved and Trash tabs at the top of the screen
    When I touch the New tab
    Then The new voicemail is the first item listed

  Scenario: I want to deactivate Do Not Disturb
    Given The Do Not Disturb icon is red
    When I touch the Do Not Disturb icon
    Then The Do Not Disturb icon turns blue
    When Someone calls me
    Then The incoming call window appears

  Scenario: I want to pick up a parked incoming call
    Given A call between two other accounts has been parked by the called account
    When The Call Park icon
    Then A keypad appears
    When I enter the call park queue number
    Then The caller is connected to my phone


  Scenario: I want to forward all incoming calls to a Coworker
    Given The Call Forward icon is blue
    When I touch the Call Forward icon
    Then A keypad appears with a list of contacts
    When I use the keypad to filter the list of contacts
    And I touch a contact element
    Then Only the contact I touched is listed
    When I touch the OK button
    Then The keypad disappears
    And The Call Forward icon is red
    When I go to the Home view
    Then A message indicates that calls are being forwarded to the contact

  Scenario: I want to forward all incoming calls to voicemail
    Given The Call Forward icon is blue
    When I touch the Call Forward icon
    Then A keypad appears with a list of contacts
    When I touch the Voicemail button
    Then The keypad disappears
    And The Call Forward icon is red
    When I go to the Home view
    Then A message indicates that calls are being forwarded to voicemail

  Scenario: I want to stop forwarding all calls
    Given The Call Forward icon is red
    When I touch the Call Forward icon
    Then The Call Forward icon is blue

