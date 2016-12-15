from behave import *
from ePhone7.views import *
import re


@step('I touch the "System" menu category')
def step_impl(context):
    # prefs_view.hide_list_items()
    # prefs_view.click_element_by_key('System')
    pass


@step('I touch the "About" menu item')
def step_impl(context):
    # prefs_view.click_element_by_key('About')
    pass


@step('The correct version is displayed')
def step_impl(context):
    # about_popup = prefs_view.find_element_by_key('AppVersion')
    # source = about_popup.text
    # prefs_view.click_element_by_key('AboutOk')
    # prefs_view.click_element_by_key('System')
    # m = re.match('App Version : (\S*)', source.encode('utf8'))
    # if m is None:
    #     print("Unknown Version")
    # else:
    #     version = m.group(1)
    #     print("\nVersion = %s" % version)
    #     expected = context.config.userdata.get('version')
    #     assert version == expected, "Incorrect Version: expected %s, got %s" % (expected, version)
    pass


@step("I go to the Contacts view")
def step_impl(context):
    # user_view.goto_tab('Contacts')
    pass


@step("I go to the Personal tab")
def step_impl(context):
    # contacts_view.goto_tab('Personal')
    pass


@step('I touch the "Sign in with Google" banner')
def step_impl(context):
    # contacts_view.click_element_by_key('GoogleSignInBanner')
    pass


@step("A Google login screen appears")
def step_impl(context):
    pass


@step("I enter my Google user id and password")
def step_impl(context):
    pass


@step("My Google contacts are shown on the display")
def step_impl(context):
    pass


@step("I am logged in to the ePhone7")
def step_impl(context):
    pass


@step("I go to the Home view")
def step_impl(context):
    pass


@step("I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen")
def step_impl(context):
    pass


@step("the Contacts view appears")
def step_impl(context):
    pass


@step("the Voicemail view appears")
def step_impl(context):
    pass


@step("I see the Personal, Coworkers, Favorites and Groups tabs")
def step_impl(context):
    pass


@step("I touch the History button")
def step_impl(context):
    pass


@step('I touch "Next"')
def step_impl(context):
    pass


@step('I touch "Personal"')
def step_impl(context):
    pass


@step('I touch "Sign in with Google"')
def step_impl(context):
    pass


@step("I see the All and New tabs at the top of the screen")
def step_impl(context):
    pass


@step("I see the New, Saved and Trash tabs at the top of the screen")
def step_impl(context):
    pass


@step("I touch the Dial button")
def step_impl(context):
    pass


@step("the Dial view appears")
def step_impl(context):
    pass


@step("I touch the Preferences button")
def step_impl(context):
    pass


@step("the Preferences view appears")
def step_impl(context):
    pass


@step("I touch the Contacts button")
def step_impl(context):
    pass


@step("I touch the Coworkers tab")
def step_impl(context):
    pass


@step("My Coworker contacts are shown on the display")
def step_impl(context):
    pass


@step("My Coworker contacts appear on the Coworkers contacts list")
def step_impl(context):
    pass


@step("I touch the handset icon on a contact list item")
def step_impl(context):
    pass


@step("My phone calls the contact")
def step_impl(context):
    pass


@step("I touch the Favorites tab")
def step_impl(context):
    pass


@step("My Favorite contacts are shown on the display")
def step_impl(context):
    pass


@step("My Favorite contacts appear on the Coworkers contacts list")
def step_impl(context):
    pass


@step("I touch the name of a contact that is not a Favorite")
def step_impl(context):
    pass


@step("A contact detail screen appears with a white star icon")
def step_impl(context):
    pass


@step("I touch the white star icon")
def step_impl(context):
    pass


@step("The star turns yellow")
def step_impl(context):
    pass


@step("The contact is shown on the display")
def step_impl(context):
    pass


@step("A contact detail screen appears with a yellow star icon")
def step_impl(context):
    pass


@step("I touch the yellow star icon")
def step_impl(context):
    pass


@step("The star turns white")
def step_impl(context):
    pass


@step("I close the contact detail screen")
def step_impl(context):
    pass


@step("The contact is not shown on the display")
def step_impl(context):
    pass


@step("I touch the name of a contact")
def step_impl(context):
    pass


@step("I touch the Groups tab")
def step_impl(context):
    pass


@step("My Group Lists are shown on the display")
def step_impl(context):
    pass


@step("I touch the Add button")
def step_impl(context):
    pass


@step("A Create New Group popup appears")
def step_impl(context):
    pass


@step("I enter a group name")
def step_impl(context):
    pass


@step("I touch the Create button")
def step_impl(context):
    pass


@step("The personal group list is shown on the display")
def step_impl(context):
    pass


@step("I touch the name of a personal Group list")
def step_impl(context):
    pass


@step("The contact list for the group is displayed")
def step_impl(context):
    pass


@step("Add and Delete buttons are visible")
def step_impl(context):
    pass


@step("My Coworker contacts are displayed in a list with checkboxes")
def step_impl(context):
    pass


@step("I touch a check a box next to a contact")
def step_impl(context):
    pass


@step("A check mark appears in the box")
def step_impl(context):
    pass


@step("I touch the Done button")
def step_impl(context):
    pass


@step("The contact is shown on the contact list for the group")
def step_impl(context):
    pass


@step("The previously added contact is not on the list with checkboxes")
def step_impl(context):
    pass


@step("I touch the Delete button")
def step_impl(context):
    pass


@step("The Group list contacts are displayed in a list with checkboxes")
def step_impl(context):
    pass


@step("The contact is not shown on the contact list for the group")
def step_impl(context):
    pass


@step("I touch the name of a system Group list")
def step_impl(context):
    pass


@step("Add and Delete buttons are not visible")
def step_impl(context):
    pass


@step("I touch the Voicemail button")
def step_impl(context):
    pass


@step("I touch the New tab")
def step_impl(context):
    pass


@step("I receive a new voicemail")
def step_impl(context):
    pass


@step("The new voicemail is the first item listed")
def step_impl(context):
    pass


@step("I touch the new voicemail element")
def step_impl(context):
    pass


@step("A voicemail detail window appears")
def step_impl(context):
    pass


@step("The voicemail audio plays back")
def step_impl(context):
    pass


@step("I touch the handset icon")
def step_impl(context):
    pass


@step("The voicemail detail window disappears")
def step_impl(context):
    pass


@step("My phone calls the voicemail sender")
def step_impl(context):
    pass


@step("I touch the Delete icon")
def step_impl(context):
    pass


@step("The voicemail is no longer listed")
def step_impl(context):
    pass


@step("I touch the Save icon")
def step_impl(context):
    pass


@step("I touch the Saved tab")
def step_impl(context):
    pass


@step("The voicemail is the first item listed")
def step_impl(context):
    pass


@step("I touch the voicemail element")
def step_impl(context):
    pass


@step("I touch the Trash tab")
def step_impl(context):
    pass


@step("I touch the Forward icon")
def step_impl(context):
    pass


@step("A list of Coworker contacts appears")
def step_impl(context):
    pass


@step("A keypad appears")
def step_impl(context):
    pass


@step("I use the keypad to filter the list of contacts")
def step_impl(context):
    pass


@step("I touch a contact element")
def step_impl(context):
    pass


@step("I can choose Cancel or OK by touching the corresponding button")
def step_impl(context):
    pass


@step("I choose OK")
def step_impl(context):
    pass


@step("The voicemail is still the first item in the view")
def step_impl(context):
    pass


@step("The voicemail is also available in the destination contact's new voicemails list")
def step_impl(context):
    pass


@step("I see the All and Missed tabs at the top of the screen")
def step_impl(context):
    pass


@step("I receive a call")
def step_impl(context):
    pass


@step("The incoming call window appears")
def step_impl(context):
    pass


@step("I answer the call")
def step_impl(context):
    pass


@step("I end the call")
def step_impl(context):
    pass


@step("The incoming call window disappears")
def step_impl(context):
    pass


@step("I touch the All tab")
def step_impl(context):
    pass


@step("I see the call at the top of the All History view")
def step_impl(context):
    pass


@step("The call has a blue handset icon with an incoming arrow")
def step_impl(context):
    pass


@step("I ignore the call")
def step_impl(context):
    pass


@step("The caller ends the call")
def step_impl(context):
    pass


@step("The call has a red handset icon with a missed arrow")
def step_impl(context):
    pass


@step("I touch the Missed tab")
def step_impl(context):
    pass


@step("I see the call at the top of the Missed History view")
def step_impl(context):
    pass


@step("The caller leaves a voicemail")
def step_impl(context):
    pass


@step("The call has a voicemail icon")
def step_impl(context):
    pass


@step("I make a call to a coworker contact")
def step_impl(context):
    pass


@step("The in-call window appears")
def step_impl(context):
    pass


@step("The in-call window disappears")
def step_impl(context):
    pass


@step("The call has a green handset icon with an outgoing arrow")
def step_impl(context):
    pass


@step("My phone calls back the caller")
def step_impl(context):
    pass


@step("I touch the voicemail icon")
def step_impl(context):
    pass


@step("I see the keypad")
def step_impl(context):
    pass


@step("I enter a Coworker contact number using the keypad")
def step_impl(context):
    pass


@step("I touch the Call button")
def step_impl(context):
    pass


@step("My phone calls the number")
def step_impl(context):
    pass


@step("I enter a 10-digit phone number using the keypad")
def step_impl(context):
    pass


@step("I enter part of a Coworker contact number using the keypad")
def step_impl(context):
    pass


@step("A list of contacts containing the partial number appears above the keypad")
def step_impl(context):
    pass


@step("I touch the contact listing  I want to call")
def step_impl(context):
    pass


@step("Only the contact I touched is listed")
def step_impl(context):
    pass


@step("I enter part of a Personal contact number using the keypad")
def step_impl(context):
    pass


@step("I touch the contact listing I want to call")
def step_impl(context):
    pass


@step("I enter part of a Coworker contact name using the keypad")
def step_impl(context):
    pass


@step("A list of Coworker contacts containing the partial name appears above the keypad")
def step_impl(context):
    pass


@step("I enter part of a Personal contact name using the keypad")
def step_impl(context):
    pass


@step("A list of Personal contacts containing the partial name appears above the keypad")
def step_impl(context):
    pass


@step("The Do Not Disturb icon is blue")
def step_impl(context):
    pass


@step("I touch the Do Not Disturb icon")
def step_impl(context):
    pass


@step("The Do Not Disturb icon turns red")
def step_impl(context):
    pass


@step("Someone calls me")
def step_impl(context):
    pass


@step("The caller gets a voicemail prompt")
def step_impl(context):
    pass


@step("The caller leaves a message")
def step_impl(context):
    pass


@step("The Do Not Disturb icon is red")
def step_impl(context):
    pass


@step("The Do Not Disturb icon turns blue")
def step_impl(context):
    pass


@step("A call between two other accounts has been parked by the called account")
def step_impl(context):
    pass


@step("The Call Park icon")
def step_impl(context):
    pass


@step("I enter the call park queue number")
def step_impl(context):
    pass


@step("The caller is connected to my phone")
def step_impl(context):
    pass


@step("I touch the Call Forward icon")
def step_impl(context):
    pass


@step("A keypad appears with a list of contacts")
def step_impl(context):
    pass


@step("I touch the OK button")
def step_impl(context):
    pass


@step("The keypad disappears")
def step_impl(context):
    pass


@step("The Call Forward icon is red")
def step_impl(context):
    pass


@step("I touch the Voicmail button")
def step_impl(context):
    pass


@step("The Call Forward icon is blue")
def step_impl(context):
    pass


@step("I go to the Preferences view")
def step_impl(context):
    pass


@step("I close all open submenus")
def step_impl(context):
    pass


@step("I see the Need Help, Personal, Phone and System category elements")
def step_impl(context):
    pass



@step("A submenu opens with an eHelp option")
def step_impl(context):
    pass


@step("A popup informs me that help email has been sent to my email address")
def step_impl(context):
    pass


@step("The popup disappears")
def step_impl(context):
    pass


@step('A submenu opens with a "Walkthrough" option')
def step_impl(context):
    pass


@step('A "Welcome to ePhone7!" window appears')
def step_impl(context):
    pass


@step("I swipe the screen from right to left")
def step_impl(context):
    pass


@step("My account does not have two-step verification enabled")
def step_impl(context):
    pass


@step('A submenu appears with a "Sign in with Google" option')
def step_impl(context):
    pass


@step("A Google dialog appears with a place to enter my email address")
def step_impl(context):
    pass


@step("I enter my email address")
def step_impl(context):
    pass


@step("A Google dialog appears with a place to enter my password")
def step_impl(context):
    pass


@step("I enter my password")
def step_impl(context):
    pass


@step("The Google dialog disappears")
def step_impl(context):
    pass


@step('The "Sign in with Google" element label changes to "Manage Accounts"')
def step_impl(context):
    pass


@step('I touch the "X" icon')
def step_impl(context):
    pass


@step("The Preferences window disappears")
def step_impl(context):
    pass


@step('I touch the "Contacts" button')
def step_impl(context):
    pass


@step('I touch the "Personal" tab')
def step_impl(context):
    pass


@step("I can see my personal contacts")
def step_impl(context):
    pass


@step('I touch "eHelp"')
def step_impl(context):
    pass


@step('A "Contact Management" window appears')
def step_impl(context):
    pass


@step('I touch "OK"')
def step_impl(context):
    pass


@step('I touch "Walkthrough"')
def step_impl(context):
    pass


@step('A "Call History" window appears')
def step_impl(context):
    pass


@step('A "Visual Voicemail" window appears')
def step_impl(context):
    pass


@step('A "Voicemail Playback" window appears')
def step_impl(context):
    pass


@step('A "Dialpad Screen" window appears')
def step_impl(context):
    pass


@step('A "Active Call Screen" window appears')
def step_impl(context):
    pass


@step('A "Active Call Dialpad" window appears')
def step_impl(context):
    pass


@step('A "Preferences Screen" window appears')
def step_impl(context):
    pass


@step('I touch "Need Help"')
def step_impl(context):
    pass


@step("A message indicates that calls are being forwarded to the contact")
def step_impl(context):
    pass


@step("A message indicates that calls are being forwarded to voicemail")
def step_impl(context):
    pass


@step("the History view appears")
def step_impl(context):
    pass


@step("I am not signed in to my gmail account")
def step_impl(context):
    pass


@step("I am signed in to my gmail account")
def step_impl(context):
    pass


@step('A submenu appears with a "Manage Accounts" option')
def step_impl(context):
    pass


@step('I touch "Manage Accounts"')
def step_impl(context):
    pass


@step('A "Sign Out of Google Account" dialog appears')
def step_impl(context):
    pass


@step("A confirmation dialog appears")
def step_impl(context):
    pass


@step('An "Account Deleted" popup appears')
def step_impl(context):
    pass


@step('The "Account Deleted" popup disappears')
def step_impl(context):
    pass


@step('The "Manage Accounts" element label changes to "Sign in with Google"')
def step_impl(context):
    pass


@step("A window appears with a button for each Contacts tab")
def step_impl(context):
    pass


@step("The current default tab is selected")
def step_impl(context):
    pass


@step("I touch the button for another tab")
def step_impl(context):
    pass


@step("The Contacts tab window disappears")
def step_impl(context):
    pass


@step("I close the Preferences window")
def step_impl(context):
    pass


@step("The new default tab is selected")
def step_impl(context):
    pass


@step('A window appears with a section labeled "Call Forward No Answer"')
def step_impl(context):
    pass


@step('The section labeled "Call Forward No Answer" is not highlighted')
def step_impl(context):
    pass


@step('I touch the "Call Forward No Answer" section')
def step_impl(context):
    pass


@step("A window appears with a list of contacts")
def step_impl(context):
    pass


@step('I touch the "OK" button')
def step_impl(context):
    pass


@step("Both windows disappear")
def step_impl(context):
    pass


@step('The section labeled "Call Forward No Answer" is highlighted')
def step_impl(context):
    pass


@step("The window disappears")
def step_impl(context):
    pass


@step('A window appears with the label "Screen Brightness" appears')
def step_impl(context):
    pass


@step("The window contains a slider control")
def step_impl(context):
    pass


@step("I touch and drag the slider control handle")
def step_impl(context):
    pass


@step("The position of the slider control changes")
def step_impl(context):
    pass


@then('A submenu appears with a "Default Contacts Tab" option')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when('I touch "Default Contacts Tab"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then('A submenu appears with a "Call Forwarding Options" option')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when('I touch "Call Forwarding Options"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when('I touch "Call Forwarding"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when('I touch the "Cancel" button')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then('A window appears with a section labeled "Call Forward Busy"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when('I touch the "Call Forward Busy" section')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step('The section labeled "Call Forward Busy" is highlighted')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step('The section labeled "Call Forward Busy" is not highlighted')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when('I touch "Phone"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then('A submenu appears with a "Brightness" option')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when('I touch "Brightness"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("Only the contact I touched is listed")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then('A submenu appears with a "Screen Timeout" option')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when('I touch "Screen Timeout"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then('A "Sleep Timer Setting" window appears with buttons for various timer settings')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("The current timer setting is selected")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the button for another timer setting")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("The new timer setting is selected")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then('The "Sleep Timer Setting" window disappears')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then('A "Select Ringtone" window appears with options for various ringtones')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("Only the current ringtone has a dot next to it")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the button for another ringtone")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("Only the new ringtone has a dot next to it")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then('A window with a "Touch Sounds" toggle appears')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step('The toggle handle is in the "Off" position')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when('I touch and drag the toggle handle to the "On" position')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then('The toggle handle stays in the "On" position')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then('A window with a "Ringer Volume" slider appears')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then('A submenu appears with an "Auto-Answer Calls" toggle')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then('A submenu appears with a "Ringtones" option')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when('I touch "Ringtones"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then('The "Ringtones" window disappears')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step('The toggle handle is in the "On" position')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when('I touch and drag the toggle handle to the "Off" position')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then('The toggle handle stays in the "Off" position')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then('A window with a "Voice Call" slider appears')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then('A submenu appears with a "Volume Control" option')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when('I touch "Volume Control"')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then('A window with a "Media Volume" slider appears')
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass