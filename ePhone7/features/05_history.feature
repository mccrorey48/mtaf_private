@regression
Feature: As a user I want to see my call history and make calls from the listed items

  Background: I am in the History view
    Given [background] I am logged in to the ePhone7
    Then  [background] I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen
    When  [background] I touch the History button
    Then  [background] I see the All and Missed tabs at the top of the screen

  Scenario: I want to see an answered call indicated on the All History view
    Given I receive a call
    Then  The incoming call window appears
    And   I answer the call
    When  I end the call
    Then  The incoming call window disappears
    When  I touch the All tab
    Then  I see the call at the top of the All History view
    And   The call has a blue handset icon with an incoming arrow

  Scenario: I want to see a missed call indicated on the All History view
    Given I receive a call
    Then  The incoming call window appears
    And   I ignore the call
    When  The caller ends the call
    Then  The incoming call window disappears
    When  I touch the All tab
    Then  I see the call at the top of the All History view
    And   The call has a red handset icon with a missed arrow

  Scenario: I want to see a missed call indicated on the Missed History view
    Given I receive a call
    Then  The incoming call window appears
    And   I ignore the call
    When  The caller ends the call
    Then  The incoming call window disappears
    When  I touch the Missed tab
    Then  I see the call at the top of the Missed History view
    And   The call has a red handset icon with a missed arrow

  Scenario: I want to see a voicemail call indicated on the All History view
    Given I receive a call
    Then  The incoming call window appears
    And   I ignore the call
    When  The caller leaves a voicemail
    Then  The incoming call window disappears
    When  The caller ends the call
    And   I touch the All tab
    Then  I see the call at the top of the All History view
    And   The call has a voicemail icon


  Scenario: I want to see an outgoing call indicated on the All History view
    Given I make a call to a coworker contact
    Then  The in-call window appears
    When  I end the call
    Then  The in-call window disappears
    When  I touch the All tab
    Then  I see the call at the top of the All History view
    And   The call has a green handset icon with an outgoing arrow

  Scenario: I want to call back an answered call indicated on the All History view
    Given I receive a call
    Then  The incoming call window appears
    And   I answer the call
    When  I end the call
    Then  The incoming call window disappears
    When  I touch the All tab
    Then  I see the call at the top of the All History view
    And   The call has a blue handset icon with an incoming arrow
    When  [history] I touch the handset icon
    Then  My phone calls back the caller

  Scenario: I want to call back a missed call indicated on the All History view
    Given I receive a call
    Then  The incoming call window appears
    And   I ignore the call
    When  The caller ends the call
    Then  The incoming call window disappears
    When  I touch the All tab
    Then  I see the call at the top of the All History view
    And   The call has a red handset icon with a missed arrow
    When  [history] I touch the handset icon
    Then  My phone calls back the caller

  Scenario: I want to call back a missed call indicated on the Missed History view
    Given I receive a call
    Then  The incoming call window appears
    And   I ignore the call
    When  The caller ends the call
    Then  The incoming call window disappears
    When  I touch the Missed tab
    Then  I see the call at the top of the Missed History view
    And   The call has a red handset icon with a missed arrow
    When  [history] I touch the handset icon
    Then  My phone calls back the caller

  Scenario: I want to listen to a voicemail indicated on the All History view
    Given I receive a call
    Then  The incoming call window appears
    And   I ignore the call
    When  The caller leaves a voicemail
    Then  The incoming call window disappears
    When  The caller ends the call
    And   I touch the All tab
    Then  I see the call at the top of the All History view
    And   The call has a voicemail icon
    When  I touch the voicemail icon
    Then  [voicemail] A voicemail detail window appears
    And   [voicemail] The voicemail audio plays back

  Scenario: I want to call back an outgoing call indicated on the All History view
    Given I make a call to a coworker contact
    Then  The in-call window appears
    When  I end the call
    Then  The in-call window disappears
    When  I touch the All tab
    Then  I see the call at the top of the All History view
    And   The call has a green handset icon with an outgoing arrow
    When  [history] I touch the handset icon
    Then  My phone calls back the caller

