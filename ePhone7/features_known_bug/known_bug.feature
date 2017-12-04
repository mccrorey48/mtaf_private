Feature: fail a scenario that is a known bug

  Scenario: this one will pass
    Given I don't do anything
    Then  nothing fails

  @known_bug
  Scenario: this one will fail
    Given I fail a step
    Then  this happens

  Scenario: this one will fail
    Given I fail a step
    Then  this happens
