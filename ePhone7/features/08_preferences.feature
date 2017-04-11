Feature: As a user I want to view and change detailed settings that control my phone's operation

  Background: I am logged in and at the Preferences view
    Given [background] I am logged in to the ePhone7
    Then [background] I close all open submenus
    And [background] I see the Need Help, Personal, Phone and System category elements

  Scenario: I want to get instructions for using my phone
    When I touch "Need Help"
    Then A submenu opens with an eHelp option
    When I touch "eHelp"
    Then A popup informs me that help email has been sent to my email address
    When I touch "OK"
    Then The popup disappears

  Scenario: I want to see a walkthrough of my phone's features
    When I touch "Need Help"
    Then A submenu opens with a "Walkthrough" option
    When I touch "Walkthrough"
    Then A "Welcome to ePhone7!" window appears
    When I swipe the screen from right to left
    Then A "Contact Management" window appears
    When I swipe the screen from right to left
    Then A "Call History" window appears
    When I swipe the screen from right to left
    Then A "Visual Voicemail" window appears
    When I swipe the screen from right to left
    Then A "Voicemail Playback" window appears
    When I swipe the screen from right to left
    Then A "Dialpad Screen" window appears
    When I swipe the screen from right to left
    Then an "Active Call Screen" window appears
    When I swipe the screen from right to left
    Then an "Active Call Dialpad" window appears
    When I swipe the screen from right to left
    Then the Preferences window appears

  Scenario: I want to sign in to gmail and download my Personal contacts
    Given I am not signed in to my gmail account
    And My account does not have two-step verification enabled
    When I touch "Personal"
    Then A submenu appears with a "Sign in with Google" option
    When I touch "Sign in with Google"
    Then A Google dialog appears with a place to enter my email address
    When I enter my email address
    And I touch "Next"
    Then A Google dialog appears with a place to enter my password
    When I enter my password
    And I touch "Next"
    Then The Google dialog disappears
    And The "Sign in with Google" element label changes to "Manage Accounts"
    When I touch the "X" icon
    Then The Preferences window disappears
    When I touch the "Contacts" button
    Then the Contacts view appears
    And I see the Personal, Coworkers, Favorites and Groups tabs
    When I touch the "Personal" tab
    Then I can see my personal contacts


  Scenario: I want to sign out of gmail and remove my Personal contacts
    Given I am signed in to my gmail account
    When I touch "Personal"
    Then A submenu appears with a "Manage Accounts" option
    When I touch "Manage Accounts"
    Then A "Sign Out of Google Account" dialog appears
    When I touch the Delete icon
    Then A confirmation dialog appears
    When I touch "OK"
    Then An "Account Deleted" popup appears
    When I touch "OK"
    Then The "Account Deleted" popup disappears
    And The "Manage Accounts" element label changes to "Sign in with Google"

  Scenario: I want to change my default Contacts tab
    When I touch "Personal"
    Then A submenu appears with a "Default Contacts Tab" option
    When I touch "Default Contacts Tab"
    Then A window appears with a button for each Contacts tab
    And The current default tab is selected
    When I touch the button for another tab
    And I touch "OK"
    Then The Contacts tab window disappears
    When I close the Preferences window
    And I touch the "Contacts" button
    Then The new default tab is selected

  Scenario: I want to forward incoming calls when I do not answer
    When I touch "Personal"
    Then A submenu appears with a "Call Forwarding Options" option
    When I touch "Call Forwarding Options"
    Then A window appears with a section labeled "Call Forward No Answer"
    And The section labeled "Call Forward No Answer" is not highlighted
    When I touch the "Call Forward No Answer" section
    Then A window appears with a list of contacts
    And I touch a contact element
    Then Only the contact I touched is listed
    When I touch "OK"
    Then Both windows disappear
    When I touch "Call Forwarding"
    Then A window appears with a section labeled "Call Forward No Answer"
    And The section labeled "Call Forward No Answer" is highlighted

  Scenario: I want to stop forwarding incoming calls when I do not answer
    When I touch "Personal"
    Then A submenu appears with a "Call Forwarding Options" option
    When I touch "Call Forwarding Options"
    Then A window appears with a section labeled "Call Forward No Answer"
    And The section labeled "Call Forward No Answer" is highlighted
    When I touch the "Call Forward No Answer" section
    And The section labeled "Call Forward No Answer" is not highlighted
    When I touch the "Cancel" button
    Then The window disappears

  Scenario: I want to forward incoming calls when my phone is busy
    When I touch "Personal"
    Then A submenu appears with a "Call Forwarding Options" option
    When I touch "Call Forwarding Options"
    Then A window appears with a section labeled "Call Forward Busy"
    When I touch the "Call Forward Busy" section
    Then A window appears with a list of contacts
    And I touch a contact element
    Then Only the contact I touched is listed
    When I touch "OK"
    Then Both windows disappear
    When I touch "Call Forwarding"
    Then A window appears with a section labeled "Call Forward Busy"
    And The section labeled "Call Forward No Answer" is highlighted

  Scenario: I want to stop forwarding incoming calls when my phone is busy
    When I touch "Personal"
    Then A submenu appears with a "Call Forwarding Options" option
    When I touch "Call Forwarding Options"
    Then A window appears with a section labeled "Call Forward Busy"
    And The section labeled "Call Forward Busy" is highlighted
    When I touch the "Call Forward Busy" section
    And The section labeled "Call Forward Busy" is not highlighted
    When I touch the "Cancel" button
    Then The window disappears

  Scenario: I want to change the brightness of my phone's display
    When I touch "Phone"
    Then A submenu appears with a "Brightness" option
    When I touch "Brightness"
    Then A window appears with the label "Screen Brightness" appears
    And The window contains a slider control
    When I touch and drag the slider control handle
    Then The position of the slider control changes
    When I touch "OK"
    Then The window disappears

  Scenario: I want to set the time my screen stays bright when idle
    When I touch "Phone"
    Then A submenu appears with a "Screen Timeout" option
    When I touch "Screen Timeout"
    Then A "Sleep Timer Setting" window appears with buttons for various timer settings
    And The current timer setting is selected
    When I touch the button for another timer setting
    Then The new timer setting is selected
    When I touch "OK"
    Then The "Sleep Timer Setting" window disappears

  Scenario: I want to change my phone's ringtone
    When I touch "Phone"
    Then A submenu appears with a "Ringtones" option
    When I touch "Ringtones"
    Then A "Select Ringtone" window appears with options for various ringtones
    And Only the current ringtone has a dot next to it
    When I touch the button for another ringtone
    Then Only the new ringtone has a dot next to it
    When I touch "OK"
    Then The "Ringtones" window disappears

  Scenario: I want to turn on my phone's touch sounds
    When I touch "Phone"
    Then A submenu appears with a "Volume Control" option
    When I touch "Volume Control"
    Then A window with a "Touch Sounds" toggle appears
    And The toggle handle is in the "Off" position
    When I touch and drag the toggle handle to the "On" position
    Then The toggle handle stays in the "On" position
    When I touch "OK"
    Then The window disappears

  Scenario: I want to turn off my phone's touch sounds
    When I touch "Phone"
    Then A submenu appears with a "Volume Control" option
    When I touch "Volume Control"
    Then A window with a "Touch Sounds" toggle appears
    And The toggle handle is in the "On" position
    When I touch and drag the toggle handle to the "Off" position
    Then The toggle handle stays in the "Off" position
    When I touch "OK"
    Then The window disappears

  Scenario: I want to adjust my phone's ring volume setting
    When I touch "Phone"
    Then A submenu appears with a "Volume Control" option
    When I touch "Volume Control"
    Then A window with a "Ringer Volume" slider appears
    When I touch and drag the slider control handle
    Then The position of the slider control changes
    When I touch "OK"
    Then The window disappears

  Scenario: I want to adjust my phone's voice volume setting
    When I touch "Phone"
    Then A submenu appears with a "Volume Control" option
    When I touch "Volume Control"
    Then A window with a "Voice Call" slider appears
    When I touch and drag the slider control handle
    Then The position of the slider control changes
    When I touch "OK"
    Then The window disappears

  Scenario: I want to adjust my phone's media volume setting
    When I touch "Phone"
    Then A submenu appears with a "Volume Control" option
    When I touch "Volume Control"
    Then A window with a "Media Volume" slider appears
    When I touch and drag the slider control handle
    Then The position of the slider control changes
    When I touch "OK"
    Then The window disappears

  Scenario: I want my phone to immediately answer incoming calls
    When I touch "Phone"
    Then A submenu appears with an "Auto-Answer Calls" toggle
    And The toggle handle is in the "Off" position
    When I touch and drag the toggle handle to the "On" position
    Then The toggle handle stays in the "On" position

  Scenario: I want my phone to stop immediately answering incoming calls
    When I touch "Phone"
    Then A submenu appears with an "Auto-Answer Calls" toggle
    And The toggle handle is in the "On" position
    When I touch and drag the toggle handle to the "Off" position
    Then The toggle handle stays in the "Off" position

  Scenario: I want to change to the 24-hour date format
    When I touch "Phone"
    Then A submenu appears with a "Date/Time Options" option
    When I touch "Date/Time Options"
    Then A window with a "24-hour Format" toggle appears
    And The toggle handle is in the "Off" position
    When I touch and drag the toggle handle to the "On" position
    Then The toggle handle stays in the "On" position
    When I touch the "OK" button
    Then The window disappears

  Scenario: I want to change to the 12-hour date format
    When I touch "Phone"
    Then A submenu appears with a "Date/Time Options" option
    When I touch "Date/Time Options"
    Then A window with a "24-hour Format" toggle appears
    And The toggle handle is in the "On" position
    When I touch and drag the toggle handle to the "Off" position
    Then The toggle handle stays in the "Off" position
    When I touch "OK"
    Then The window disappears

  Scenario: I want to change the time zone
    When I touch "Phone"
    Then A submenu appears with a "Date/Time Options" option
    When I touch "Date/Time Options"
    Then A window with a "Change Timezone" option appears
    And The current time zone text is shown
    When I touch the current time zone text
    Then A menu appears with time zone choices
    When I touch a new time zone choice
    Then The menu disappears
    And The new time zone text is shown
    When I touch "OK"
    Then The window disappears

  Scenario: I want to log out of my phone
    When I touch "System"
    Then A submenu appears with a "Utilities" option
    When I touch the "Utilities" option
    Then A menu with a "Clear App Data/Cache" option appears
    When I touch "Clear App Data/Cache"
    Then A "Clear All User Data" confirmation dialog appears
    When I touch "Confirm"
    Then The login screen appears

  Scenario: I want to reset my phone to the factory settings
    When I touch "System"
    Then A submenu appears with a "Utilities" option
    When I touch the "Utilities" option
    Then A menu with a "Factory Reset" option appears
    When I touch "Factory Reset"
    Then A "Factory Reset" confirmation dialog appears
    When I touch "Confirm"
    Then The login screen appears

  Scenario: I want to see my phone's network settings
    When I touch "System"
    Then A submenu appears with a "Network" option
    When I touch the "Network" option
    Then A window appears with a "Check Ethernet" option
    When I touch "Check Ethernet"
    Then The network settings are displayed

