Feature: As a user I want to be able to see my favorite contacts from the active call screen (R2D2-1649)

  Scenario: the in-call screen Coworkers button shows Coworker contacts
    When  I touch the "Dial" button
    And   [dial] I make a call to a coworker contact
    And   the coworker contact answers the call
    And   [active_call] an "Active Call" window appears
    When  I touch the "Coworkers" button
    Then  [active_call] the in-call contacts screen appears
    And   [active_call] the Coworkers tab is selected
    And   [active_call] my Coworker contacts are listed on the contacts screen
    Then  [active_call] I end the call

  Scenario: the in-call screen Coworkers button shows Favorite contacts
    Given I add my favorite Coworker contacts to my Favorites list
    When  I touch the "Dial" button
    And   [dial] I make a call to a coworker contact
    And   the coworker contact answers the call
    And   [active_call] an "Active Call" window appears
    When  I touch the "Coworkers" button
    Then  [active_call] the in-call contacts screen appears
    And   [active_call] the Coworkers tab is selected
    Then  [active_call] I select the Favorites tab
    And   [active_call] my favorite Coworker contacts are listed
    Then  [active_call] I end the call

