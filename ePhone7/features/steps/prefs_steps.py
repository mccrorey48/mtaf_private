from behave import *

from ePhone7.utils.versions import *
from ePhone7.views import *
from mtaf import mtaf_logging
import re
from mtaf.user_exception import UserException as Ux

log = mtaf_logging.get_logger('mtaf.prefs')


@step("[prefs] A popup informs me that help email has been sent to my email address")
def prefs__a_popup_informs_me_that_help_email_has_been_sent_to_my_email_address(context):
    pass


@step('[prefs] A submenu appears with a "Call Forwarding Options" option')
def prefs__a_submenu_appears_with_a_call_forwarding_options_option(context):
    pass


@step('[prefs] A submenu appears with a "Network" option')
def prefs__a_submenu_appears_with_a_network_option(context):
    prefs_view.element_is_present('MenuItemNetworkText')


@step('[prefs] A submenu appears with an "Auto-Answer Calls" toggle')
def prefs__a_submenu_appears_with_an_autoanswer_calls_toggle(context):
    pass


@step("[prefs] A submenu opens with an eHelp option")
def prefs__a_submenu_opens_with_an_ehelp_option(context):
    pass


@step('[prefs] A window appears with a list of contacts')
def prefs__a_window_appears_with_a_list_of_contacts(context):
    pass


@step('[prefs] A window appears with a section labeled "Call Forward Busy"')
def prefs__a_window_appears_with_a_section_labeled_call_forward_busy(context):
    pass


@step('[prefs] an upgrade is found and an "Upgrade" button appears')
def prefs__an_upgrade_is_found_and_an_upgrade_button_appears(context):
    prefs_view.element_is_present('UpgradeButton')


@step("[prefs] I close all open submenus")
def prefs__i_close_all_open_submenus(context):
    prefs_view.hide_list_items()


@step("[prefs] I read the displayed versions for the app and AOSP")
def prefs__i_read_the_displayed_versions_for_the_app_and_aosp(context):
    app_version = prefs_view.find_named_element('AppVersion').text
    aosp_version = prefs_view.find_named_element('SystemVersion').text
    prefs_view.click_named_element('AboutOk')
    prefs_view.click_named_element('System')
    m = re.match('App Version : (\d+\.\d+\.\d+)', app_version.encode('utf8'))
    if m is None:
        context.app_version = "Unknown Version"
    else:
        context.app_version = m.group(1)
        print("\nVersion = %s" % context.app_version)
    m = re.match('System Version : (\S*)', aosp_version.encode('utf8'))
    if m is None:
        context.aosp_version = "Unknown Version"
    else:
        context.aosp_version = m.group(1)
        print("\nVersion = %s" % context.aosp_version)


@step("[prefs] I see the Need Help, Personal, Phone and System category elements")
def prefs__i_see_the_need_help_personal_phone_and_system_category_elements(context):
    pass


@step("[prefs] I swipe the Wired Headset switch to the {direction}")
def prefs__i_swipe_the_wired_headset_switch_to_the_direction(context, direction):
    prefs_view.swipe_named_element("WiredHeadsetSwitch", direction)


@step("[prefs] I touch a contact element")
def prefs__i_touch_a_contact_element(context):
    pass


@step('[prefs] I touch and drag the toggle handle to the "Off" position')
def prefs__i_touch_and_drag_the_toggle_handle_to_the_off_position(context):
    pass


@step('[prefs] I touch and drag the toggle handle to the "On" position')
def prefs__i_touch_and_drag_the_toggle_handle_to_the_on_position(context):
    pass


@step('[prefs] I touch the "Call Forward Busy" section')
def prefs__i_touch_the_call_forward_busy_section(context):
    pass


@step("[prefs] I touch the Delete icon")
def prefs__i_touch_the_delete_icon(context):
    pass


@step('[prefs] I touch the "X" icon')
def prefs__i_touch_the_x_icon(context):
        prefs_view.CloseButton.click()


@step('[prefs] Only the contact I touched is listed')
def prefs__only_the_contact_i_touched_is_listed(context):
    pass


@step("[prefs] the email notification popup disappears")
def prefs__the_email_notification_popup_disappears(context):
    pass


@step("[prefs] the installed versions are displayed correctly")
def prefs__the_installed_versions_are_displayed_correctly(context):
    installed_aosp, installed_app = get_installed_versions()
    assert context.aosp_version == installed_aosp, "Expected displayed aosp version %s, got %s" % \
                                                   (installed_aosp, context.aosp_version)
    assert context.app_version == installed_app, "Expected displayed app version %s, got %s" % \
                                                 (installed_app, context.app_version)


@step("[prefs] the Preferences window appears")
def prefs__the_preferences_window_appears(context):
    assert prefs_view.Preferences is not None, "prefs_view.Preferences not present"
    for i in range(5):
        elems = prefs_view.find_named_elements('Collapse')
        if len(elems) == 0:
            break
        elems[0].click()
    else:
        raise Ux("Failed to collapse expanded Preferences menu categories")


@step("[prefs] the Preferences window disappears")
def prefs__the_preferences_window_disappears(context):
    assert prefs_view.element_becomes_not_present('Preferences')


