Feature: As a user I want to use and manage my contact lists

  Background: I am at the Contacts view
    Given I am logged in to the ePhone7
    Then I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen
    When I touch the "Contacts" button
    Then the Contacts view appears
    And I see the Personal, Coworkers, Favorites and Groups tabs

  Scenario: I want to import my Google contacts
    Given I go to the Personal tab
    When I touch the "Sign in with Google" banner
    Then A Google login screen appears
    And I enter my Google user id and password
    Then My Google contacts are shown on the display

  Scenario: I want to see my Coworkers list
    Given I touch the Coworkers tab
    Then My Coworker contacts are shown on the display

  Scenario: I want to call a contact from my Coworkers list
    Given I touch the Coworkers tab
    Then My Coworker contacts are each listed with a handset icon
    When I touch the handset icon on a contact list item
    Then My phone calls the contact

  Scenario: I want to see my Favorites list
    Given I touch the Favorites tab
    Then My Favorite contacts are shown on the display

  Scenario: I want to call a contact from my Favorites list
    Given I touch the Favorites tab
    Then My Favorite contacts are shown on the display
    When I touch the handset icon on a contact list item
    Then My phone calls the contact

  Scenario: I want to add a contact to my Favorites list
    Given I touch the Coworkers tab
    Then My Coworker contacts are shown on the display
    When I touch the name of a contact that is not a Favorite
    Then A contact detail screen appears with a white star icon
    When I touch the white star icon
    Then The star turns yellow
    When I touch the Favorites tab
    Then The contact is shown on the display

  Scenario: I want to set the Favorites status of multiple Coworker contacts
    Given I touch the Coworkers tab
    Then My Coworker contacts are shown on the display
    When I long-press a contact list item
    Then An "Add Multiple Favorites" confirmation dialog appears
    When I touch "OK"
    Then The contacts are shown with a Favorites star icon next to each one
    And Any existing Favorite contacts have a yellow start icon
    And Any other contacts have a white start icon
    When I touch the Favorites star icon on some contacts
    Then The color toggles between yellow and white
    When I long-press a contact list item
    Then My Coworker contacts are each listed with a handset icon
    When I touch the Favorites tab
    Then My updated Favorite contacts are shown on the display

  Scenario: I want to set the Favorites status of multiple Personal contacts
    Given I touch the "Personal" tab
    Then My Personal contacts are shown on the display
    When I long-press a contact list item
    Then An "Add Multiple Favorites" confirmation dialog appears
    When I touch "OK"
    Then The contacts are shown with a Favorites star icon next to each one
    And Any existing Favorite contacts have a yellow start icon
    And Any other contacts have a white start icon
    When I touch the Favorites star icon on some contacts
    Then The color toggles between yellow and white
    When I long-press a contact list item
    Then My Personal contacts are each listed with a handset icon
    When I touch the Favorites tab
    Then My updated Favorite contacts are shown on the display

  Scenario: I want to remove a contact from my Favorites list
    Given I touch the Favorites tab
    And My Favorite contacts are shown on the display
    And I touch the name of a contact
    And A contact detail screen appears with a yellow star icon
    And I touch the yellow star icon
    And The star turns white
    When I close the contact detail screen
    Then The contact is not shown on the display

  Scenario: I want to see my Group lists
    Given I touch the Groups tab
    Then My Group Lists are shown on the display

  Scenario: I want to create a personal Group List
    Given I touch the Groups tab
    Then My Group Lists are shown on the display
    When I touch the Add button
    Then A Create New Group popup appears
    When I enter a group name
    And I touch the Create button
    Then The personal group list is shown on the display

  Scenario: I want to add a contact to a personal Group List
    Given I touch the Groups tab
    Then My Group Lists are shown on the display
    When I touch the name of a personal Group list
    Then The contact list for the group is displayed
    And Add and Delete buttons are visible
    When I touch the Add button
    Then My Coworker contacts are displayed in a list with checkboxes
    When I touch a check a box next to a contact
    Then A check mark appears in the box
    When I touch the Done button
    Then The contact is shown on the contact list for the group
    When I touch the Add button
    Then My Coworker contacts are displayed in a list with checkboxes
    And The previously added contact is not on the list with checkboxes


  Scenario: I want to delete a contact from a Group
    Given I touch the Groups tab
    Then My Group Lists are shown on the display
    When I touch the name of a personal Group list
    Then The contact list for the group is displayed
    And Add and Delete buttons are visible
    When I touch the Add button
    Then My Coworker contacts are displayed in a list with checkboxes
    When I touch a check a box next to a contact
    Then A check mark appears in the box
    When I touch the Done button
    Then The contact is shown on the contact list for the group
    When I touch the Delete button
    Then The Group list contacts are displayed in a list with checkboxes
    When I touch a check a box next to a contact
    Then A check mark appears in the box
    When I touch the Done button
    And The contact is not shown on the contact list for the group

  Scenario: I should be unable to edit a system Group
    Given I touch the Groups tab
    Then My Group Lists are shown on the display
    When I touch the name of a system Group list
    Then The contact list for the group is displayed
    And Add and Delete buttons are not visible


