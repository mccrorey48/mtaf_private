@regression
Feature: As a user I want to see my call history and make calls from the listed items

  Background: I am in the History view
    Given I go to the home screen
    When  I touch the "History" button
    Then  the "History" view is present

  Scenario: I want to see a missed call indicated on the All History view
    Given I receive and ignore a call
    When  [history] I touch the All tab
    Then  [history] I see the call at the top of the All History view
    And   [history] the call has a red handset icon

  Scenario: I want to see an answered call indicated on the All History view
    Given I receive and answer a call
    When  [history] I touch the All tab
    Then  [history] I see the call at the top of the All History view
    And   [history] the call has a blue handset icon

  Scenario: I want to see a missed call indicated on the Missed History view
    Given I receive and ignore a call
    When  [history] I touch the Missed tab
    Then  [history] I see the call at the top of the Missed History view
    And   [history] the call has a red handset icon

  Scenario: I want to see an outgoing call indicated on the All History view
    Given I touch the "Dial" button
    When  [dial] I make a call to a coworker contact
    Then  [active_call] an "Active Call" window appears
    When  [active_call] I end the call
    Then  the in-call window disappears
    Given I go to the home screen
    When  I touch the "History" button
    Then  the "History" view is present
    When  [history] I touch the All tab
    Then  [history] I see the call at the top of the All History view
    And   [history] the call has a green handset icon


  Scenario: I want to call back a missed call indicated on the All History view
    Given I receive and ignore a call
    When  [history] I touch the All tab
    Then  [history] I see the call at the top of the All History view
    And   [history] the call has a red handset icon
    When  [history] I touch the handset icon
    Then  My phone calls back the caller

  Scenario: I want to call back an answered call indicated on the All History view
    Given I receive a call
    Then  the incoming call window appears
    When  I answer the call
    Then  [active_call] an "Active Call" window appears
    When  [active_call] I end the call
    Then  the incoming call window disappears
    When  [history] I touch the All tab
    Then  [history] I see the call at the top of the All History view
    And   [history] the call has a blue handset icon
    When  [history] I touch the handset icon
    Then  My phone calls back the caller

  Scenario: I want to call back a missed call indicated on the Missed History view
    Given I receive and ignore a call
    When  [history] I touch the Missed tab
    Then  [history] I see the call at the top of the Missed History view
    And   [history] the call has a red handset icon
    When  [history] I touch the handset icon
    Then  My phone calls back the caller

  Scenario: I want to call back an outgoing call indicated on the All History view
    Given I touch "Dial"
    Then  [dial] the Dial view appears
    When  [dial] I make a call to a coworker contact
    Then  [active_call] an "Active Call" window appears
    When  [active_call] I end the call
    Then  the in-call window disappears
    Given I go to the home screen
    When  I touch the "History" button
    Then  the "History" view is present
    When  [history] I touch the All tab
    Then  [history] I see the call at the top of the All History view
    And   [history] the call has a green handset icon
    When  [history] I touch the handset icon
    Then  my phone calls back the contacts number
