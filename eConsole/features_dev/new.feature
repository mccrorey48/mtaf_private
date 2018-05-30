Feature: element finder functions

  @select
  Scenario: element not present (select)
    Given I send the Home keycode
    Then  the Home view is present

  @select @wip
  Scenario: element not present (premier)
    Given I send the Home keycode
    Then  the Home view is present
#    And   the Contacts view is not present
#    When  I touch the "Contacts" button
#    When  I touch "Contacts" button
#    Then  the Home view is not present
#    And   the Contacts view is present
