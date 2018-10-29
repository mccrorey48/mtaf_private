@foo
Feature: test feature

#  @known_bug
  Scenario: a scenario
    Given I run a step with no substeps
    And   I run a step with a passing substep
#    And   I run a step with a fake substep
#    And   I run a step with fake and passing substeps
#    Given I run a step with substeps that have substeps
##    And I run a step with failing then passing substeps
    Then this happens

#  @bar
#  Scenario: failing scenario
#    Given I run a step with a failing substep
#    Given   I run a step with a passing substep
#    And   I run a step with a fake substep
#    Given I run a step with substeps that have substeps
#    Then this happens
#
#  @bar
#  Scenario: another scenario
#    Given I run a step with no substeps
#    Given   I run a step with a passing substep
#    And   I run a step with a fake substep
#    Given I run a step with substeps that have substeps
#    Then this happens

