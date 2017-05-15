@regression
Feature: As a user I want to navigate to different views using the touch screen

  Background: I am at the Home view
    Given I am logged in to the ePhone7
    Then  [user] I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen

  Scenario: I go to the Contacts view
    Given [user] I touch the "Contacts" button
    Then  [contacts] the Contacts view appears
    And   [contacts] I see the Personal, Coworkers, Favorites and Groups tabs

  Scenario: I go to the History view
    Given [user] I touch the History button
    Then  [history] the History view appears
    And   [history] I see the All and Missed tabs at the top of the screen

  Scenario: I go to the Voicemail view
    Given [user] I touch the Voicemail button
    Then  [voicemail] I see the New, Saved and Trash tabs at the top of the screen

  Scenario: I go to the Dial view
    Given [user] I touch the Dial button
    Then  [dial] the Dial view appears

  Scenario: I go to the Preferences view
    Given [user] I touch the Preferences icon
    Then  [prefs] the Preferences window appears

