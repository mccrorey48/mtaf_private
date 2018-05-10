@regression
Feature: As a user I want the current audio path indicated on the in-call screen (R2D2-2142)

  Background: the wired headset is enabled in Preferences
    Given I go to the home screen
    When  [user] I touch the Preferences icon
    Then  [prefs] the Preferences window appears
    When  I touch the "Phone" category
    And   [prefs] I swipe the Wired Headset switch to the right
    And   [prefs] I touch the "X" icon
    Then  [prefs] the Preferences window disappears

  Scenario: the in-call screen audio icon is correct when using the speaker
    When  [user] I touch the Headset icon if it is green
    Then  [user] the Headset icon is blue
    When  I touch the "Dial" button
    And   [dial] I make a call to a coworker contact
    And   the coworker contact answers the call
    Then  [active_call] the speaker icon is displayed
    And   [active_call] I end the call

  Scenario: the in-call screen audio icon is correct when using the wired headset
    When  [user] I touch the Headset icon if it is blue
    Then  [user] the Headset icon is green
    When  I touch the "Dial" button
    And   [dial] I make a call to a coworker contact
    And   the coworker contact answers the call
    Then  [active_call] the headset icon is displayed
    And   [active_call] I end the call

