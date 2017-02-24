Feature: As a user I want to navigate to different views using the touch screen

  Background: I am at the Home view
    Given I am logged in to the ePhone7
    Then I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen

  Scenario: I want to go to the Contacts view
    Given I touch the Contacts button
    Then the Contacts view appears
    And I see the Personal, Coworkers, Favorites and Groups tabs

  Scenario: I want to go to the History view
    Given I touch the History button
    Then the History view appears
    And I see the All and Missed tabs at the top of the screen

  Scenario: I want to go to the Voicemail view
    Given I touch the Voicemail button
    Then the Voicemail view appears
    And I see the New, Saved and Trash tabs at the top of the screen

  Scenario: I want to go to the Dial view
    Given I touch the Dial button
    Then the Dial view appears

  Scenario: I want to go to the Preferences view
    Given I touch the Preferences icon
    Then the Preferences window appears

