Feature: As a user I want to have a Record button available during an active call (R2D2-1954)

  @wip
  Scenario: I want to record an incoming call
    Given I am logged in to the ePhone7
    And I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen
    When I touch the Dial button
    Then The Dial view appears
    When I dial the Advanced Settings direct code
    And I touch the call button
    Then the Advanced Options view appears
    When I scroll down to the Call Record Enable setting
    And I check the Call Record Enable checkbox
    And I scroll to the top of the Advanced Options view
    And I swipe down twice
    Then the Advanced Options view disappears
    When I receive a call
    And I answer the call
    Then an "Active Call Screen" window appears
    And a Record button is visible
    And the Record button is white

#  @wip
  Scenario: I want to record an outgoing call
    Given I am logged in to the ePhone7
    And I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen
    When I touch the Dial button
    Then The Dial view appears
    When I dial the Advanced Settings direct code
    And I touch the call button
    Then the Advanced Options view appears
    When I scroll down to the Call Record Enable setting
    And I check the Call Record Enable checkbox
    And I scroll to the top of the Advanced Options view
    And I swipe down twice
    Then the Advanced Options view disappears
    When I make a call to a coworker contact
    Then an "Active Call Screen" window appears
    And a Record button is visible
    And the Record button is white

#  @wip
  Scenario: I want to disable recording for an incoming call
    Given I am logged in to the ePhone7
    And I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen
    When I touch the Dial button
    Then The Dial view appears
    When I dial the Advanced Settings direct code
    And I touch the call button
    Then the Advanced Options view appears
    When I scroll down to the Call Record Enable setting
    And I uncheck the Call Record Enable checkbox
    And I scroll to the top of the Advanced Options view
    And I swipe down twice
    Then the Advanced Options view disappears
    When I receive a call
    And I answer the call
    Then an "Active Call Screen" window appears
    And a Record button is visible
    And the Record button is gray

#  @wip
  Scenario: I want to disable recording for an outgoing call
    Given I am logged in to the ePhone7
    And I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen
    When I touch the Dial button
    Then The Dial view appears
    When I dial the Advanced Settings direct code
    And I touch the call button
    Then the Advanced Options view appears
    When I scroll down to the Call Record Enable setting
    And I uncheck the Call Record Enable checkbox
    And I scroll to the top of the Advanced Options view
    And I swipe down twice
    Then the Advanced Options view disappears
    When I make a call to a coworker contact
    Then an "Active Call Screen" window appears
    And a Record button is visible
    And the Record button is gray
