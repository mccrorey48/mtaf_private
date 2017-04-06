from behave import *
from ePhone7.views import *
import re


@step("A call between two other accounts has been parked by the called account")
def step_impl(context):
    pass


@step('A "Call History" window appears')
def step_impl(context):
    pass


@step("A check mark appears in the box")
def step_impl(context):
    pass


@then('A "Clear All User Data" confirmation dialog appears')
def step_impl(context):
    pass


@step("A confirmation dialog appears")
def step_impl(context):
    pass


@step("A contact detail screen appears with a white star icon")
def step_impl(context):
    pass


@step("A contact detail screen appears with a yellow star icon")
def step_impl(context):
    pass


@step('A "Contact Management" window appears')
def step_impl(context):
    pass


@step("A Create New Group popup appears")
def step_impl(context):
    pass


@step('A "Dialpad Screen" window appears')
def step_impl(context):
    pass


@step('A "Factory Reset" confirmation dialog appears')
def step_impl(context):
    pass


@step("A Google dialog appears with a place to enter my email address")
def step_impl(context):
    pass


@step("A Google dialog appears with a place to enter my password")
def step_impl(context):
    pass


@step("A Google login screen appears")
def step_impl(context):
    pass


@step("A keypad appears")
def step_impl(context):
    pass


@step("A keypad appears with a list of contacts")
def step_impl(context):
    pass


@step("A list of contacts containing the partial number appears above the keypad")
def step_impl(context):
    pass


@step("A list of Coworker contacts appears")
def step_impl(context):
    pass


@step("A list of Coworker contacts containing the partial name appears above the keypad")
def step_impl(context):
    pass


@step("A list of Personal contacts containing the partial name appears above the keypad")
def step_impl(context):
    pass


@then("A menu appears with time zone choices")
def step_impl(context):
    pass


@then('A menu with a "Clear App Data/Cache" option appears')
def step_impl(context):
    pass


@then('A menu with a "Factory Reset" option appears')
def step_impl(context):
    pass


@step("A message indicates that calls are being forwarded to the contact")
def step_impl(context):
    pass


@step("A message indicates that calls are being forwarded to voicemail")
def step_impl(context):
    pass


@step("A popup informs me that help email has been sent to my email address")
def step_impl(context):
    pass


@step('A "Preferences Screen" window appears')
def step_impl(context):
    pass


@step("a Record button is visible")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert user_view.element_is_present('CallRecordButton')
        context.record_button = user_view.find_named_element('CallRecordButton')


@then('A "Select Ringtone" window appears with options for various ringtones')
def step_impl(context):
    pass


@step('A "Sign Out of Google Account" dialog appears')
def step_impl(context):
    pass


@then('A "Sleep Timer Setting" window appears with buttons for various timer settings')
def step_impl(context):
    pass


@then('A submenu appears with a "Brightness" option')
def step_impl(context):
    pass


@then('A submenu appears with a "Call Forwarding Options" option')
def step_impl(context):
    pass


@then('A submenu appears with a "Date/Time Options" option')
def step_impl(context):
    pass


@then('A submenu appears with a "Default Contacts Tab" option')
def step_impl(context):
    pass


@step('A submenu appears with a "Manage Accounts" option')
def step_impl(context):
    pass


@then('A submenu appears with a "Network" option')
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_view.element_is_present('MenuItemNetworkText')


@then('A submenu appears with a "Ringtones" option')
def step_impl(context):
    pass


@then('A submenu appears with a "Screen Timeout" option')
def step_impl(context):
    pass


@step('A submenu appears with a "Sign in with Google" option')
def step_impl(context):
    pass


@then('A submenu appears with a "Utilities" option')
def step_impl(context):
    pass


@then('A submenu appears with a "Volume Control" option')
def step_impl(context):
    pass


@then('A submenu appears with an "Auto-Answer Calls" toggle')
def step_impl(context):
    pass


@step('A submenu opens with a "Walkthrough" option')
def step_impl(context):
    pass


@step("A submenu opens with an eHelp option")
def step_impl(context):
    pass


@step('A "Visual Voicemail" window appears')
def step_impl(context):
    pass


@step("A voicemail detail window appears")
def step_impl(context):
    pass


@step('A "Voicemail Playback" window appears')
def step_impl(context):
    pass


@step('A "Welcome to ePhone7!" window appears')
def step_impl(context):
    pass


@step("A window appears with a button for each Contacts tab")
def step_impl(context):
    pass


@then('A window appears with a "Check Ethernet" option')
def step_impl(context):
    pass


@step("A window appears with a list of contacts")
def step_impl(context):
    pass


@then('A window appears with a section labeled "Call Forward Busy"')
def step_impl(context):
    pass


@step('A window appears with a section labeled "Call Forward No Answer"')
def step_impl(context):
    pass


@step('A window appears with the label "Screen Brightness" appears')
def step_impl(context):
    pass


@then('A window with a "24-hour Format" toggle appears')
def step_impl(context):
    pass


@then('A window with a "Change Timezone" option appears')
def step_impl(context):
    pass


@then('A window with a "Media Volume" slider appears')
def step_impl(context):
    pass


@then('A window with a "Ringer Volume" slider appears')
def step_impl(context):
    pass


@then('A window with a "Touch Sounds" toggle appears')
def step_impl(context):
    pass


@then('A window with a "Voice Call" slider appears')
def step_impl(context):
    pass


@step("Add and Delete buttons are not visible")
def step_impl(context):
    pass


@step("Add and Delete buttons are visible")
def step_impl(context):
    pass


@step('An "Account Deleted" popup appears')
def step_impl(context):
    pass


@step('an "Active Call Dialpad" window appears')
def step_impl(context):
    pass


@step('an "Active Call Screen" window appears')
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        base_view.find_named_element('ActiveCallScreen')


@then('An "Add Multiple Favorites" confirmation dialog appears')
def step_impl(context):
    pass


@step("Any existing Favorite contacts have a yellow start icon")
def step_impl(context):
    pass


@step("Any other contacts have a white start icon")
def step_impl(context):
    pass


@step("Both windows disappear")
def step_impl(context):
    pass


@step("I am logged in to the ePhone7")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        base_view.send_keycode('KEYCODE_BACK')
        # base_view.close_appium()
        # base_view.open_appium()
        # if prefs_view.element_is_present('Preferences'):
        #     prefs_view.click_named_element('Close')
        if not user_view.element_is_present('UserHeaderName', timeout=120):
            login_view.login()
            tnc_view.accept_tnc()
            app_intro_view.skip_intro()
            assert user_view.element_is_present('UserHeaderName', 10), 'Unable to log in'
        else:
            print("UserHeaderName found")


@step("I am not signed in to my gmail account")
def step_impl(context):
    pass


@step("I am signed in to my gmail account")
def step_impl(context):
    pass


@step("I answer the call")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        user_view.click_named_element('IncomingCallAnswerToSpeaker')
        user_view.softphones[context.caller_name].wait_for_call_status('call', user_view.call_status_wait)


@step("I can choose Cancel or OK by touching the corresponding button")
def step_impl(context):
    pass


@step("I can see my personal contacts")
def step_impl(context):
    pass


@step("I check the Call Record Enable checkbox")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        cbs = base_view.find_named_elements("AdvancedCheckbox")
        assert len(cbs) > 2, "Expected >2 AdvancedCheckbox elements, got %s" % len(cbs)
        if cbs[1].get_attribute('checked') == 'false':
            cbs[1].click()
            checked = cbs[1].get_attribute('checked')
            assert checked == 'true'


@step("I close all open submenus")
def step_impl(context):
    pass


@step("I close the contact detail screen")
def step_impl(context):
    pass


@step("I close the Preferences window")
def step_impl(context):
    pass


@when("I dial the {code_name} direct code")
def dial_server_direct_code(context, code_name):
    if 'fake' not in str(context._config.tags).split(','):
        keypad_view.dial_name(code_name)


@then("The reboot alert window appears")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert prefs_view.element_is_present("VlanRebootAlert")


@step("I end the call")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        user_view.end_call()


@step("I enter a 10-digit phone number using the keypad")
def step_impl(context):
    pass


@step("I enter a Coworker contact number using the keypad")
def step_impl(context):
    pass


@step("I enter a group name")
def step_impl(context):
    pass


@when("I enter a VLAN identifier between 1 and 4094")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_view.find_named_element('VlanIdentifier').clear()
        prefs_view.send_keycode('KEYCODE_2')
        prefs_view.send_keycode('KEYCODE_0')
        prefs_view.send_keycode('KEYCODE_BACK')



@when("I enter a VLAN identifier greater than 4094")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_view.find_named_element('VlanIdentifier').clear()
        prefs_view.send_keycode('KEYCODE_4')
        prefs_view.send_keycode('KEYCODE_3')
        prefs_view.send_keycode('KEYCODE_3')
        prefs_view.send_keycode('KEYCODE_3')
        prefs_view.send_keycode('KEYCODE_BACK')


@step("I enter a VLAN priority between 0 and 7")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_view.find_named_element('VlanPriority').clear()
        prefs_view.send_keycode('KEYCODE_3')
        prefs_view.send_keycode('KEYCODE_BACK')


@step("I enter a VLAN priority greater than 7")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_view.find_named_element('VlanPriority').clear()
        prefs_view.send_keycode('KEYCODE_8')
        prefs_view.send_keycode('KEYCODE_BACK')


@step("I enter my email address")
def step_impl(context):
    pass


@step("I enter my Google user id and password")
def step_impl(context):
    pass


@step("I enter my password")
def step_impl(context):
    pass


@step("I enter part of a Coworker contact name using the keypad")
def step_impl(context):
    pass


@step("I enter part of a Coworker contact number using the keypad")
def step_impl(context):
    pass


@step("I enter part of a Personal contact name using the keypad")
def step_impl(context):
    pass


@step("I enter part of a Personal contact number using the keypad")
def step_impl(context):
    pass


@step("I enter the call park queue number")
def step_impl(context):
    pass


@step("I go to the Contacts view")
def step_impl(context):
    # user_view.goto_tab('Contacts')
    pass


@step("I go to the Home view")
def step_impl(context):
    # user_view.goto_tab('Contacts')
    pass


@step("I go to the New Voicemail view")
def step_impl(context):
    # contacts_view.goto_tab('Personal')
    pass


@step("I go to the Personal tab")
def step_impl(context):
    # contacts_view.goto_tab('Personal')
    pass


@step("I go to the Saved Voicemail view")
def step_impl(context):
    # contacts_view.goto_tab('Personal')
    pass


@step("I have at least one new voicemail")
def step_impl(context):
    pass


@step("I have at least one saved voicemail")
def step_impl(context):
    pass


@step("I ignore the call")
def step_impl(context):
    pass


@when("I long-press a contact list item")
def step_impl(context):
    pass


@step("I make a call to a coworker contact")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        context.softphone = user_view.configure_called_answer_ring()
        keypad_view.dial_number(context.softphone.number)
        keypad_view.click_named_element('FuncKeyCall')
        context.softphone.wait_for_call_status('early', keypad_view.call_status_wait)



@step("I receive a call")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        context.caller_name, src_cfg = user_view.receive_call()


@step("I receive a new voicemail")
def step_impl(context):
    pass


@when("I scroll down to the Call Record Enable setting")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        elems = base_view.find_named_elements('AdvancedItems')
        assert len(elems) > 1
        base_view.scroll(elems[-1], elems[0])
        length = len(base_view.find_named_elements('CallRecordEnableText'))
        # one retry in case the scroll didn't work
        if length != 1:
            elems = base_view.find_named_elements('AdvancedItems')
            assert len(elems) > 1
            base_view.scroll(elems[-1], elems[0])
        assert length == 1, "Expected exactly one CallRecordEnableText element, got %s" % length


@step("I scroll to the top of the Advanced Options view")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("I see a warning message and the phone does not reboot")
def step_impl(context):
    pass


@step("I see the All and Missed tabs at the top of the screen")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        history_view.find_named_element('All')
        history_view.find_named_element('Missed')


@step("I see the call at the top of the All History view")
def step_impl(context):
    pass


@step("I see the call at the top of the Missed History view")
def step_impl(context):
    pass


@step("I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        user_view.find_named_element('Contacts')
        user_view.find_named_element('History')
        user_view.find_named_element('Voicemail')
        user_view.find_named_element('Keypad')


@step("I see the keypad")
def step_impl(context):
    pass


@step("I see the Need Help, Personal, Phone and System category elements")
def step_impl(context):
    pass


@then("I see the Network Settings view")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert prefs_view.element_is_present('NetworkSettingsLabel')


@step("I see the New, Saved and Trash tabs at the top of the screen")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert voicemail_view.element_is_present('New')
        assert voicemail_view.element_is_present('Saved')
        assert voicemail_view.element_is_present('Trash')


@step("I see the Personal, Coworkers, Favorites and Groups tabs")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert contacts_view.element_is_present('Personal')
        assert contacts_view.element_is_present('Coworkers')
        assert contacts_view.element_is_present('Favorites')
        assert contacts_view.element_is_present('Groups')


@step("I swipe down twice")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("I swipe the screen from right to left")
def step_impl(context):
    pass


@step("I touch a check a box next to a contact")
def step_impl(context):
    pass


@step("I touch a contact element")
def step_impl(context):
    pass


@when("I touch a new time zone choice")
def step_impl(context):
    pass


@step("I touch and drag the slider control handle")
def step_impl(context):
    pass


@when('I touch and drag the toggle handle to the "Off" position')
def step_impl(context):
    pass


@when('I touch and drag the toggle handle to the "On" position')
def step_impl(context):
    pass


@when('I touch "Brightness"')
def step_impl(context):
    pass


@when('I touch "Call Forwarding"')
def step_impl(context):
    pass


@when('I touch "Call Forwarding Options"')
def step_impl(context):
    pass


@step('I touch "Check Ethernet"')
def step_impl(context):
    pass


@when('I touch "Clear App Data/Cache"')
def step_impl(context):
    pass


@step('I touch "Confirm"')
def step_impl(context):
    pass


@when('I touch "Date/Time Options"')
def step_impl(context):
    pass


@when('I touch "Default Contacts Tab"')
def step_impl(context):
    pass


@step('I touch "eHelp"')
def step_impl(context):
    pass


@step('I touch "Factory Reset"')
def step_impl(context):
    pass


@step('I touch "Manage Accounts"')
def step_impl(context):
    pass


@step('I touch "Need Help"')
def step_impl(context):
    pass


@step('I touch "Next"')
def step_impl(context):
    pass


@step('I touch "OK"')
def step_impl(context):
    pass


@step('I touch "OK" on the popup')
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        base_view.click_named_element("ConfirmButton")


@step('I touch "Personal"')
def step_impl(context):
    pass


@when('I touch "Phone"')
def step_impl(context):
    pass


@when('I touch "Ringtones"')
def step_impl(context):
    pass


@step('I touch "Save and Reboot"')
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_view.click_named_element('NetworkSaveAndReboot')
        pass


@when('I touch "Screen Timeout"')
def step_impl(context):
    pass


@step('I touch "Sign in with Google"')
def step_impl(context):
    pass


@when('I touch "System"')
def step_impl(context):
    pass


@step('I touch the "About" menu item')
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_view.click_named_element('About')


@step("I touch the Add button")
def step_impl(context):
    pass


@step("I touch the All tab")
def step_impl(context):
    pass


@step("I touch the Back button")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        base_view.send_keycode('KEYCODE_BACK')


@when("I touch the button for another ringtone")
def step_impl(context):
    pass


@step("I touch the button for another tab")
def step_impl(context):
    pass


@when("I touch the button for another timer setting")
def step_impl(context):
    pass


@step("I touch the Call button")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        keypad_view.click_named_element('FuncKeyCall')


@when('I touch the "Call Forward Busy" section')
def step_impl(context):
    pass


@step("I touch the Call Forward icon")
def step_impl(context):
    pass


@step('I touch the "Call Forward No Answer" section')
def step_impl(context):
    pass


@when('I touch the "Cancel" button')
def step_impl(context):
    pass


@step("I touch the contact listing  I want to call")
def step_impl(context):
    pass


@step("I touch the contact listing I want to call")
def step_impl(context):
    pass


@step("I touch the Contacts button")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        user_view.click_named_element('Contacts')


@step('I touch the "Contacts" button')
def step_impl(context):
    pass


@step("I touch the Coworkers tab")
def step_impl(context):
    pass


@step("I touch the Create button")
def step_impl(context):
    pass


@when("I touch the current time zone text")
def step_impl(context):
    pass


@step("I touch the Delete button")
def step_impl(context):
    pass


@step("I touch the Delete icon")
def step_impl(context):
    pass


@step("I touch the Dial button")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        user_view.click_named_element('Keypad')


@step("I touch the Do Not Disturb icon")
def step_impl(context):
    pass


@step("I touch the Done button")
def step_impl(context):
    pass


@when("I touch the Favorites star icon on some contacts")
def step_impl(context):
    pass


@step("I touch the Favorites tab")
def step_impl(context):
    pass


@step("I touch the Forward icon")
def step_impl(context):
    pass


@step("I touch the Groups tab")
def step_impl(context):
    pass


@step("I touch the handset icon")
def step_impl(context):
    pass


@step("I touch the handset icon on a contact list item")
def step_impl(context):
    pass


@step("I touch the History button")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        user_view.click_named_element('History')


@step("I touch the Missed tab")
def step_impl(context):
    pass


@step("I touch the name of a contact")
def step_impl(context):
    pass


@step("I touch the name of a contact that is not a Favorite")
def step_impl(context):
    pass


@step("I touch the name of a personal Group list")
def step_impl(context):
    pass


@step("I touch the name of a system Group list")
def step_impl(context):
    pass


@when('I touch the "Network" option')
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_view.click_named_element('MenuItemNetworkText')


@step("I touch the New tab")
def step_impl(context):
    pass


@step("I touch the new voicemail element")
def step_impl(context):
    pass


@step('I touch the "Personal" tab')
def step_impl(context):
    pass


@given("I touch the Personal tab")
def step_impl(context):
    pass


@step("I touch the Preferences icon")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        user_view.click_named_element('PrefsButton')


@step("I touch the Save icon")
def step_impl(context):
    pass


@step("I touch the Saved tab")
def step_impl(context):
    pass


@step('I touch the "Sign in with Google" banner')
def step_impl(context):
    # contacts_view.click_named_element('GoogleSignInBanner')
    pass


@step('I touch the "System" menu category')
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_view.hide_list_items()
        prefs_view.click_named_element('System')


@step("I touch the Trash tab")
def step_impl(context):
    pass


@when('I touch the "Utilities" option')
def step_impl(context):
    pass


@when("I touch the VLAN Disable button")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_view.click_named_element('VlanDisable')


@step("I enable VLAN")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        elem = prefs_view.find_named_element('VlanEnable')
        if elem.get_attribute('checked') == 'false':
            elem.click()
            assert elem.get_attribute('checked') == 'true'


@step("I touch the Voicemail button")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        user_view.click_named_element('Voicemail')


@step("I touch the voicemail element")
def step_impl(context):
    pass


@step("I touch the voicemail icon")
def step_impl(context):
    pass


@step("I touch the Voicmail button")
def step_impl(context):
    pass


@step("I touch the white star icon")
def step_impl(context):
    pass


@step('I touch the "X" icon')
def step_impl(context):
    pass


@step("I touch the yellow star icon")
def step_impl(context):
    pass


@when('I touch "Volume Control"')
def step_impl(context):
    pass


@step('I touch "Walkthrough"')
def step_impl(context):
    pass


@step("I uncheck the Call Record Enable checkbox")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        cbs = base_view.find_named_elements("AdvancedCheckbox")
        assert len(cbs) > 2, "Expected >2 AdvancedCheckbox elements, got %s" % len(cbs)
        if cbs[1].get_attribute('checked') == 'true':
            cbs[1].click()
            assert cbs[1].get_attribute('checked') == 'false'


@step("I use the keypad to filter the list of contacts")
def step_impl(context):
    pass


@step("My account does not have two-step verification enabled")
def step_impl(context):
    pass


@step("My Coworker contacts are displayed in a list with checkboxes")
def step_impl(context):
    pass


@step("My Coworker contacts are each listed with a handset icon")
def step_impl(context):
    pass


@step("My Coworker contacts are shown on the display")
def step_impl(context):
    pass


@step("My Favorite contacts appear on the Coworkers contacts list")
def step_impl(context):
    pass


@step("My Favorite contacts are shown on the display")
def step_impl(context):
    pass


@step("My Google contacts are shown on the display")
def step_impl(context):
    pass


@step("My Group Lists are shown on the display")
def step_impl(context):
    pass


@then("my new voicemails are listed")
def step_impl(context):
    pass


@then("My Personal contacts are each listed with a handset icon")
def step_impl(context):
    pass


@then("My Personal contacts are shown on the display")
def step_impl(context):
    pass


@step("My phone calls back the caller")
def step_impl(context):
    pass


@step("My phone calls the contact")
def step_impl(context):
    pass


@step("My phone calls the number")
def step_impl(context):
    pass


@step("My phone calls the voicemail sender")
def step_impl(context):
    pass


@then("my saved voicemails are listed")
def step_impl(context):
    pass


@then("My updated Favorite contacts are shown on the display")
def step_impl(context):
    pass


@step("Only the contact I touched is listed")
def step_impl(context):
    pass


@step("Only the current ringtone has a dot next to it")
def step_impl(context):
    pass


@then("Only the new ringtone has a dot next to it")
def step_impl(context):
    pass


@step("Someone calls me")
def step_impl(context):
    pass


@step('the "Account Deleted" popup disappears')
def step_impl(context):
    pass


@then("the Advanced Options view appears")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert base_view.element_is_present('AdvancedOptions'), "Expected Advanced Options view to appear but it did not"


@then("the Advanced Options view disappears")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert base_view.element_is_not_present('AdvancedOptions'), "Expected Advanced Options view to disappear but it did not"


@step("the Call Forward icon is blue")
def step_impl(context):
    pass


@step("the Call Forward icon is red")
def step_impl(context):
    pass


@step("the call has a blue handset icon with an incoming arrow")
def step_impl(context):
    pass


@step("the call has a green handset icon with an outgoing arrow")
def step_impl(context):
    pass


@step("the call has a red handset icon with a missed arrow")
def step_impl(context):
    pass


@step("the call has a voicemail icon")
def step_impl(context):
    pass


@step("the Call Park icon")
def step_impl(context):
    pass


@step("the caller ends the call")
def step_impl(context):
    pass


@step("the caller gets a voicemail prompt")
def step_impl(context):
    pass


@step("the caller is connected to my phone")
def step_impl(context):
    pass


@step("the caller leaves a message")
def step_impl(context):
    pass


@step("the caller leaves a voicemail")
def step_impl(context):
    pass


@then("the color toggles between yellow and white")
def step_impl(context):
    pass


@step("the contact is not shown on the contact list for the group")
def step_impl(context):
    pass


@step("the contact is not shown on the display")
def step_impl(context):
    pass


@step("the contact is shown on the contact list for the group")
def step_impl(context):
    pass


@step("the contact is shown on the display")
def step_impl(context):
    pass


@step("the contact list for the group is displayed")
def step_impl(context):
    pass


@then("the contacts are shown with a Favorites star icon next to each one")
def step_impl(context):
    pass


@step("the Contacts tab window disappears")
def step_impl(context):
    pass


@step("the Contacts view appears")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert contacts_view.element_is_present('ContactsList')


@step('the correct version is displayed')
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        about_popup = prefs_view.find_named_element('AppVersion')
        source = about_popup.text
        prefs_view.click_named_element('AboutOk')
        prefs_view.click_named_element('System')
        m = re.match('App Version : (\S*)', source.encode('utf8'))
        if m is None:
            print("Unknown Version")
        else:
            version = m.group(1)
            print("\nVersion = %s" % version)
            expected = context.config.userdata.get('version')
            assert version == expected, "Incorrect Version: expected %s, got %s" % (expected, version)
        pass


@step("the coworker contact answers the call")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        context.softphone.account_info.call.answer(200)
        context.softphone.wait_for_call_status('call', user_view.call_status_wait)
    pass

@step("the current default tab is selected")
def step_impl(context):
    pass


@then("the Current OTA Server popup appears")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert(keypad_view.element_is_present('CurrentOtaPopup'))


@then("the Current OTA Server popup disappears")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert(keypad_view.element_is_not_present('CurrentOtaPopup'))


@step("the current time zone text is shown")
def step_impl(context):
    pass


@step("the current timer setting is selected")
def step_impl(context):
    pass


@then("the Dial view appears")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert keypad_view.element_is_present('DialPad')


@step("the Disable button is active")
def step_impl(context):
    pass


@step("the Do Not Disturb icon is blue")
def step_impl(context):
    pass


@step("the Do Not Disturb icon is red")
def step_impl(context):
    pass


@step("the Do Not Disturb icon turns blue")
def step_impl(context):
    pass


@step("the Do Not Disturb icon turns red")
def step_impl(context):
    pass


@step("the Google dialog disappears")
def step_impl(context):
    pass


@step("the Group list contacts are displayed in a list with checkboxes")
def step_impl(context):
    pass


@step("the History view appears")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert history_view.element_is_present('HistoryList')


@step("the in-call window appears")
def step_impl(context):
    pass


@step("the in-call window disappears")
def step_impl(context):
    pass


@step("the incoming call window appears")
def step_impl(context):
    pass


@step("the incoming call window disappears")
def step_impl(context):
    pass


@step("the keypad disappears")
def step_impl(context):
    pass


@then("the login screen appears")
def step_impl(context):
    pass


@step('the "Manage Accounts" element label changes to "Sign in with Google"')
def step_impl(context):
    pass


@then("the menu disappears")
def step_impl(context):
    pass


@then('the message "{message}" is shown')
def step_impl(context, message):
    if 'fake' not in str(context._config.tags).split(','):
        text = keypad_view.find_named_element('OtaUpdatePopupContent').text
        assert text == message, "expected %s, got %s" % (message, text)


@then("the network settings are displayed")
def step_impl(context):
    pass


@step("the new default tab is selected")
def step_impl(context):
    pass


@step("the new time zone text is shown")
def step_impl(context):
    pass


@then("the new timer setting is selected")
def step_impl(context):
    pass


@step("the new voicemail is the first item listed")
def step_impl(context):
    pass


@step("the New Voicemail view appears")
def step_impl(context):
    pass


@then('the "OTA Server Update" popup appears')
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert(keypad_view.element_is_present('OtaUpdatePopup'))


@then('the "OTA Server Update" popup disappears')
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert(keypad_view.element_is_not_present('OtaUpdatePopup'))


@step("the personal group list is shown on the display")
def step_impl(context):
    pass


@step("the popup disappears")
def step_impl(context):
    pass


@step("the popup does not show the current OTA URL")
def step_impl(context):
    pass


@step("the popup shows the current OTA environment name")
def step_impl(context):
    pass


@step("the position of the slider control changes")
def step_impl(context):
    pass


@step("the Preferences window appears")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert prefs_view.element_is_present('Preferences')


@step("the Preferences window disappears")
def step_impl(context):
    pass


@step("the previously added contact is not on the list with checkboxes")
def step_impl(context):
    pass


@step("the Record button is gray")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        user_view.get_screenshot_as_png('record_button')
        expected_color = [115, 115, 115]
        actual_color = user_view.get_element_color('record_button', context.record_button)
        assert actual_color == expected_color, "expected color %s, got %s" % (expected_color, actual_color)


@step("the Record button is white")
def step_impl(context):
    if 'fake' not in str(context._config.tags).split(','):
        user_view.get_screenshot_as_png('record_button')
        expected_color = [216, 216, 216]
        actual_color = user_view.get_element_color('record_button', context.record_button)
        assert actual_color == expected_color, "expected color %s, got %s" % (expected_color, actual_color)


@then('the "Ringtones" window disappears')
def step_impl(context):
    pass


@step('the section labeled "Call Forward Busy" is highlighted')
def step_impl(context):
    pass


@step('the section labeled "Call Forward Busy" is not highlighted')
def step_impl(context):
    pass


@step('the section labeled "Call Forward No Answer" is highlighted')
def step_impl(context):
    pass


@step('the section labeled "Call Forward No Answer" is not highlighted')
def step_impl(context):
    pass


@step('the "Sign in with Google" element label changes to "Manage Accounts"')
def step_impl(context):
    pass


@then('the "Sleep Timer Setting" window disappears')
def step_impl(context):
    pass


@step("the star turns white")
def step_impl(context):
    pass


@step("the star turns yellow")
def step_impl(context):
    pass


@step('the toggle handle is in the "Off" position')
def step_impl(context):
    pass


@step('the toggle handle is in the "On" position')
def step_impl(context):
    pass


@then('the toggle handle stays in the "Off" position')
def step_impl(context):
    pass


@then('the toggle handle stays in the "On" position')
def step_impl(context):
    pass


@given("the VLAN Enable button is active")
def step_impl(context):
    pass


@step("the voicemail audio plays back")
def step_impl(context):
    pass


@step("the voicemail detail window disappears")
def step_impl(context):
    pass


@step("the voicemail is also available in the destination contact's new voicemails list")
def step_impl(context):
    pass


@step("the voicemail is no longer listed")
def step_impl(context):
    pass


@step("the voicemail is still the first item in the view")
def step_impl(context):
    pass


@step("the voicemail is the first item listed")
def step_impl(context):
    pass


@step("the Voicemail view appears")
def step_impl(context):
    pass


@step("the window contains a slider control")
def step_impl(context):
    pass


@step("the window disappears")
def step_impl(context):
    pass


@given("VLAN is enabled")
def step_impl(context):
    pass


