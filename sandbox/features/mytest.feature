Feature: test feature

#  @scenario_tag @foo
#  Scenario: a scenario
#    Given I run a step with no substeps
##    And   I run a step with a failing substep
##    And   I run a step with a fake substep
##    And   I run a step with fake and passing substeps
##    And I run a step with failing then passing substeps
#    Then this happens

  Scenario: another scenario
#    Given I run a step with no substeps
#    Given   I run a step with a passing substep
#    And   I run a step with a fake substep
    Given I run a step with substeps that have substeps
#    Then this happens

