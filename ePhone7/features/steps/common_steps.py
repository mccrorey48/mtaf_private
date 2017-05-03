from behave import *
from ePhone7.views import *
from time import sleep
from prefs import *
from user import *
from advanced import *
from lib.user_exception import UserException as Ux

@step("A call between two other accounts has been parked by the called account")
def a_call_between_two_other_accounts_has_been_parked_by_the_called_account(context):
    pass


@step('A "Call History" window appears')
def a_call_history_window_appears(context):
    pass


@step('A "Clear All User Data" confirmation dialog appears')
def a_clear_all_user_data_confirmation_dialog_appears(context):
    pass


@step("A confirmation dialog appears")
def a_confirmation_dialog_appears(context):
    pass


@step('A "Contact Management" window appears')
def a_contact_management_window_appears(context):
    pass


@step('A "Dialpad Screen" window appears')
def a_dialpad_screen_window_appears(context):
    pass


@step('A "Factory Reset" confirmation dialog appears')
def a_factory_reset_confirmation_dialog_appears(context):
    pass


@step("A Google dialog appears with a place to enter my email address")
def a_google_dialog_appears_with_a_place_to_enter_my_email_address(context):
    pass


@step("A Google dialog appears with a place to enter my password")
def a_google_dialog_appears_with_a_place_to_enter_my_password(context):
    pass


@step("A keypad appears with a list of contacts")
def a_keypad_appears_with_a_list_of_contacts(context):
    pass


@step("A list of contacts containing the partial number appears above the keypad")
def a_list_of_contacts_containing_the_partial_number_appears_above_the_keypad(context):
    pass


@step("A list of Coworker contacts containing the partial name appears above the keypad")
def a_list_of_coworker_contacts_containing_the_partial_name_appears_above_the_keypad(context):
    pass


@step("A list of Personal contacts containing the partial name appears above the keypad")
def a_list_of_personal_contacts_containing_the_partial_name_appears_above_the_keypad(context):
    pass


@step("A menu appears with time zone choices")
def a_menu_appears_with_time_zone_choices(context):
    pass


@step('A menu with a "Clear App Data/Cache" option appears')
def a_menu_with_a_clear_app_datacache_option_appears(context):
    pass


@step('A menu with a "Factory Reset" option appears')
def a_menu_with_a_factory_reset_option_appears(context):
    pass


@step("A message indicates that calls are being forwarded to the contact")
def a_message_indicates_that_calls_are_being_forwarded_to_the_contact(context):
    pass


@step("A message indicates that calls are being forwarded to voicemail")
def a_message_indicates_that_calls_are_being_forwarded_to_voicemail(context):
    pass


@step("A popup informs me that help email has been sent to my email address")
def a_popup_informs_me_that_help_email_has_been_sent_to_my_email_address(context):
    pass


@step("a Record button is visible")
def a_record_button_is_visible(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert user_view.element_is_present('CallRecordButton')
        context.record_button = user_view.find_named_element('CallRecordButton')


@step('A "Select Ringtone" window appears with options for various ringtones')
def a_select_ringtone_window_appears_with_options_for_various_ringtones(context):
    pass


@step('A "Sign Out of Google Account" dialog appears')
def a_sign_out_of_google_account_dialog_appears(context):
    pass


@step('A "Sleep Timer Setting" window appears with buttons for various timer settings')
def a_sleep_timer_setting_window_appears_with_buttons_for_various_timer_settings(context):
    pass


@step('A submenu appears with a "Brightness" option')
def a_submenu_appears_with_a_brightness_option(context):
    pass


@step('A submenu appears with a "Call Forwarding Options" option')
def a_submenu_appears_with_a_call_forwarding_options_option(context):
    pass


@step('A submenu appears with a "Date/Time Options" option')
def a_submenu_appears_with_a_datetime_options_option(context):
    pass


@step('A submenu appears with a "Default Contacts Tab" option')
def a_submenu_appears_with_a_default_contacts_tab_option(context):
    pass


@step('A submenu appears with a "Manage Accounts" option')
def a_submenu_appears_with_a_manage_accounts_option(context):
    pass


@step('A submenu appears with a "Ringtones" option')
def a_submenu_appears_with_a_ringtones_option(context):
    pass


@step('A submenu appears with a "Screen Timeout" option')
def a_submenu_appears_with_a_screen_timeout_option(context):
    pass


@step('A submenu appears with a "Sign in with Google" option')
def a_submenu_appears_with_a_sign_in_with_google_option(context):
    pass


@step('A submenu appears with a "Utilities" option')
def a_submenu_appears_with_a_utilities_option(context):
    pass


@step('A submenu appears with a "Volume Control" option')
def a_submenu_appears_with_a_volume_control_option(context):
    pass


@step('A submenu appears with an "Auto-Answer Calls" toggle')
def a_submenu_appears_with_an_autoanswer_calls_toggle(context):
    pass


@step('A submenu opens with a "Walkthrough" option')
def a_submenu_opens_with_a_walkthrough_option(context):
    pass


@step("A submenu opens with an eHelp option")
def a_submenu_opens_with_an_ehelp_option(context):
    pass


@step('A "Visual Voicemail" window appears')
def a_visual_voicemail_window_appears(context):
    pass


@step('A "Voicemail Playback" window appears')
def a_voicemail_playback_window_appears(context):
    pass


@step('A "Welcome to ePhone7!" window appears')
def a_welcome_to_ephone7_window_appears(context):
    pass


@step("A window appears with a button for each Contacts tab")
def a_window_appears_with_a_button_for_each_contacts_tab(context):
    pass


@step('A window appears with a "Check Ethernet" option')
def a_window_appears_with_a_check_ethernet_option(context):
    pass


@step("A window appears with a list of contacts")
def a_window_appears_with_a_list_of_contacts(context):
    pass


@step('A window appears with a section labeled "Call Forward Busy"')
def a_window_appears_with_a_section_labeled_call_forward_busy(context):
    pass


@step('A window appears with a section labeled "Call Forward No Answer"')
def a_window_appears_with_a_section_labeled_call_forward_no_answer(context):
    pass


@step('A window appears with the label "Screen Brightness" appears')
def a_window_appears_with_the_label_screen_brightness_appears(context):
    pass


@step('A window with a "24-hour Format" toggle appears')
def a_window_with_a_24hour_format_toggle_appears(context):
    pass


@step('A window with a "Change Timezone" option appears')
def a_window_with_a_change_timezone_option_appears(context):
    pass


@step('A window with a "Media Volume" slider appears')
def a_window_with_a_media_volume_slider_appears(context):
    pass


@step('A window with a "Ringer Volume" slider appears')
def a_window_with_a_ringer_volume_slider_appears(context):
    pass


@step('A window with a "Touch Sounds" toggle appears')
def a_window_with_a_touch_sounds_toggle_appears(context):
    pass


@step('A window with a "Voice Call" slider appears')
def a_window_with_a_voice_call_slider_appears(context):
    pass


@step('An "Account Deleted" popup appears')
def an_account_deleted_popup_appears(context):
    pass


@step('an "Active Call Dialpad" window appears')
def an_active_call_dialpad_window_appears(context):
    pass


@step('an "Active Call Screen" window appears')
def an_active_call_screen_window_appears(context):
    if 'fake' not in str(context._config.tags).split(','):
        base_view.find_named_element('ActiveCallScreen')


@step("Both windows disappear")
def both_windows_disappear(context):
    pass


@step("[dial] I touch the Call button")
def dial__i_touch_the_call_button(context):
    if 'fake' not in str(context._config.tags).split(','):
        dial_view.click_named_element('FuncKeyCall')


@step("I am logged in to the ePhone7")
def i_am_logged_in_to_the_ephone7(context):
    if 'fake' not in str(context._config.tags).split(','):
        base_view.send_keycode('KEYCODE_BACK')
        # base_view.close_appium()
        # base_view.open_appium()
        # if prefs_view.element_is_present('Preferences'):
        #     prefs_view.exit_prefs()
        if not user_view.element_is_present('UserHeaderName', timeout=120):
            login_view.login()
            tnc_view.accept_tnc()
            app_intro_view.skip_intro()
            assert user_view.element_is_present('UserHeaderName', 10), 'Unable to log in'
        else:
            print("UserHeaderName found")


@step("I am not signed in to my gmail account")
def i_am_not_signed_in_to_my_gmail_account(context):
    pass


@step("I am signed in to my gmail account")
def i_am_signed_in_to_my_gmail_account(context):
    pass


@step("I answer the call")
def i_answer_the_call(context):
    if 'fake' not in str(context._config.tags).split(','):
        user_view.click_named_element('IncomingCallAnswerToSpeaker')
        user_view.softphones[context.caller_name].wait_for_call_status('call', user_view.call_status_wait)


@step("I can see my personal contacts")
def i_can_see_my_personal_contacts(context):
    pass


@step("I close all open submenus")
def i_close_all_open_submenus(context):
    pass


@when("I close the Preferences window")
def i_close_the_preferences_window(context):
    pass


@step("I end the call")
def i_end_the_call(context):
    if 'fake' not in str(context._config.tags).split(','):
        user_view.end_call()


@step("I enter a 10-digit phone number using the keypad")
def i_enter_a_10digit_phone_number_using_the_keypad(context):
    pass


@step("I enter a Coworker contact number using the keypad")
def i_enter_a_coworker_contact_number_using_the_keypad(context):
    pass


@step("I enter a VLAN identifier between 1 and 4094")
def i_enter_a_vlan_identifier_between_1_and_4094(context):
    if 'fake' not in str(context._config.tags).split(','):
        network_view.find_named_element('VlanIdentifier').clear()
        network_view.send_keycode('KEYCODE_2')
        network_view.send_keycode('KEYCODE_0')
        network_view.send_keycode('KEYCODE_BACK')


@step("I enter a VLAN priority greater than 7")
def i_enter_a_vlan_priority_greater_than_7(context):
    if 'fake' not in str(context._config.tags).split(','):
        network_view.find_named_element('VlanPriority').clear()
        network_view.send_keycode('KEYCODE_8')
        network_view.send_keycode('KEYCODE_BACK')


@step("I enter my email address")
def i_enter_my_email_address(context):
    pass


@step("I enter my password")
def i_enter_my_password(context):
    pass


@step("I enter part of a Coworker contact name using the keypad")
def i_enter_part_of_a_coworker_contact_name_using_the_keypad(context):
    pass


@step("I enter part of a Coworker contact number using the keypad")
def i_enter_part_of_a_coworker_contact_number_using_the_keypad(context):
    pass


@step("I enter part of a Personal contact name using the keypad")
def i_enter_part_of_a_personal_contact_name_using_the_keypad(context):
    pass


@step("I enter part of a Personal contact number using the keypad")
def i_enter_part_of_a_personal_contact_number_using_the_keypad(context):
    pass


@step("I enter the call park queue number")
def i_enter_the_call_park_queue_number(context):
    pass


@step("I go to the Contacts view")
def i_go_to_the_contacts_view(context):
    if 'fake' not in str(context._config.tags).split(','):
        user_view.goto_tab('Contacts')


@step("I go to the Home view")
def i_go_to_the_home_view(context):
    if 'fake' not in str(context._config.tags).split(','):
        user_view.goto_tab('Contacts')


@step("I go to the New Voicemail view")
def i_go_to_the_new_voicemail_view(context):
    if 'fake' not in str(context._config.tags).split(','):
        contacts_view.goto_tab('Personal')


@step("I go to the Saved Voicemail view")
def i_go_to_the_saved_voicemail_view(context):
    if 'fake' not in str(context._config.tags).split(','):
        contacts_view.goto_tab('Personal')


@step("I have at least one new voicemail")
def i_have_at_least_one_new_voicemail(context):
    pass


@step("I have at least one saved voicemail")
def i_have_at_least_one_saved_voicemail(context):
    pass


@step("I ignore the call")
def i_ignore_the_call(context):
    pass


@step("I make a call to a coworker contact")
def i_make_a_call_to_a_coworker_contact(context):
    if 'fake' not in str(context._config.tags).split(','):
        context.softphone = user_view.configure_called_answer_ring()
        dial_view.dial_number(context.softphone.number)
        dial_view.click_named_element('FuncKeyCall')
        context.softphone.wait_for_call_status('early', dial_view.call_status_wait)


@step("I receive a call")
def i_receive_a_call(context):
    if 'fake' not in str(context._config.tags).split(','):
        context.caller_name, src_cfg = user_view.receive_call()


@step("I receive a new voicemail")
def i_receive_a_new_voicemail(context):
    pass


@then('I see an "Invalid VLAN Priority" alert')
def i_see_an_invalid_vlan_priority_alert(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert network_view.element_is_present('InvalidVlanPriority'), "Expected Invalid VLAN Priority alert"


@step("I see the call at the top of the All History view")
def i_see_the_call_at_the_top_of_the_all_history_view(context):
    pass


@step("I see the call at the top of the Missed History view")
def i_see_the_call_at_the_top_of_the_missed_history_view(context):
    pass


@step("I see the keypad")
def i_see_the_keypad(context):
    pass


@then("I set the OTA server")
def i_set_the_ota_server(context):
    if 'fake' not in str(context._config.tags).split(','):
        ota_server = context.config.userdata.get('ota_server')
        app_version = context.app_version
        text = ''
        expected = ''
        if context.app_version == '1.0.10' and ota_server == 'alpha':
            # special case for version 1.0.10, directly enter the upgrade url
            user_view.set_ota_server(ota_server)
        else:
            user_view.goto_tab('Dial')
            if ota_server == 'beta':
                dial_view.dial_name('Beta OTA Server')
                dial_view.click_named_element('FuncKeyCall')
                text = dial_view.find_named_element('OtaUpdatePopupContent').text
                expected = 'Beta OTA Server Enabled'
            elif ota_server == 'alpha':
                dial_view.dial_name('Alpha OTA Server')
                dial_view.click_named_element('FuncKeyCall')
                text = dial_view.find_named_element('OtaUpdatePopupContent').text
                expected = 'Production OTA Server Enabled'
            elif ota_server == 'production':
                dial_view.dial_name('Production OTA Server')
                dial_view.click_named_element('FuncKeyCall')
                text = dial_view.find_named_element('OtaUpdatePopupContent').text
                expected = 'Production OTA Server Enabled'
            else:
                raise Ux('unknown expected ota_server defined: %s' % ota_server)
            assert text == expected, "expected %s, got %s" % (expected, text)
            base_view.click_named_element('OtaAddressOk')
            base_view.send_keycode('KEYCODE_BACK')
            sleep(5)


@step("I swipe down twice")
def i_swipe_down_twice(context):
    pass


@step("I swipe the screen from right to left")
def i_swipe_the_screen_from_right_to_left(context):
    pass


@step("I touch a new time zone choice")
def i_touch_a_new_time_zone_choice(context):
    pass


@step("I touch and drag the slider control handle")
def i_touch_and_drag_the_slider_control_handle(context):
    pass


@step('I touch and drag the toggle handle to the "Off" position')
def i_touch_and_drag_the_toggle_handle_to_the_off_position(context):
    pass


@step('I touch and drag the toggle handle to the "On" position')
def i_touch_and_drag_the_toggle_handle_to_the_on_position(context):
    pass


@step('I touch "Brightness"')
def i_touch_brightness(context):
    pass


@step('I touch "Call Forwarding"')
def i_touch_call_forwarding(context):
    pass


@step('I touch "Call Forwarding Options"')
def i_touch_call_forwarding_options(context):
    pass


@step('I touch "Check Ethernet"')
def i_touch_check_ethernet(context):
    pass


@step('I touch "Clear App Data/Cache"')
def i_touch_clear_app_datacache(context):
    pass


@step('I touch "Confirm"')
def i_touch_confirm(context):
    pass


@step('I touch "Date/Time Options"')
def i_touch_datetime_options(context):
    pass


@step('I touch "Default Contacts Tab"')
def i_touch_default_contacts_tab(context):
    pass


@step('I touch "eHelp"')
def i_touch_ehelp(context):
    pass


@step('I touch "Factory Reset"')
def i_touch_factory_reset(context):
    pass


@step('I touch "Manage Accounts"')
def i_touch_manage_accounts(context):
    pass


@step('I touch "Need Help"')
def i_touch_need_help(context):
    pass


@step('I touch "Next"')
def i_touch_next(context):
    pass


@when('I touch "OK" on the "Invalid VLAN Priority" alert')
def i_touch_ok_on_the_invalid_vlan_priority_alert(context):
    if 'fake' not in str(context._config.tags).split(','):
        network_view.click_named_element('InvalidVlanOk')


@step('I touch "OK" on the popup')
def i_touch_ok_on_the_popup(context):
    if 'fake' not in str(context._config.tags).split(','):
        base_view.click_named_element("OtaServerOk")


@step('I touch "Personal"')
def i_touch_personal(context):
    pass


@step('I touch "Phone"')
def i_touch_phone(context):
    pass


@step('I touch "Ringtones"')
def i_touch_ringtones(context):
    pass


@step('I touch "Screen Timeout"')
def i_touch_screen_timeout(context):
    pass


@step('I touch "Sign in with Google"')
def i_touch_sign_in_with_google(context):
    pass


@step('I touch "System"')
def i_touch_system(context):
    pass


@step("I touch the All tab")
def i_touch_the_all_tab(context):
    pass


@step("I touch the Back button")
def i_touch_the_back_button(context):
    if 'fake' not in str(context._config.tags).split(','):
        base_view.send_keycode('KEYCODE_BACK')


@step("I touch the button for another ringtone")
def i_touch_the_button_for_another_ringtone(context):
    pass


@step("I touch the button for another tab")
def i_touch_the_button_for_another_tab(context):
    pass


@step("I touch the button for another timer setting")
def i_touch_the_button_for_another_timer_setting(context):
    pass


@step('I touch the "Call Forward Busy" section')
def i_touch_the_call_forward_busy_section(context):
    pass


@step("I touch the Call Forward icon")
def i_touch_the_call_forward_icon(context):
    pass


@step('I touch the "Call Forward No Answer" section')
def i_touch_the_call_forward_no_answer_section(context):
    pass


@step('I touch the "Cancel" button')
def i_touch_the_cancel_button(context):
    pass


@step("I touch the contact listing I want to call")
def i_touch_the_contact_listing_i_want_to_call(context):
    pass


@step("I touch the current time zone text")
def i_touch_the_current_time_zone_text(context):
    pass


@step("I touch the Do Not Disturb icon")
def i_touch_the_do_not_disturb_icon(context):
    pass


@step("I touch the Missed tab")
def i_touch_the_missed_tab(context):
    pass


@when('I touch the "OK" button')
def i_touch_the_ok_button(context):
    pass


@step("I touch the Trash tab")
def i_touch_the_trash_tab(context):
    pass


@step('I touch the "Utilities" option')
def i_touch_the_utilities_option(context):
    pass


@step("I touch the voicemail icon")
def i_touch_the_voicemail_icon(context):
    pass


@step('I touch "Volume Control"')
def i_touch_volume_control(context):
    pass


@step('I touch "Walkthrough"')
def i_touch_walkthrough(context):
    pass


@step("I verify the system and app versions are current")
def i_verify_the_system_and_app_versions_are_current(context):
    if 'fake' not in str(context._config.tags).split(','):
        context.execute_steps(u"""
            Given I am logged in to the ePhone7
            When  [user] I touch the Preferences icon
            Then  [prefs] the Preferences window appears
            When  [prefs] I touch the "System" menu category
            And   [prefs] I touch the "About ePhone7" menu item
            Then  [prefs] I read the displayed versions for the app and AOSP
            When  [prefs] I touch the "X" icon
            Then  [prefs] the Preferences window disappears
            """)
    app_actual = context.app_version
    aosp_actual = context.aosp_version
    app_expect = context.config.userdata.get('current_app')
    aosp_expect = context.config.userdata.get('current_aosp')
    assert context.app_version == context.config.userdata.get('current_app'), "Expected app version %s, got %s" % (app_expect, app_actual)
    assert context.aosp_version == context.config.userdata.get('current_aosp'), "Expected aosp version %s, got %s" % (aosp_expect, aosp_actual)


@step("I wait for the phone to restart")
def i_wait_for_the_phone_to_restart(context):
    if 'fake' not in str(context._config.tags).split(','):
        base_view.close_appium()
        sleep(30)
        base_view.open_appium('nolaunch', force=True, timeout=60)
        base_view.startup()


@then("I wait for the phone to upgrade and reboot")
def i_wait_for_the_phone_to_upgrade_and_reboot(context):
    if 'fake' not in str(context._config.tags).split(','):
        # poll and do nothing while current activity is .OtaAppActivity
        # (this loop is expected continue while the new software is being downloaded;
        # it should end when the reboot begins, so that trying to read the current activity
        # via Appium raises an exception)
        while True:
            try:
                sleep(5)
                current_activity = base_view.driver.current_activity
                if current_activity != '.OtaAppActivity':
                    break
            except:
                base_view.close_appium()
                break
        # turn on USB access for adb and Appium via the spud port
        import os
        from ePhone7.utils.spud_serial import SpudSerial
        ip_addr = SpudSerial.get_my_ip_addr()
        actions = [
            {'cmd': '', 'new_cwd': '', 'expect': 'mtp_open', 'timeout': 600},
            {'cmd': 'cd /data/misc/adb\n', 'new_cwd': 'data/misc/adb'},
            {'cmd': 'alias tftp="busybox tftp"\n', 'new_cwd': None},
            {'cmd': 'tftp -g -r adbkey.pub -l adb_keys %s\n' % ip_addr, 'new_cwd': None},
            {'cmd': 'chown system adb_keys\n', 'new_cwd': None},
            {'cmd': 'chmod 640 adb_keys\n', 'new_cwd': None},
            {'cmd': 'cd /data/property\n', 'new_cwd': 'data/property'},
            {'cmd': 'echo -n mtp,adb > persist.sys.usb.config\n', 'new_cwd': None},
            {'cmd': 'reboot\n', 'new_cwd': '', 'expect': 'mtp_open', 'timeout': 120}
        ]
        # put the adb public key in the /tftpboot directory so the tftp action can upload it to the phone
        with open(os.path.join(os.getenv('HOME'), '.android', 'adbkey.pub')) as input_file:
            with open('/tftpboot/adbkey.pub', 'w') as output_file:
                key = input_file.read()
                output_file.write(key + '\n')
        ss = SpudSerial('/dev/ttyUSB0', pwd_check=False)
        for action in actions:
            ss.do_action(action)
        # at this point the reboot of Android should be complete with USB debug enabled, so we
        # call base_view.startup() to get the ePhone7 app into the right state
        base_view.open_appium('nolaunch', force=True, timeout=60)
        base_view.startup()


@step("my account does not have two-step verification enabled")
def my_account_does_not_have_twostep_verification_enabled(context):
    pass


@step("my Favorite contacts appear on the Coworkers contacts list")
def my_favorite_contacts_appear_on_the_coworkers_contacts_list(context):
    pass


@step("my new voicemails are listed")
def my_new_voicemails_are_listed(context):
    pass


@step("my phone calls back the caller")
def my_phone_calls_back_the_caller(context):
    pass


@step("my phone calls the number")
def my_phone_calls_the_number(context):
    pass


@step("my phone calls the voicemail sender")
def my_phone_calls_the_voicemail_sender(context):
    pass


@step("my saved voicemails are listed")
def my_saved_voicemails_are_listed(context):
    pass


@given("my system version needs to be upgraded")
def my_system_version_needs_to_be_upgraded(context):
    if 'fake' not in str(context._config.tags).split(','):
        context.execute_steps(u"""
            Given I am logged in to the ePhone7
            When  [user] I touch the Preferences icon
            Then  [prefs] the Preferences window appears
            When  [prefs] I touch the "System" menu category
            And   [prefs] I touch the "About ePhone7" menu item
            Then  [prefs] I read the displayed versions for the app and AOSP
            When  [prefs] I touch the "X" icon
            Then  [prefs] the Preferences window disappears
            """)
        need_aosp_downgrade = context.aosp_version != context.config.userdata.get('downgrade_aosp')
        need_app_downgrade = context.app_version != context.config.userdata.get('downgrade_app')
        if need_aosp_downgrade or need_app_downgrade:
            base_view.close_appium()
            if need_aosp_downgrade:
                base_view.force_aosp_downgrade(context.config.userdata.get('downgrade_aosp'))
            if need_app_downgrade:
                base_view.force_app_downgrade(context.config.userdata.get('downgrade_app'))
            base_view.open_appium('nolaunch', force=True, timeout=60)
            base_view.startup()
            context.execute_steps(u"""
                Given I am logged in to the ePhone7
                When  [user] I touch the Preferences icon
                Then  [prefs] the Preferences window appears
                When  [prefs] I touch the "System" menu category
                And   [prefs] I touch the "About ePhone7" menu item
                Then  [prefs] I read the displayed versions for the app and AOSP
                When  [prefs] I touch the "X" icon
                Then  [prefs] the Preferences window disappears
                """)


@step("Only the contact I touched is listed")
def only_the_contact_i_touched_is_listed(context):
    pass


@step("Only the current ringtone has a dot next to it")
def only_the_current_ringtone_has_a_dot_next_to_it(context):
    pass


@step("Only the new ringtone has a dot next to it")
def only_the_new_ringtone_has_a_dot_next_to_it(context):
    pass


@step("Someone calls me")
def someone_calls_me(context):
    pass


@step('the "Account Deleted" popup disappears')
def the_account_deleted_popup_disappears(context):
    pass


@step("the Advanced Options view disappears")
def the_advanced_options_view_disappears(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert user_view.element_is_not_present('AdvancedOptions'), "Expected Advanced Options view to disappear but it did not"


@step("the Call Forward icon is blue")
def the_call_forward_icon_is_blue(context):
    pass


@step("the Call Forward icon is red")
def the_call_forward_icon_is_red(context):
    pass


@step("the call has a blue handset icon with an incoming arrow")
def the_call_has_a_blue_handset_icon_with_an_incoming_arrow(context):
    pass


@step("the call has a green handset icon with an outgoing arrow")
def the_call_has_a_green_handset_icon_with_an_outgoing_arrow(context):
    pass


@step("the call has a red handset icon with a missed arrow")
def the_call_has_a_red_handset_icon_with_a_missed_arrow(context):
    pass


@step("the call has a voicemail icon")
def the_call_has_a_voicemail_icon(context):
    pass


@step("the Call Park icon")
def the_call_park_icon(context):
    pass


@step("the caller ends the call")
def the_caller_ends_the_call(context):
    pass


@step("the caller gets a voicemail prompt")
def the_caller_gets_a_voicemail_prompt(context):
    pass


@step("the caller is connected to my phone")
def the_caller_is_connected_to_my_phone(context):
    pass


@step("the caller leaves a message")
def the_caller_leaves_a_message(context):
    pass


@step("the caller leaves a voicemail")
def the_caller_leaves_a_voicemail(context):
    pass


@step("the Contacts tab window disappears")
def the_contacts_tab_window_disappears(context):
    pass


@step("the coworker contact answers the call")
def the_coworker_contact_answers_the_call(context):
    if 'fake' not in str(context._config.tags).split(','):
        context.softphone.account_info.call.answer(200)
        context.softphone.wait_for_call_status('call', user_view.call_status_wait)
    pass


@step("the current default tab is selected")
def the_current_default_tab_is_selected(context):
    pass


@step("the Current OTA Server popup appears")
def the_current_ota_server_popup_appears(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert(dial_view.element_is_present('CurrentOtaPopup'))


@step("the Current OTA Server popup disappears")
def the_current_ota_server_popup_disappears(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert(dial_view.element_is_not_present('CurrentOtaPopup'))


@step("the current time zone text is shown")
def the_current_time_zone_text_is_shown(context):
    pass


@step("the current timer setting is selected")
def the_current_timer_setting_is_selected(context):
    pass


@step("the Do Not Disturb icon is blue")
def the_do_not_disturb_icon_is_blue(context):
    pass


@step("the Do Not Disturb icon is red")
def the_do_not_disturb_icon_is_red(context):
    pass


@step("the Do Not Disturb icon turns blue")
def the_do_not_disturb_icon_turns_blue(context):
    pass


@step("the Do Not Disturb icon turns red")
def the_do_not_disturb_icon_turns_red(context):
    pass


@step("the Google dialog disappears")
def the_google_dialog_disappears(context):
    pass


@step("the in-call window appears")
def the_incall_window_appears(context):
    pass


@step("the in-call window disappears")
def the_incall_window_disappears(context):
    pass


@step("the incoming call window appears")
def the_incoming_call_window_appears(context):
    pass


@step("the incoming call window disappears")
def the_incoming_call_window_disappears(context):
    pass


@step("the keypad disappears")
def the_keypad_disappears(context):
    pass


@step("the login screen appears")
def the_login_screen_appears(context):
    pass


@step('the "Manage Accounts" element label changes to "Sign in with Google"')
def the_manage_accounts_element_label_changes_to_sign_in_with_google(context):
    pass


@step("the menu disappears")
def the_menu_disappears(context):
    pass


@step('the message "{message}" is shown')
def the_message_message_is_shown(context, message):
    if 'fake' not in str(context._config.tags).split(','):
        text = dial_view.find_named_element('OtaUpdatePopupContent').text
        assert text == message, "expected %s, got %s" % (message, text)


@step("the network settings are displayed")
def the_network_settings_are_displayed(context):
    pass


@step("the new default tab is selected")
def the_new_default_tab_is_selected(context):
    pass


@step("the new time zone text is shown")
def the_new_time_zone_text_is_shown(context):
    pass


@step("the new timer setting is selected")
def the_new_timer_setting_is_selected(context):
    pass


@step("the New Voicemail view appears")
def the_new_voicemail_view_appears(context):
    pass


@step('the "OTA Server Update" popup appears')
def the_ota_server_update_popup_appears(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert(dial_view.element_is_present('OtaUpdatePopup'))


@step('the "OTA Server Update" popup disappears')
def the_ota_server_update_popup_disappears(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert(dial_view.element_is_not_present('OtaUpdatePopup'))


@step("the popup disappears")
def the_popup_disappears(context):
    pass


@step("the popup does not show the current OTA URL")
def the_popup_does_not_show_the_current_ota_url(context):
    pass


@step("the popup shows the current OTA environment name")
def the_popup_shows_the_current_ota_environment_name(context):
    pass


@step("the position of the slider control changes")
def the_position_of_the_slider_control_changes(context):
    pass


@step("the Record button is gray")
def the_record_button_is_gray(context):
    if 'fake' not in str(context._config.tags).split(','):
        user_view.get_screenshot_as_png('record_button')
        expected_color = [115, 115, 115]
        actual_color = user_view.get_element_color('record_button', context.record_button)
        assert actual_color == expected_color, "expected color %s, got %s" % (expected_color, actual_color)


@step("the Record button is white")
def the_record_button_is_white(context):
    if 'fake' not in str(context._config.tags).split(','):
        user_view.get_screenshot_as_png('record_button')
        expected_color = [216, 216, 216]
        actual_color = user_view.get_element_color('record_button', context.record_button)
        assert actual_color == expected_color, "expected color %s, got %s" % (expected_color, actual_color)


@step('the "Ringtones" window disappears')
def the_ringtones_window_disappears(context):
    pass


@step('the section labeled "Call Forward Busy" is highlighted')
def the_section_labeled_call_forward_busy_is_highlighted(context):
    pass


@step('the section labeled "Call Forward Busy" is not highlighted')
def the_section_labeled_call_forward_busy_is_not_highlighted(context):
    pass


@step('the section labeled "Call Forward No Answer" is highlighted')
def the_section_labeled_call_forward_no_answer_is_highlighted(context):
    pass


@step('the section labeled "Call Forward No Answer" is not highlighted')
def the_section_labeled_call_forward_no_answer_is_not_highlighted(context):
    pass


@step('the "Sign in with Google" element label changes to "Manage Accounts"')
def the_sign_in_with_google_element_label_changes_to_manage_accounts(context):
    pass


@step('the "Sleep Timer Setting" window disappears')
def the_sleep_timer_setting_window_disappears(context):
    pass


@step('the toggle handle is in the "Off" position')
def the_toggle_handle_is_in_the_off_position(context):
    pass


@step('the toggle handle is in the "On" position')
def the_toggle_handle_is_in_the_on_position(context):
    pass


@step('the toggle handle stays in the "Off" position')
def the_toggle_handle_stays_in_the_off_position(context):
    pass


@step('the toggle handle stays in the "On" position')
def the_toggle_handle_stays_in_the_on_position(context):
    pass


@step("the VLAN Enable button is active")
def the_vlan_enable_button_is_active(context):
    pass


@step("the window contains a slider control")
def the_window_contains_a_slider_control(context):
    pass


@step("the window disappears")
def the_window_disappears(context):
    pass


@step("VLAN is enabled")
def vlan_is_enabled(context):
    pass


