@wip
Feature: As a user I want the current audio path indicated on the in-call screen (R2D2-2143)

  Scenario: the in-call screen audio icon is correct when using the speaker
    Given I go to the home screen
    When  [user] I touch the Preferences icon
    Then  [prefs] the Preferences window appears
    When  I touch the "Phone" category
    And   [prefs] I swipe the Wired Headset switch to the left
    Then  [prefs] I touch the "X" icon
    Then  I touch the "Dial" button
    When  [dial] I make a call to a coworker contact
    And   the coworker contact answers the call
    And   [active_call] the speaker icon is displayed
    Then  [active_call] I end the call

  Scenario: the in-call screen audio icon is correct when using the wired headset
    Given I go to the home screen
    When  [user] I touch the Preferences icon
    Then  [prefs] the Preferences window appears
    When  I touch the "Phone" category
    And   [prefs] I swipe the Wired Headset switch to the right
    Then  [prefs] I touch the "X" icon
    Then  I touch the "Dial" button
    When  [dial] I make a call to a coworker contact
    And   the coworker contact answers the call
    And   [active_call] the headset icon is displayed
    Then  [active_call] I end the call

