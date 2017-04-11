from behave import *
from common_steps import *
from network import *


@then('[background] A submenu appears with a "Network" option')
def background_a_submenu_appears_with_a_network_option(context):
    if 'fake' not in str(context._config.tags).split(','):
        a_submenu_appears_with_a_network_option(context)


@given("[background] I am logged in to the ePhone7")
def background_i_am_logged_in_to_the_ephone7(context):
    if 'fake' not in str(context._config.tags).split(','):
        i_am_logged_in_to_the_ephone7(context)


@then("[background] I close all open submenus")
def background_i_close_all_open_submenus(context):
    if 'fake' not in str(context._config.tags).split(','):
        i_close_all_open_submenus(context)


@when("[background] I enter a VLAN identifier between 1 and 4094")
def background_i_enter_a_vlan_identifier_between_1_and_4094(context):
    if 'fake' not in str(context._config.tags).split(','):
        i_enter_a_vlan_identifier_between_1_and_4094(context)


@step("[background] I enter a VLAN priority between 0 and 7")
def background_i_enter_a_vlan_priority_between_0_and_7(context):
    if 'fake' not in str(context._config.tags).split(','):
        network_i_enter_a_vlan_priority_between_0_and_7(context)


@then("[background] I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen")
def background_i_see_the_contacts_history_voicemail_and_dial_buttons_at_the_bottom_of_the_screen(context):
    if 'fake' not in str(context._config.tags).split(','):
        i_see_the_contacts_history_voicemail_and_dial_buttons_at_the_bottom_of_the_screen(context)


@step("[background] I see the Need Help, Personal, Phone and System category elements")
def background_i_see_the_need_help_personal_phone_and_system_category_elements(context):
    if 'fake' not in str(context._config.tags).split(','):
        i_see_the_need_help_personal_phone_and_system_category_elements(context)


@then("[background] I see the Network Settings view")
def background_i_see_the_network_settings_view(context):
    if 'fake' not in str(context._config.tags).split(','):
        network_i_see_the_network_settings_view(context)


@step('[background] I touch "Save and Reboot"')
def background_i_touch_save_and_reboot(context):
    if 'fake' not in str(context._config.tags).split(','):
        network_i_touch_save_and_reboot(context)


@when("[background] I touch the Dial button")
def background_i_touch_the_dial_button(context):
    if 'fake' not in str(context._config.tags).split(','):
        i_touch_the_dial_button(context)


@when('[background] I touch the "Network" option')
def background_i_touch_the_network_option(context):
    if 'fake' not in str(context._config.tags).split(','):
        i_touch_the_network_option(context)


@when("[background] I touch the Preferences icon")
def background_i_touch_the_preferences_icon(context):
    if 'fake' not in str(context._config.tags).split(','):
        i_touch_the_preferences_icon(context)


@when('[background] I touch the "System" menu category')
def background_i_touch_the_system_menu_category(context):
    if 'fake' not in str(context._config.tags).split(','):
        i_touch_the_system_menu_category(context)


@step("[background] I touch the VLAN Enable button")
def background_i_touch_the_vlan_enable_button(context):
    if 'fake' not in str(context._config.tags).split(','):
        i_touch_the_vlan_enable_button(context)


@step("[background] I wait for the phone to restart")
def background_i_wait_for_the_phone_to_restart(context):
    if 'fake' not in str(context._config.tags).split(','):
        i_wait_for_the_phone_to_restart(context)


@then("[background] the Dial view appears")
def background_the_dial_view_appears(context):
    if 'fake' not in str(context._config.tags).split(','):
        the_dial_view_appears(context)


@step("[background] the Disable button is inactive")
def background_the_disable_button_is_inactive(context):
    if 'fake' not in str(context._config.tags).split(','):
        network_the_disable_button_is_inactive(context)


@step("[background] the Enable button is active")
def background_the_enable_button_is_active(context):
    if 'fake' not in str(context._config.tags).split(','):
        network_the_enable_button_is_active(context)


@then("[background] the Preferences window appears")
def background_the_preferences_window_appears(context):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_the_preferences_window_appears(context)


@then("[background] The reboot alert window appears")
def background_the_reboot_alert_window_appears(context):
    if 'fake' not in str(context._config.tags).split(','):
        the_reboot_alert_window_appears(context)


