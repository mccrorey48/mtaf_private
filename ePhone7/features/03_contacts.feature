Feature: As a user I want to use and manage my contact lists

  Background: I am at the Contacts view
    Given [background] I go to the home screen
    Then  [background] I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen
    When  I touch "Contacts"
    Then  [background] I see the Personal, Coworkers, Favorites and Groups tabs

#  Scenario: I want to import my Google contacts
#    Given I touch the "Personal" tab
#    When  I touch the "Sign in with Google" banner
#    Then  [contacts] a Google login screen appears
#    And   [contacts] I enter my Google user id and password
#    Then  [contacts] my Google contacts are shown on the display

  @regression
  Scenario: I want to see my Coworkers list
    Given I touch the "Coworkers" tab
    Then  [contacts] my Coworker contacts are shown on the display

  @regression
  Scenario: I want to call a contact from my Coworkers list
    Given I touch the "Coworkers" tab
    Then  [contacts] my Coworker contacts are each shown with a handset icon
#    And   [contacts] the contact I want to call has a green handset icon
    And   [contacts] the contact I want to call is online
    When  [contacts] I touch the handset icon next to the contact I want to call
    Then  [contacts] my phone calls the contact

  Scenario: I want to see my Favorites list
    Given I touch the "Favorites" tab
    Then  [contacts] my Favorite contacts are shown on the display

  Scenario: I want to call a contact from my Favorites list
    Given I touch the "Favorites" tab
    Then  [contacts] my Favorite contacts are shown on the display
#    And   [contacts] the contact I want to call has a green handset icon
    And   [contacts] the contact I want to call is online
    When  [contacts] I touch the handset icon next to the contact I want to call
    Then  [contacts] my phone calls the contact

  Scenario: I want to add a contact to my Favorites list
    Given I touch the "Coworkers" tab
    Then  [contacts] my Coworker contacts are shown on the display
    When  [contacts] I touch the name of a contact that is not a Favorite
    Then  [contacts] a contact detail screen appears with a white star icon
    When  [contacts] I touch the white star icon
    Then  [contacts] the star turns yellow
    When  I touch the "Favorites" tab
    Then  [contacts] the contact is shown on the display

  Scenario: I want to set the Favorites status of multiple Coworker contacts
    Given I touch the "Coworkers" tab
    Then  [contacts] my Coworker contacts are shown on the display
    When  [contacts] I long-press a contact list item
    Then  [contacts] An "Add Multiple Favorites" confirmation dialog appears
    When  I touch "OK" on the Add Multiple Favorites confirmation dialog
    Then  [contacts] my Coworker contacts are each shown with a Favorites star icon
    And   [contacts] Any existing Favorite contacts have a yellow start icon
    And   [contacts] Any other contacts have a white start icon
    When  [contacts] I touch the Favorites star icon on some contacts
    Then  [contacts] the color toggles between yellow and white
    When  [contacts] I long-press a contact list item
    Then  [contacts] my Coworker contacts are each shown with a handset icon
    When  I touch the "Favorites" tab
    Then  [contacts] my updated Favorite contacts are shown on the display

  Scenario: I want to set the Favorites status of multiple Personal contacts
    Given I touch the "Personal" tab
    Then  [contacts] my Personal contacts are shown on the display
    When  [contacts] I long-press a contact list item
    Then  [contacts] An "Add Multiple Favorites" confirmation dialog appears
    When  I touch "OK" on the Add Multiple Favorites confirmation dialog
    Then  [contacts] my Coworker contacts are each shown with a Favorites star icon
    And   [contacts] Any existing Favorite contacts have a yellow start icon
    And   [contacts] Any other contacts have a white start icon
    When  [contacts] I touch the Favorites star icon on some contacts
    Then  [contacts] the color toggles between yellow and white
    When  [contacts] I long-press a contact list item
    Then  [contacts] my Personal contacts are each listed with a handset icon
    When  I touch the "Favorites" tab
    Then  [contacts] my updated Favorite contacts are shown on the display

  Scenario: I want to remove a contact from my Favorites list
    Given I touch the "Favorites" tab
    And   [contacts] my Favorite contacts are shown on the display
    And   [contacts] I touch the name of a contact
    And   [contacts] a contact detail screen appears with a yellow star icon
    And   [contacts] I touch the yellow star icon
    And   [contacts] the star turns white
    When  [contacts] I close the contact detail screen
    Then  [contacts] the contact is not shown on the display

  Scenario: I want to see my Group lists
    Given I touch the "Groups" tab
    Then  [contacts] my Group Lists are shown on the display

  Scenario: I want to create a personal Group List
    Given I touch the "Groups" tab
    Then  [contacts] my Group Lists are shown on the display
    When  I touch the "Add" button
    Then  [contacts] a Create New Group popup appears
    When  [contacts] I enter a group name
    And   I touch the "Create" button
    Then  [contacts] the personal group list is shown on the display

  Scenario: I want to add a contact to a personal Group List
    Given I touch the "Groups" tab
    Then  [contacts] my Group Lists are shown on the display
    When  [contacts] I touch the name of a personal Group list
    Then  [contacts] the contact list for the group is displayed
    And   [contacts] Add and Delete buttons are visible
    When  I touch the "Add" button
    Then  [contacts] my Coworker contacts are displayed in a list with checkboxes
    When  [contacts] I touch a check a box next to a contact
    Then  [contacts] a check mark appears in the box
    When  I touch the "Done" button
    Then  [contacts] the contact is shown on the contact list for the group
    When  I touch the "Add" button
    Then  [contacts] my Coworker contacts are displayed in a list with checkboxes
    And   [contacts] the previously added contact is not on the list with checkboxes


  Scenario: I want to delete a contact from a Group
    Given I touch the "Groups" tab
    Then  [contacts] my Group Lists are shown on the display
    When  [contacts] I touch the name of a personal Group list
    Then  [contacts] the contact list for the group is displayed
    And   [contacts] Add and Delete buttons are visible
    When  I touch the "Add" button
    Then  [contacts] my Coworker contacts are displayed in a list with checkboxes
    When  [contacts] I touch a check a box next to a contact
    Then  [contacts] a check mark appears in the box
    When  I touch the "Done" button
    Then  [contacts] the contact is shown on the contact list for the group
    When  I touch the "Delete" button
    Then  [contacts] the Group list contacts are displayed in a list with checkboxes
    When  [contacts] I touch a check a box next to a contact
    Then  [contacts] a check mark appears in the box
    When  I touch the "Done" button
    And   [contacts] the contact is not shown on the contact list for the group

  Scenario: I should be unable to edit a system Group
    Given I touch the "Groups" tab
    Then  [contacts] my Group Lists are shown on the display
    When  [contacts] I touch the name of a system Group list
    Then  [contacts] the contact list for the group is displayed
    And   [contacts] Add and Delete buttons are not visible


