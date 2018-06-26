@regression
Feature: As a user I want to use and manage my contact lists

  Background: I am at the Contacts view and no Favorites are set
    Given I go to the home screen
    Given I touch the "Contacts" button
    Then  the "Contacts" view is present
    When  [contacts] I touch the Coworkers tab
    Then  [contacts] my Coworker contacts are shown on the display
    When  [contacts] I long-press a contact list item
    Then  [contacts] An "Add Multiple Favorites" confirmation dialog appears
    When  I touch "OK"
    Then  [contacts] my Coworker contacts are each shown with a Favorites star icon
    And   [contacts] I touch the star icons so all are white
    When  [contacts] I long-press a contact list item
    Then  [contacts] my Coworker contacts are each shown with a handset icon

  Scenario: I want to call a contact from my Coworkers list
    Given [contacts] I touch the Coworkers tab
    Then  [contacts] my Coworker contacts are each shown with a handset icon
    And   [contacts] the contact I want to call is online
    When  [contacts] I touch the handset icon next to the contact I want to call
    Then  [contacts] my phone calls the contact

  Scenario: I want to add a Coworker contact to my Favorites list
    Given [contacts] I touch the Coworkers tab
    Then  [contacts] my Coworker contacts are shown on the display
    When  [contacts] I touch the name of a Coworker contact that is not a Favorite
    Then  [contacts] a contact detail screen appears with a white star icon
    When  [contacts] I touch the star icon
    Then  [contacts] the star turns yellow
    When  [contacts] I touch the Favorites tab
    Then  [contacts] the new favorite contact is shown on the display

    Scenario: I want to set the Favorites status of multiple Coworker contacts
    Given [contacts] I touch the Coworkers tab
    Then  [contacts] my Coworker contacts are shown on the display
    When  [contacts] I long-press a contact list item
    Then  [contacts] An "Add Multiple Favorites" confirmation dialog appears
    When  I touch "OK"
    Then  [contacts] my Coworker contacts are each shown with a Favorites star icon
    And   [contacts] I touch the star icons so Favorites are yellow and others are white
    When  [contacts] I long-press a contact list item
    Then  [contacts] my Coworker contacts are each shown with a handset icon
    When  [contacts] I touch the Favorites tab
    Then  [contacts] my Favorite contacts are shown on the display
    When  [contacts] I touch the Coworkers tab
    And   [contacts] I long-press a contact list item
    Then  [contacts] An "Add Multiple Favorites" confirmation dialog appears
    When  I touch "OK"
    Then  [contacts] my Coworker contacts are each shown with a Favorites star icon
    When  [contacts] I touch the star icons so all are white
    And   [contacts] I long-press a contact list item
    Then  [contacts] my Coworker contacts are each shown with a handset icon
    When  [contacts] I touch the Favorites tab
    Then  [contacts] no Coworker contacts are shown on the favorites display

#  Scenario: I want to set the Favorites status of multiple Personal contacts
#    Given I touch the "Personal" tab
#    Then  [contacts] my Personal contacts are shown on the display
#    When  [contacts] I long-press a contact list item
#    Then  [contacts] An "Add Multiple Favorites" confirmation dialog appears
#    When  I touch "OK"
#    Then  [contacts] my Personal contacts are each shown with a Favorites star icon
#    And   [contacts] I touch the star icons so Favorites are yellow and others are white
#    When  [contacts] I long-press a contact list item
#    Then  [contacts] my Personal contacts are each shown with a handset icon
#    When  I touch the "Favorites" tab
#    Then  [contacts] my Favorites contacts are shown on the display
#    When  I touch the "Personal" tab
#    And   [contacts] I long-press a contact list item
#    Then  [contacts] An "Add Multiple Favorites" confirmation dialog appears
#    When  I touch "OK"
#    Then  [contacts] my Personal contacts are each shown with a Favorites star icon
#    When  [contacts] I touch the star icons so all are white
#    And   [contacts] I long-press a contact list item
#    Then  [contacts] my Personal contacts are each shown with a handset icon
#    When  I touch the "Favorites" tab
#    Then  [contacts] no Personal contacts are shown on the favorites display

#  Scenario: I want to remove a contact from my Favorites list
#    Given I touch the "Favorites" tab
#    And   [contacts] my Favorite contacts are shown on the display
#    And   [contacts] I touch the name of a contact
#    And   [contacts] a contact detail screen appears with a yellow star icon
#    And   [contacts] I touch the yellow star icon
#    And   [contacts] the star turns white
#    When  [contacts] I close the contact detail screen
#    Then  [contacts] the contact is not shown on the display
#
#  Scenario: I want to see my Group lists
#    Given I touch the "Groups" tab
#    Then  [contacts] my Group Lists are shown on the display
#
#  Scenario: I want to create a personal Group List
#    Given I touch the "Groups" tab
#    Then  [contacts] my Group Lists are shown on the display
#    When  I touch the "Add" button
#    Then  [contacts] a Create New Group popup appears
#    When  [contacts] I enter a group name
#    And   I touch the "Create" button
#    Then  [contacts] the personal group list is shown on the display
#
#  Scenario: I want to add a contact to a personal Group List
#    Given I touch the "Groups" tab
#    Then  [contacts] my Group Lists are shown on the display
#    When  [contacts] I touch the name of a personal Group list
#    Then  [contacts] the contact list for the group is displayed
#    And   [contacts] Add and Delete buttons are visible
#    When  I touch the "Add" button
#    Then  [contacts] my Coworker contacts are displayed in a list with checkboxes
#    When  [contacts] I touch a check a box next to a contact
#    Then  [contacts] a check mark appears in the box
#    When  I touch the "Done" button
#    Then  [contacts] the contact is shown on the contact list for the group
#    When  I touch the "Add" button
#    Then  [contacts] my Coworker contacts are displayed in a list with checkboxes
#    And   [contacts] the previously added contact is not on the list with checkboxes
#
#
#  Scenario: I want to delete a contact from a Group
#    Given I touch the "Groups" tab
#    Then  [contacts] my Group Lists are shown on the display
#    When  [contacts] I touch the name of a personal Group list
#    Then  [contacts] the contact list for the group is displayed
#    And   [contacts] Add and Delete buttons are visible
#    When  I touch the "Add" button
#    Then  [contacts] my Coworker contacts are displayed in a list with checkboxes
#    When  [contacts] I touch a check a box next to a contact
#    Then  [contacts] a check mark appears in the box
#    When  I touch the "Done" button
#    Then  [contacts] the contact is shown on the contact list for the group
#    When  I touch the "Delete" button
#    Then  [contacts] the Group list contacts are displayed in a list with checkboxes
#    When  [contacts] I touch a check a box next to a contact
#    Then  [contacts] a check mark appears in the box
#    When  I touch the "Done" button
#    And   [contacts] the contact is not shown on the contact list for the group
#
#  Scenario: I should be unable to edit a system Group
#    Given I touch the "Groups" tab
#    Then  [contacts] my Group Lists are shown on the display
#    When  [contacts] I touch the name of a system Group list
#    Then  [contacts] the contact list for the group is displayed
#    And   [contacts] Add and Delete buttons are not visible
#

