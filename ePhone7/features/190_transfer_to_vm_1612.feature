# @regression @known_bug @wip
Feature: As a user I want to transfer an active call to voicemail (R2D2-1612)

  Scenario: I transfer an incoming call to voicemail
    Given I receive a call
    And   I answer the call
    Then  [active_call] an "Active Call" window appears
    When  [active_call] I tap "Transfer to VM"
    Then  [active_call] the transfer dialog appears
    When  [active_call] I select a coworker's mailbox
    Then  [active_call] I see a green banner with the coworker's name
    And   [active_call] I see an orange banner with the caller's name
    When  [active_call] I touch the "end call" button
    Then  I am at the home screen
    And   [active_call] the caller leaves a message and hangs up
