@regression
Feature: As a user I want to see my contact lists (R2D2-2054)

  Background: I am at the Contacts view
    Given I go to the home screen
    Then  [user] I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen
    When  I touch "Contacts"
    Then  [contacts] I see the Personal, Coworkers, Favorites and Groups tabs

  Scenario: I want to see my Coworkers list
    Given I touch the "Coworkers" tab
    Then  [contacts] my Coworker contacts are shown on the display

  Scenario: I want to see favorite Coworker contacts on the Favorites list
    Given I touch the "Coworkers" tab
    Then  [contacts] my Coworker contacts are shown on the display
    When  [contacts] I long-press a contact list item
    Then  [contacts] An "Add Multiple Favorites" confirmation dialog appears
    When  I touch "OK"
    Then  [contacts] my Coworker contacts are each shown with a Favorites star icon
    And   [contacts] I touch the star icons so Favorites are yellow and others are white
    When  [contacts] I long-press a contact list item
    Then  [contacts] my Coworker contacts are each shown with a handset icon
    When  I touch the "Favorites" tab
    Then  [contacts] my Favorite contacts are shown on the display
    When  I touch the "Coworkers" tab
    And   [contacts] I long-press a contact list item
    Then  [contacts] An "Add Multiple Favorites" confirmation dialog appears
    When  I touch "OK"
    Then  [contacts] my Coworker contacts are each shown with a Favorites star icon
    When  [contacts] I touch the star icons so all are white
    And   [contacts] I long-press a contact list item
    Then  [contacts] my Coworker contacts are each shown with a handset icon
    When  I touch the "Favorites" tab
    Then  [contacts] no Coworker contacts are shown on the favorites display

#  Scenario: I want to see my Group lists
#    Given [contacts] I touch the Groups tab
#    Then  [contacts] my Group Lists are shown on the display

