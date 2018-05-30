#Feature: voicemail matcher
#
#  Scenario: match new VM elements to vvm microservice metadata
#    Given I send the Home keycode
#    Then  the Home view is present
#    And   the Voicemail view is not present
#    When  I touch the "Voicemail" button
#    Then  the Home view is not present
#    And   the Voicemail view is present
#    When  I touch the "NEW" tab
#    Then  I see my existing new voicemails
