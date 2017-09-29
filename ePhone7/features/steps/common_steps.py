from behave import *
from ePhone7.views import *
from time import sleep, time
from prefs_steps import *
from advanced_steps import *
from lib.user_exception import UserException as Ux, UserFailException as Fx
from ePhone7.utils.get_softphone import get_softphone
from ePhone7.utils.versions import *
from lib.wrappers import fake


@step("A call between two other accounts has been parked by the called account")
@fake
def a_call_between_two_other_accounts_has_been_parked_by_the_called_account(context):
    pass


@step('A "Call History" window appears')
@fake
def a_call_history_window_appears(context):
    pass


@step('A "Clear All User Data" confirmation dialog appears')
@fake
def a_clear_all_user_data_confirmation_dialog_appears(context):
    pass


@step("A confirmation dialog appears")
@fake
def a_confirmation_dialog_appears(context):
    pass


@step('A "Contact Management" window appears')
@fake
def a_contact_management_window_appears(context):
    pass


@step('A "Dialpad Screen" window appears')
@fake
def a_dialpad_screen_window_appears(context):
    pass


@step('A "Factory Reset" confirmation dialog appears')
@fake
def a_factory_reset_confirmation_dialog_appears(context):
    pass


@step("A Google dialog appears with a place to enter my email address")
@fake
def a_google_dialog_appears_with_a_place_to_enter_my_email_address(context):
    pass


@step("A Google dialog appears with a place to enter my password")
@fake
def a_google_dialog_appears_with_a_place_to_enter_my_password(context):
    pass


@step("A menu appears with time zone choices")
@fake
def a_menu_appears_with_time_zone_choices(context):
    pass


@step('A menu with a "Clear App Data/Cache" option appears')
@fake
def a_menu_with_a_clear_app_datacache_option_appears(context):
    pass


@step('A menu with a "Factory Reset" option appears')
@fake
def a_menu_with_a_factory_reset_option_appears(context):
    pass


@step("A message indicates that calls are being forwarded to the contact")
@fake
def a_message_indicates_that_calls_are_being_forwarded_to_the_contact(context):
    pass


@step("A message indicates that calls are being forwarded to voicemail")
@fake
def a_message_indicates_that_calls_are_being_forwarded_to_voicemail(context):
    pass


@step('A "Select Ringtone" window appears with options for various ringtones')
@fake
def a_select_ringtone_window_appears_with_options_for_various_ringtones(context):
    pass


@step('A "Sign Out of Google Account" dialog appears')
@fake
def a_sign_out_of_google_account_dialog_appears(context):
    pass


@step('A "Sleep Timer Setting" window appears with buttons for various timer settings')
@fake
def a_sleep_timer_setting_window_appears_with_buttons_for_various_timer_settings(context):
    pass


@step('A submenu appears with a "Brightness" option')
@fake
def a_submenu_appears_with_a_brightness_option(context):
    pass


@step('A submenu appears with a "Date/Time Options" option')
@fake
def a_submenu_appears_with_a_datetime_options_option(context):
    pass


@step('A submenu appears with a "Default Contacts Tab" option')
@fake
def a_submenu_appears_with_a_default_contacts_tab_option(context):
    pass


@step('A submenu appears with a "Manage Accounts" option')
@fake
def a_submenu_appears_with_a_manage_accounts_option(context):
    pass


@step('A submenu appears with a "Ringtones" option')
@fake
def a_submenu_appears_with_a_ringtones_option(context):
    pass


@step('A submenu appears with a "Screen Timeout" option')
@fake
def a_submenu_appears_with_a_screen_timeout_option(context):
    pass


@step('A submenu appears with a "Sign in with Google" option')
@fake
def a_submenu_appears_with_a_sign_in_with_google_option(context):
    pass


@step('A submenu appears with a "Utilities" option')
@fake
def a_submenu_appears_with_a_utilities_option(context):
    pass


@step('A submenu appears with a "Volume Control" option')
@fake
def a_submenu_appears_with_a_volume_control_option(context):
    pass


@step('A submenu opens with a "Walkthrough" option')
@fake
def a_submenu_opens_with_a_walkthrough_option(context):
    pass


@step('A "Visual Voicemail" window appears')
@fake
def a_visual_voicemail_window_appears(context):
    pass


@step('A "Voicemail Playback" window appears')
@fake
def a_voicemail_playback_window_appears(context):
    pass


@step('A "Welcome to ePhone7!" window appears')
@fake
def a_welcome_to_ephone7_window_appears(context):
    pass


@step("A window appears with a button for each Contacts tab")
@fake
def a_window_appears_with_a_button_for_each_contacts_tab(context):
    pass


@step('A window appears with a "Check Ethernet" option')
@fake
def a_window_appears_with_a_check_ethernet_option(context):
    pass


@step('A window appears with a section labeled "Call Forward No Answer"')
@fake
def a_window_appears_with_a_section_labeled_call_forward_no_answer(context):
    pass


@step('A window appears with the label "Screen Brightness" appears')
@fake
def a_window_appears_with_the_label_screen_brightness_appears(context):
    pass


@step('A window with a "24-hour Format" toggle appears')
@fake
def a_window_with_a_24hour_format_toggle_appears(context):
    pass


@step('A window with a "Change Timezone" option appears')
@fake
def a_window_with_a_change_timezone_option_appears(context):
    pass


@step('A window with a "Media Volume" slider appears')
@fake
def a_window_with_a_media_volume_slider_appears(context):
    pass


@step('A window with a "Ringer Volume" slider appears')
@fake
def a_window_with_a_ringer_volume_slider_appears(context):
    pass


@step('A window with a "Touch Sounds" toggle appears')
@fake
def a_window_with_a_touch_sounds_toggle_appears(context):
    pass


@step('A window with a "Voice Call" slider appears')
@fake
def a_window_with_a_voice_call_slider_appears(context):
    pass


@step('An "Account Deleted" popup appears')
@fake
def an_account_deleted_popup_appears(context):
    pass


@step('an "Active Call Dialpad" window appears')
@fake
def an_active_call_dialpad_window_appears(context):
    pass


@step('an "Active Call Screen" window appears')
@fake
def an_active_call_screen_window_appears(context):
    base_view.find_named_element('ActiveCallScreen')


@step("Both windows disappear")
@fake
def both_windows_disappear(context):
    pass


@step("I add a my favorite Coworker contacts to my Favorites list")
@fake
def i_add_a_my_favorite_coworker_contacts_to_my_favorites_list(context):
    context.run_substep("I touch the \"Contacts\" button")
    context.run_substep("I touch the \"Coworkers\" tab")
    context.run_substep("[contacts] my Coworker contacts are shown on the display")
    context.run_substep("[contacts] I long-press a contact list item")
    context.run_substep("[contacts] An \"Add Multiple Favorites\" confirmation dialog appears")
    context.run_substep("I touch \"OK\"")
    context.run_substep("[contacts] my Coworker contacts are each shown with a Favorites star icon")
    context.run_substep("[contacts] I touch the star icons so Favorites are yellow and others are white")
    context.run_substep("[contacts] I long-press a contact list item")
    context.run_substep("[contacts] my Coworker contacts are each shown with a handset icon")


@step("I am at the home screen")
@fake
def i_am_at_the_home_screen(context):
    assert user_view.element_is_present('UserHeaderName', 10), 'UserHeaderName element not present'
    assert user_view.element_is_present('HomeScreenLogo', 10), 'HomeScreenLogo element not present'


@step("I am not signed in to my gmail account")
@fake
def i_am_not_signed_in_to_my_gmail_account(context):
    pass


@step("I am signed in to my gmail account")
@fake
def i_am_signed_in_to_my_gmail_account(context):
    pass


@step("I answer the call")
@fake
def i_answer_the_call(context):
    user_view.click_named_element('IncomingCallAnswerToSpeaker')
    user_view.softphones[context.caller_name].wait_for_call_status('call', user_view.call_status_wait)


@step("I can see my personal contacts")
@fake
def i_can_see_my_personal_contacts(context):
    pass


@step("I downgrade my aosp to {downgrade_aosp_version}")
@fake
def i_downgrade_my_aosp_to_downgradeaospversion(context, downgrade_aosp_version):
    installed_aosp, installed_app = get_installed_versions()
    context.installed_aosp = installed_aosp
    if installed_aosp != downgrade_aosp_version:
        get_downgrade_images(downgrade_aosp_version)
        base_view.close_appium()
        force_aosp_downgrade(downgrade_aosp_version)
        installed_aosp, installed_app= get_installed_versions()
        assert installed_aosp == downgrade_aosp_version
        context.installed_aosp = installed_aosp
        base_view.open_appium()
        base_view.startup()


@step("I downgrade my app")
@fake
def i_downgrade_my_app(context):
    if context.needs_app_downgrade:
        base_view.close_appium()
        force_app_downgrade(context.config.userdata['downgrade_app'])
        base_view.open_appium('nolaunch', force=True, timeout=60)
        base_view.startup()


@step("I enter my email address")
@fake
def i_enter_my_email_address(context):
    pass


@step("I enter my password")
@fake
def i_enter_my_password(context):
    pass


@step("I enter part of a Coworker contact name using the keypad")
@fake
def i_enter_part_of_a_coworker_contact_name_using_the_keypad(context):
    pass


@step("I enter part of a Personal contact name using the keypad")
@fake
def i_enter_part_of_a_personal_contact_name_using_the_keypad(context):
    pass


@step("I enter part of a Personal contact number using the keypad")
@fake
def i_enter_part_of_a_personal_contact_number_using_the_keypad(context):
    pass


@step("I go to the Contacts view")
@fake
def i_go_to_the_contacts_view(context):
    user_view.goto_tab('Contacts')


@step("I go to the home screen")
@fake
def i_go_to_the_home_screen(context):
    context.run_substep("I touch the Home icon")
    context.run_substep("I am at the home screen")


@step("I go to the New Voicemail view")
@fake
def i_go_to_the_new_voicemail_view(context):
    contacts_view.goto_tab('Personal')


@step("I go to the Saved Voicemail view")
@fake
def i_go_to_the_saved_voicemail_view(context):
    contacts_view.goto_tab('Personal')


@step("I have at least one new voicemail")
@fake
def i_have_at_least_one_new_voicemail(context):
    pass


@step("I have at least one saved voicemail")
@fake
def i_have_at_least_one_saved_voicemail(context):
    pass


@step("I ignore the call")
@fake
def i_ignore_the_call(context):
    pass


@step("I perform an OTA upgrade")
@fake
def i_perform_an_ota_upgrade(context):
    context.run_substep('I set the OTA server')
    context.run_substep('[user] I touch the Preferences icon')
    context.run_substep('[prefs] the Preferences window appears')
    context.run_substep('I touch the "System" menu category')
    context.run_substep('I touch the "Updates" menu item')
    context.run_substep('I wait for the phone to upgrade and reboot')
    context.run_substep('the current versions are installed')


@step("I receive a call")
@fake
def i_receive_a_call(context):
    # use DefaultSoftphoneUser to call the ePhone7
    context.caller_name, src_cfg = user_view.receive_call(wait_timeout=10)


@step("I receive a new voicemail")
@fake
def i_receive_a_new_voicemail(context):
    pass


@step("I receive and ignore a call")
@fake
def i_receive_and_ignore_a_call(context):
    context.run_substep("I receive a call")
    context.run_substep("the incoming call window appears")
    context.run_substep("I ignore the call")
    context.run_substep("the caller ends the call")
    context.run_substep("the incoming call window disappears")


@step("I receive and ignore a call and the caller leaves a voicemail")
@fake
def i_receive_and_ignore_a_call_and_the_caller_leaves_a_voicemail(context):
    context.run_substep("I receive a call")
    context.run_substep("the incoming call window appears")
    context.run_substep("I ignore the call")
    context.run_substep("the caller leaves a voicemail")
    context.run_substep("the incoming call window disappears")
    context.run_substep("the caller ends the call")


@step('I see an "Invalid VLAN Priority" alert')
@fake
def i_see_an_invalid_vlan_priority_alert(context):
    assert network_view.element_is_present('InvalidVlanPriority'), "Expected Invalid VLAN Priority alert"


@step("I see the call at the top of the Missed History view")
@fake
def i_see_the_call_at_the_top_of_the_missed_history_view(context):
    pass


@step("I set the OTA server")
@fake
def i_set_the_ota_server(context):
    user_view.goto_tab("Dial")
    ota_server = context.config.userdata.get('ota_server')
    if ota_server.lower() == 'alpha':
        dial_view.dial_set_alpha_ota_server(context.installed_aosp)
    elif ota_server.lower() == 'beta':
        dial_view.dial_set_beta_ota_server()
    elif ota_server.lower().startswith('prod'):
        dial_view.dial_set_production_ota_server()
    else:
        raise Ux("%s is not a valid server name" % ota_server)
    dial_view.touch_call_button()
    sleep(0.5)
    dial_view.send_keycode_back()


@step("I swipe down twice")
@fake
def i_swipe_down_twice(context):
    pass


@step("I swipe the screen from right to left")
@fake
def i_swipe_the_screen_from_right_to_left(context):
    pass


@step("I touch a new time zone choice")
@fake
def i_touch_a_new_time_zone_choice(context):
    pass


@step("I touch and drag the slider control handle")
@fake
def i_touch_and_drag_the_slider_control_handle(context):
    pass


@step('I touch "Brightness"')
@fake
def i_touch_brightness(context):
    pass


@step('I touch "Call Forwarding"')
@fake
def i_touch_call_forwarding(context):
    pass


@step('I touch "Check Ethernet"')
@fake
def i_touch_check_ethernet(context):
    pass


@step('I touch "Clear App Data/Cache"')
@fake
def i_touch_clear_app_datacache(context):
    pass


@step('I touch "Confirm"')
@fake
def i_touch_confirm(context):
    pass


@step('I touch "Date/Time Options"')
@fake
def i_touch_datetime_options(context):
    pass


@step('I touch "Default Contacts Tab"')
@fake
def i_touch_default_contacts_tab(context):
    pass


@step('I touch "Manage Accounts"')
@fake
def i_touch_manage_accounts(context):
    pass


@step('I touch "Next"')
@fake
def i_touch_next(context):
    pass


@step("I touch the Back button")
@fake
def i_touch_the_back_button(context):
    base_view.send_keycode_back()


@step("I touch the Back icon")
@fake
def i_touch_the_back_icon(context):
    base_view.send_keycode_back()


@step("I touch the button for another ringtone")
@fake
def i_touch_the_button_for_another_ringtone(context):
    pass


@step("I touch the button for another tab")
@fake
def i_touch_the_button_for_another_tab(context):
    pass


@step("I touch the button for another timer setting")
@fake
def i_touch_the_button_for_another_timer_setting(context):
    pass


@step('I touch the "Call Forward No Answer" section')
@fake
def i_touch_the_call_forward_no_answer_section(context):
    pass


@step('I touch the "Cancel" button')
@fake
def i_touch_the_cancel_button(context):
    pass


@step("I touch the current time zone text")
@fake
def i_touch_the_current_time_zone_text(context):
    pass


@step("I touch the Home icon")
@fake
def i_touch_the_home_icon(context):
    base_view.send_keycode_home()


@step("I touch the voicemail icon")
@fake
def i_touch_the_voicemail_icon(context):
    pass


@step("I upgrade the phone if the versions are not correct")
@fake
def i_upgrade_the_phone_if_the_versions_are_not_correct(context):
    if 'fake' not in str(context._config.tags).split(','):
        current_aosp, current_app = get_current_versions(context.config.userdata['ota_server'])
        installed_aosp, installed_app = get_installed_versions()
        context.installed_aosp = installed_aosp
        log.debug("installed versions: app %s, aosp %s" % (installed_app, installed_aosp))
        log.debug("required versions: app %s, aosp %s" % (current_app, current_aosp))
        aosp_upgrade_required = current_aosp != installed_aosp
    else:
        aosp_upgrade_required = True
    if aosp_upgrade_required:
        log.debug("checking for updates")
        context.run_substep('I perform an OTA upgrade')


@step("I use the spud serial interface to list the installed packages")
@fake
def i_use_the_spud_serial_interface_to_list_the_installed_packages(context):
    pass


@step("I wait for the phone to restart")
@fake
def i_wait_for_the_phone_to_restart(context):
    base_view.close_appium_until_reboot()
    base_view.startup()


@step("I wait for the phone to upgrade and reboot")
@fake
def i_wait_for_the_phone_to_upgrade_and_reboot(context):
    # start_time = time()
    # timeout = 20
    # current_activity = None
    # while time() - start_time < timeout:
    #     current_activity = base_view.driver.current_activity
    #     log.debug('waiting for upgrade and reboot: current activity is %s' % current_activity)
    #     if current_activity == '.OTAAppActivity':
    #         break
    # else:
    #     raise Ux('current_activity %s after %s seconds, expected .OTAAppActivity' % (current_activity, timeout))
    base_view.close_appium_until_reboot()
    base_view.startup()


@step("my account does not have two-step verification enabled")
@fake
def my_account_does_not_have_twostep_verification_enabled(context):
    pass


@step("my Favorite contacts appear on the Coworkers contacts list")
@fake
def my_favorite_contacts_appear_on_the_coworkers_contacts_list(context):
    pass


@step("my new voicemails are listed")
@fake
def my_new_voicemails_are_listed(context):
    pass


@step("my phone calls back the caller")
@fake
def my_phone_calls_back_the_caller(context):
    pass


@step("my phone calls the number")
@fake
def my_phone_calls_the_number(context):
    pass


@step("my phone calls the voicemail sender")
@fake
def my_phone_calls_the_voicemail_sender(context):
    pass


@step("my saved voicemails are listed")
@fake
def my_saved_voicemails_are_listed(context):
    pass


@step("Only the current ringtone has a dot next to it")
@fake
def only_the_current_ringtone_has_a_dot_next_to_it(context):
    pass


@step("Only the new ringtone has a dot next to it")
@fake
def only_the_new_ringtone_has_a_dot_next_to_it(context):
    pass


@step("Someone calls me")
@fake
def someone_calls_me(context):
    pass


@step('the "Account Deleted" popup disappears')
@fake
def the_account_deleted_popup_disappears(context):
    pass


@step("the Advanced Options view disappears")
@fake
def the_advanced_options_view_disappears(context):
    assert advanced_settings_view.element_is_not_present('AdvancedOptions'), \
        "Expected Advanced Options view to disappear but it did not"


@step("the call has a red handset icon with a missed arrow")
@fake
def the_call_has_a_red_handset_icon_with_a_missed_arrow(context):
    pass


@step("the call has a voicemail icon")
@fake
def the_call_has_a_voicemail_icon(context):
    pass


@step("the caller ends the call")
@fake
def the_caller_ends_the_call(context):
    user_view.softphones[context.caller_name].end_call()


@step("the caller gets a voicemail prompt")
@fake
def the_caller_gets_a_voicemail_prompt(context):
    pass


@step("the caller is connected to my phone")
@fake
def the_caller_is_connected_to_my_phone(context):
    pass


@step("the caller leaves a message")
@fake
def the_caller_leaves_a_message(context):
    pass


@step("the caller leaves a voicemail")
@fake
def the_caller_leaves_a_voicemail(context):
    pass


@step("the Contacts tab window disappears")
@fake
def the_contacts_tab_window_disappears(context):
    pass


@step("the coworker contact answers the call")
@fake
def the_coworker_contact_answers_the_call(context):
    context.softphone.account_info.call.answer(200)
    context.softphone.wait_for_call_status('call', user_view.call_status_wait)


@step("the current default tab is selected")
@fake
def the_current_default_tab_is_selected(context):
    pass


@step("the Current OTA Server popup appears")
@fake
def the_current_ota_server_popup_appears(context):
    assert(dial_view.element_is_present('CurrentOtaPopup'))


@step("the Current OTA Server popup disappears")
@fake
def the_current_ota_server_popup_disappears(context):
    assert(dial_view.element_is_not_present('CurrentOtaPopup'))


@step("the current time zone text is shown")
@fake
def the_current_time_zone_text_is_shown(context):
    pass


@step("the current timer setting is selected")
@fake
def the_current_timer_setting_is_selected(context):
    pass


@step("the current versions are installed")
@fake
def the_current_versions_are_installed(context):
    current_aosp, current_app = get_current_versions(context.config.userdata['ota_server'])
    installed_aosp, installed_app = get_installed_versions()
    context.installed_aosp = installed_aosp
    assert installed_aosp == current_aosp, "Expected installed aosp version %s, got %s" % (current_aosp, installed_aosp)
    assert installed_app == current_app, "Expected installed app version %s, got %s" % (current_app, installed_app)


@step("the ePhone7 and softphone simultaneously receive a call")
@fake
def the_ephone7_and_softphone_simultaneously_receive_a_call(context):
    try:
        # use DefaultSoftphoneUser to call the ePhone7
        # wait a second to make sure the system knows it is online
        sleep(1)
        context.caller_name, src_cfg = user_view.receive_call(wait_for_status='call', wait_timeout=10)
    except Ux as e:
        context.call_answered = False
        log.warn("UserException: %s" % e)
        raise e
    else:
        context.call_answered = True


@step("the ePhone7 app should not crash")
@fake
def the_ephone7_app_should_not_crash(context):
    sleep(5)
    try:
        activity = base_view.driver.current_activity
    except:
        assert False, "could not read current activity"
    assert activity == '.activities.MainViewActivity', 'Expected .activities.MainViewActivity, got %s' % activity


@step("the Google dialog disappears")
@fake
def the_google_dialog_disappears(context):
    pass


@step("the in-call window appears")
@fake
def the_incall_window_appears(context):
    pass


@step("the in-call window disappears")
@fake
def the_incall_window_disappears(context):
    pass


@step("the incoming call window appears")
@fake
def the_incoming_call_window_appears(context):
    pass


@step("the incoming call window disappears")
@fake
def the_incoming_call_window_disappears(context):
    pass


@step("the installed aosp is not the downgrade version")
@fake
def the_installed_aosp_is_not_the_downgrade_version(context):
    downgrade_aosp = context.config.userdata['downgrade_aosp']
    installed_aosp = context.config.userdata['installed_aosp']
    context.needs_aosp_downgrade = installed_aosp != downgrade_aosp


@step("the installed app is not the downgrade version")
@fake
def the_installed_app_is_not_the_downgrade_version(context):
    downgrade_app = context.config.userdata['downgrade_app']
    installed_app = context.config.userdata['installed_app']
    context.needs_app_downgrade = installed_app != downgrade_app


@step("the login screen appears")
@fake
def the_login_screen_appears(context):
    pass


@step('the "Manage Accounts" element label changes to "Sign in with Google"')
@fake
def the_manage_accounts_element_label_changes_to_sign_in_with_google(context):
    pass


@step("the menu disappears")
@fake
def the_menu_disappears(context):
    pass


@step('the message "{message}" is shown')
@fake
def the_message_message_is_shown(context, message):
    text = dial_view.find_named_element('OtaUpdatePopupContent').text
    assert text == message, "expected %s, got %s" % (message, text)


@step("the network settings are displayed")
@fake
def the_network_settings_are_displayed(context):
    pass


@step("the new default tab is selected")
@fake
def the_new_default_tab_is_selected(context):
    pass


@step("the new time zone text is shown")
@fake
def the_new_time_zone_text_is_shown(context):
    pass


@step("the new timer setting is selected")
@fake
def the_new_timer_setting_is_selected(context):
    pass


@step("the New Voicemail view appears")
@fake
def the_new_voicemail_view_appears(context):
    pass


@step('the "OTA Server Update" popup appears')
@fake
def the_ota_server_update_popup_appears(context):
    assert(dial_view.element_is_present('OtaUpdatePopup'))


@step('the "OTA Server Update" popup disappears')
@fake
def the_ota_server_update_popup_disappears(context):
    assert(dial_view.element_is_not_present('OtaUpdatePopup'))


@step("The package com.android.wallpaper.livepicker is not listed")
@fake
def the_package_com_android_wallpaper_livepicker_is_not_listed(context):
    pass


@step("the phone restarts without a register retry message")
@fake
def the_phone_restarts_without_a_register_retry_message(context):
    base_view.close_appium()
    sleep(30)
    base_view.open_appium('nolaunch', force=True, timeout=60)
    try:
        base_view.startup(allow_reg_retry=False)
    except Fx as e:
        assert False, e.msg


@step("the popup disappears")
@fake
def the_popup_disappears(context):
    pass


@step("the popup does not show the current OTA URL")
@fake
def the_popup_does_not_show_the_current_ota_url(context):
    pass


@step("the popup shows the current OTA environment name")
@fake
def the_popup_shows_the_current_ota_environment_name(context):
    pass


@step("the position of the slider control changes")
@fake
def the_position_of_the_slider_control_changes(context):
    pass


@step('the "Ringtones" window disappears')
@fake
def the_ringtones_window_disappears(context):
    pass


@step('the section labeled "Call Forward Busy" is highlighted')
@fake
def the_section_labeled_call_forward_busy_is_highlighted(context):
    pass


@step('the section labeled "Call Forward Busy" is not highlighted')
@fake
def the_section_labeled_call_forward_busy_is_not_highlighted(context):
    pass


@step('the section labeled "Call Forward No Answer" is highlighted')
@fake
def the_section_labeled_call_forward_no_answer_is_highlighted(context):
    pass


@step('the section labeled "Call Forward No Answer" is not highlighted')
@fake
def the_section_labeled_call_forward_no_answer_is_not_highlighted(context):
    pass


@step('the "Sign in with Google" element label changes to "Manage Accounts"')
@fake
def the_sign_in_with_google_element_label_changes_to_manage_accounts(context):
    pass


@step('the "Sleep Timer Setting" window disappears')
@fake
def the_sleep_timer_setting_window_disappears(context):
    pass


@step("the softphone answers the call")
@fake
def the_softphone_answers_the_call(context):
    assert context.call_answered is True


@step("the softphone is set to autoanswer")
@fake
def the_softphone_is_set_to_autoanswer(context):
    context.softphone_alt.set_incoming_response(200)


@step('the toggle handle is in the "Off" position')
@fake
def the_toggle_handle_is_in_the_off_position(context):
    pass


@step('the toggle handle is in the "On" position')
@fake
def the_toggle_handle_is_in_the_on_position(context):
    pass


@step('the toggle handle stays in the "Off" position')
@fake
def the_toggle_handle_stays_in_the_off_position(context):
    pass


@step('the toggle handle stays in the "On" position')
@fake
def the_toggle_handle_stays_in_the_on_position(context):
    pass


@step("the VLAN Enable button is active")
@fake
def the_vlan_enable_button_is_active(context):
    pass


@step("the window contains a slider control")
@fake
def the_window_contains_a_slider_control(context):
    pass


@step("the window disappears")
@fake
def the_window_disappears(context):
    pass


@step("there is a softphone registered on my ePhone7's user account")
@fake
def there_is_a_softphone_registered_on_my_ephone7s_user_account(context):
    context.softphone_alt = get_softphone('R2d2AltUser')


@step("VLAN is enabled")
@fake
def vlan_is_enabled(context):
    pass


