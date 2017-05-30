Feature: As a user I want to to update my phone's software to the latest version

  Scenario: Performing an online upgrade from 2.1.3/1.0.10 to alpha
    Given I am logged in to the ePhone7
    And   I downgrade my aosp to 2.1.3 and app to 1.0.10
    Then  I set the OTA server
    When  [user] I touch the Preferences icon
    Then  [prefs] the Preferences window appears
    When  [prefs] I touch the "System" menu category
    And   [prefs] I touch the "Updates" menu item
    And   [prefs] I touch the "Check for System Update" option
    Then  [prefs] an upgrade is found and an "Upgrade" button appears
    When  [prefs] I touch the "Upgrade" button
    Then  I wait for the phone to upgrade and reboot
    And   I verify the system and app versions are current

  Scenario: Performing an online upgrade from production to alpha
    Given I am logged in to the ePhone7
    And   I downgrade my aosp and app to production version
    Then  I set the OTA server
    When  [user] I touch the Preferences icon
    Then  [prefs] the Preferences window appears
    When  [prefs] I touch the "System" menu category
    And   [prefs] I touch the "Updates" menu item
    And   [prefs] I touch the "Check for System Update" option
    Then  [prefs] an upgrade is found and an "Upgrade" button appears
    When  [prefs] I touch the "Upgrade" button
    Then  I wait for the phone to upgrade and reboot
    And   I verify the system and app versions are current

  Scenario: Performing an online upgrade from 2.3.8/1.3.6 to alpha
    Given I am logged in to the ePhone7
    Then  I downgrade my aosp to 2.3.8 and app to 1.3.6
    Then  I set the OTA server
    When  [user] I touch the Preferences icon
    Then  [prefs] the Preferences window appears
    When  [prefs] I touch the "System" menu category
    And   [prefs] I touch the "Updates" menu item
    Then  I wait for the phone to upgrade and reboot
    And   I verify the system and app versions are current

  Scenario: Downgrade AOSP to 2.3.8/1.3.6
    Given I am logged in to the ePhone7
    Then  I downgrade my aosp to 2.3.8 and app to 1.3.6

  @downgrade
  Scenario: Downgrade AOSP to 2.1.3/1.0.10
    Given I am logged in to the ePhone7
    Then  I downgrade my aosp to 2.1.3 and app to 1.0.10

