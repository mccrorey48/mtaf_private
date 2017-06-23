Feature: As a user I want to transfer an active call to voicemail (R2D2-1612)

  Scenario: I transfer an incoming call to voicemail
    Given I receive a call
    And   I answer the call
    When  [active_call] I tap "Transfer to VM"
    Then  [active_call] the transfer dialpad appears
    When  [active_call] I select a coworker's mailbox
    Then  [active_call] I touch "OK" to complete the voicemail transfer
