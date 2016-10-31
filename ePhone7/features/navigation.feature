Feature: The user can navigate to different views by touching tabs on the screen

  Background: Navigating screen views when logged in
    Given I log in if necessary
    And I am at the Home screen
    Then I see the Contacts, History, Voicemail and Dial tabs


  Scenario: Go to the Contacts view
    Given I am on the home screen
    And I touch the Contacts tab
    Then the Contacts view appears
    And I see the Personal, Coworkers, Favorites and Groups tabs

  Scenario: Go to the History view

