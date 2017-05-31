Feature: As a user I want to see my contact lists (R2D2-2054)

  Background: I am at the Contacts view
    Given I am logged in to the ePhone7
    Then  [user] I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen
    When  [user] I touch the "Contacts" button and the Contacts view appears
    Then  [contacts] I see the Personal, Coworkers, Favorites and Groups tabs

  @regression
  Scenario: I want to see my Coworkers list
    Given [contacts] I touch the Coworkers tab
    Then  [contacts] my Coworker contacts are shown on the display

  Scenario: I want to see favorite Coworker contacts on the Favorites list
    Given [contacts] I touch the Coworkers tab
    Then  [contacts] my Coworker contacts are shown on the display
    When  [contacts] I long-press a contact list item
    Then  [contacts] An "Add Multiple Favorites" confirmation dialog appears
    When  [contacts] I touch "OK"
    Then  [contacts] the contacts are shown with a Favorites star icon next to each one
    When  [contacts] I touch the star icons so Favorites are yellow and others are white
    When  [contacts] I long-press a contact list item
    Then  [contacts] my Coworker contacts are each listed with a handset icon
    When  [contacts] I touch the Favorites tab
    Then  [contacts] my Favorite contacts are shown on the display

  Scenario: I want to see my Group lists
    Given [contacts] I touch the Groups tab
    Then  [contacts] my Group Lists are shown on the display

