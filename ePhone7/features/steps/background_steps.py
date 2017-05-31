from behave import *
from common_steps import *
from network_steps import *
from prefs_steps import *
from user_steps import *
from dial_steps import *
from history_steps import *
from advanced_steps import *


@then('[background] A submenu appears with a "Network" option')
@fake
def background__a_submenu_appears_with_a_network_option(context):
    prefs__a_submenu_appears_with_a_network_option(context)


@given("[background] I am logged in to the ePhone7")
@fake
def background__i_am_logged_in_to_the_ephone7(context):
    i_am_logged_in_to_the_ephone7(context)


@then("[background] I close all open submenus")
@fake
def background__i_close_all_open_submenus(context):
    i_close_all_open_submenus(context)


@when("[background] I dial the {codename} direct code")
@fake
def background__i_dial_the_codename_direct_code(context, codename):
    dial__i_dial_the_codename_direct_code(context, codename)


@when("[background] I enter a VLAN identifier between 1 and 4094")
@fake
def background__i_enter_a_vlan_identifier_between_1_and_4094(context):
    i_enter_a_vlan_identifier_between_1_and_4094(context)


@step("[background] I enter a VLAN priority between 0 and 7")
@fake
def background__i_enter_a_vlan_priority_between_0_and_7(context):
    network__i_enter_a_vlan_priority_between_0_and_7(context)


@when("[background] I scroll down to the Call Record Enable setting")
@fake
def background__i_scroll_down_to_the_call_record_enable_setting(context):
    advanced__i_scroll_down_to_the_call_record_enable_setting(context)


@then("[background] I see the All and Missed tabs at the top of the screen")
@fake
def background__i_see_the_all_and_missed_tabs_at_the_top_of_the_screen(context):
    history__i_see_the_all_and_missed_tabs_at_the_top_of_the_screen(context)


@step("[background] I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen")
@fake
def background__i_see_the_contacts_history_voicemail_and_dial_buttons_at_the_bottom_of_the_screen(context):
    user__i_see_the_contacts_history_voicemail_and_dial_buttons_at_the_bottom_of_the_screen(context)


@step("[background] I see the Need Help, Personal, Phone and System category elements")
@fake
def background__i_see_the_need_help_personal_phone_and_system_category_elements(context):
    prefs__i_see_the_need_help_personal_phone_and_system_category_elements(context)


@then("[background] I see the Network Settings view")
@fake
def background__i_see_the_network_settings_view(context):
    network__i_see_the_network_settings_view(context)


@step('[background] I touch "Save and Reboot"')
@fake
def background__i_touch_save_and_reboot(context):
    network__i_touch_save_and_reboot(context)


@step("[background] I touch the call button")
@fake
def background__i_touch_the_call_button(context):
    dial__i_touch_the_call_button(context)


@when("[background] I touch the Dial button")
@fake
def background__i_touch_the_dial_button(context):
    user__i_touch_the_dial_button(context)


@when("[background] I touch the History button")
@fake
def background__i_touch_the_history_button(context):
    user__i_touch_the_history_button(context)


@when('[background] I touch the "{name}" menu category')
@fake
def background__i_touch_the_name_menu_category(context, name):
    prefs__i_touch_the_name_menu_category(context, name)


@when('[background] I touch the "Network" option')
@fake
def background__i_touch_the_network_option(context):
    prefs__i_touch_the_network_option(context)


@when("[background] I touch the Preferences icon")
@fake
def background__i_touch_the_preferences_icon(context):
    user__i_touch_the_preferences_icon(context)


@step("[background] I touch the VLAN Enable button")
@fake
def background__i_touch_the_vlan_enable_button(context):
    network__i_touch_the_vlan_enable_button(context)


@step("[background] I wait for the phone to restart")
@fake
def background__i_wait_for_the_phone_to_restart(context):
    i_wait_for_the_phone_to_restart(context)


@then("[background] the Advanced Options view appears")
@fake
def background__the_advanced_options_view_appears(context):
    advanced__the_advanced_options_view_appears(context)


@then("[background] the Dial view appears")
@fake
def background__the_dial_view_appears(context):
    dial__the_dial_view_appears(context)


@step("[background] the Disable button is inactive")
@fake
def background__the_disable_button_is_inactive(context):
    network__the_disable_button_is_inactive(context)


@step("[background] the Enable button is active")
@fake
def background__the_enable_button_is_active(context):
    network__the_enable_button_is_active(context)


@then("[background] the Preferences window appears")
@fake
def background__the_preferences_window_appears(context):
    prefs__the_preferences_window_appears(context)


@then("[background] The reboot alert window appears")
@fake
def background__the_reboot_alert_window_appears(context):
    network__the_reboot_alert_window_appears(context)


