Feature: As a user I want to make calls by directly entering all or part of a contact's name or number

  Background: I am in the Dial view
    Given I go to the home screen
    Then  [user] I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen
    When  I touch the "Dial" button
    Then  [dial] I see the keypad

  Scenario: I want to call a Coworker contact by entering the number
    Given [dial] I enter a Coworker contact number using the keypad
    When  [dial] I touch the Call button
    Then  My phone calls the number

  Scenario: I want to call an external number by entering the number
    Given [dial] I enter a 10-digit phone number using the keypad
    When  [dial] I touch the Call button
    Then  My phone calls the number

  Scenario: I want to find a Coworker contact using a partial number search and call it
    Given [dial] I enter part of a Coworker contact number using the keypad
    Then  [dial] A list of contacts containing the partial number appears above the keypad
    When  [dial] I touch the contact listing I want to call
    Then  [dial] Only the contact I touched is listed
    When  [dial] I touch the Call button
    Then  My phone calls the number

  Scenario: I want to find a Personal contact using a partial number search and call it
    Given I enter part of a Personal contact number using the keypad
    Then  [dial] A list of contacts containing the partial number appears above the keypad
    When  [dial] I touch the contact listing I want to call
    Then  [dial] Only the contact I touched is listed
    When  [dial] I touch the Call button
    Then  My phone calls the number

  Scenario: I want to find a Coworker contact using a partial name search and call it
    Given I enter part of a Coworker contact name using the keypad
    Then  [dial] A list of Coworker contacts containing the partial name appears above the keypad
    When  [dial] I touch the contact listing I want to call
    Then  [dial] Only the contact I touched is listed
    When  [dial] I touch the Call button
    Then  My phone calls the number

  Scenario: I want to find a Personal contact using a partial name search and call it
    Given I enter part of a Personal contact name using the keypad
    Then  [dial] A list of Personal contacts containing the partial name appears above the keypad
    When  [dial] I touch the contact listing I want to call
    Then  [dial] Only the contact I touched is listed
    When  [dial] I touch the Call button
    Then  My phone calls the number

