Feature: As a user I want to navigate to different views using the touch screen

  Background: I start by logging in to the ePhone7 and going to the Home screen
    Given I am logged in to the ePhone7
    And I go to the Home screen
    Then I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen


  Scenario: I want to go to the Contacts view
    Given I touch the Contacts button
    Then the Contacts view appears
    And I see the Personal, Coworkers, Favorites and Groups tabs at the top of the screen

  Scenario: I want to go to the History view
    Given I touch the History button
    Then the Contacts view appears
    And I see the All and New tabs at the top of the screen

  Scenario: I want to go to the Voicemail view
    Given I touch the History button
    Then the Voicemail view appears
    And I see the New, Saved and Trash tabs at the top of the screen

  Scenario: I want to go to the Dial view
    Given I touch the Dial button
    Then the Dial view appears

  Scenario: I want to go to the Preferences view
    Given I touch the Preferences button
    Then the Preferences view appears

