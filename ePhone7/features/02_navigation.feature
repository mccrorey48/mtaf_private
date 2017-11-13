@regression @wip
Feature: As a user I want to navigate to different views using the touch screen

  Background: I am at the Home view
    Given I go to the home screen

  Scenario: I go to the Contacts view
    Given I touch the "Contacts" button
    Then  the "Contacts" view appears

  Scenario: I go to the History view
    Given I touch the "History" button
    Then  the "History" view appears

  Scenario: I go to the Voicemail view
    Given I touch the "Voicemail" button
    Then  the "Voicemail" view appears

  Scenario: I go to the Dial view
    Given I touch the "Dial" button
    Then  the "Dial" view appears

  Scenario: I go to the Preferences view
    Given [user] I touch the Preferences icon
    Then  the "Preferences" view appears
    When  [prefs] I touch the "X" icon
    Then  the "Preferences" view disappears

