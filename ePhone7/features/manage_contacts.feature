Feature: Manage contacts

  Scenario: Import Google contacts
    Given I go to the Contacts view
    And I go to the Personal tab
    When I touch the "Sign in with Google" banner
    Then A Google login screen appears
    And I enter my Google user id and password
    Then My Google contacts appear on the Personal contacts list