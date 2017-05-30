from behave import *
from ePhone7.views import *
import re
from lib.user_exception import UserException as Ux
import lib.logging_esi as logging
from ePhone7.utils.versions import *
log = logging.get_logger('esi.prefs')


@step("[prefs] A popup informs me that help email has been sent to my email address")
def prefs__a_popup_informs_me_that_help_email_has_been_sent_to_my_email_address(context):
    pass


@step('[prefs] A submenu appears with a "Call Forwarding Options" option')
def prefs__a_submenu_appears_with_a_call_forwarding_options_option(context):
    pass


@step('[prefs] A submenu appears with a "Network" option')
def prefs__a_submenu_appears_with_a_network_option(context):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_view.element_is_present('MenuItemNetworkText')


@step("[prefs] A submenu opens with an eHelp option")
def prefs__a_submenu_opens_with_an_ehelp_option(context):
    pass


@step('[prefs] A window appears with a list of contacts')
def prefs__a_window_appears_with_a_list_of_contacts(context):
    pass


@step('[prefs] A window appears with a section labeled "Call Forward Busy"')
def prefs__a_window_appears_with_a_section_labeled_call_forward_busy(context):
    pass


@then('[prefs] an upgrade is found and an "Upgrade" button appears')
def prefs__an_upgrade_is_found_and_an_upgrade_button_appears(context):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_view.element_is_present('UpgradeButton')


@then("[prefs] I read the displayed versions for the app and AOSP")
def prefs__i_read_the_displayed_versions_for_the_app_and_aosp(context):
    if 'fake' not in str(context._config.tags).split(','):
        app_version = prefs_view.find_named_element('AppVersion').text
        aosp_version = prefs_view.find_named_element('SystemVersion').text
        prefs_view.click_named_element('AboutOk')
        prefs_view.click_named_element('System')
        m = re.match('App Version : (\S*)', app_version.encode('utf8'))
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


@step("[prefs] I touch a contact element")
def prefs__i_touch_a_contact_element(context):
    pass


@step('[prefs] I touch "Call Forwarding Options"')
def prefs__i_touch_call_forwarding_options(context):
    pass


@step('[prefs] I touch "eHelp"')
def prefs__i_touch_ehelp(context):
    pass


@step('[prefs] I touch "Need Help"')
def prefs__i_touch_need_help(context):
    pass


@step('[prefs] I touch "OK" on the email notification popup')
def prefs__i_touch_ok_on_the_email_notification_popup(context):
    if 'fake' not in str(context._config.tags).split(','):
        pass


@step('[prefs] I touch "Personal"')
def prefs__i_touch_personal(context):
    pass


@step('[prefs] I touch the "Call Forward Busy" section')
def prefs__i_touch_the_call_forward_busy_section(context):
    pass


@step('[prefs] I touch the "Check for System Update" option')
def prefs__i_touch_the_check_for_system_update_option(context):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_view.click_named_element('SystemUpdate')


@step("[prefs] I touch the Delete button")
def prefs__i_touch_the_delete_button(context):
    pass


@when("[prefs] I touch the Delete icon")
def prefs__i_touch_the_delete_icon(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step('[prefs] I touch the "{name}" menu category')
def prefs__i_touch_the_name_menu_category(context, name):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_view.hide_list_items()
        elems = prefs_view.find_named_elements('MenuCategories')
        for elem in elems:
            if elem.text == name:
                elem.click()
                break
        else:
            raise Ux('No menu category element with text="%s" was found' % name)


@step('[prefs] I touch the "{name}" menu item')
def prefs__i_touch_the_name_menu_item(context, name):
    if 'fake' not in str(context._config.tags).split(','):
        elems = prefs_view.find_named_elements('MenuItemTexts')
        for elem in elems:
            if elem.text == name:
                elem.click()
                break
        else:
            raise Ux('No menu item text element with text="%s" was found' % name)


@step('[prefs] I touch the "Network" option')
def prefs__i_touch_the_network_option(context):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_view.click_named_element('MenuItemNetworkText')


@step('[prefs] I touch the "Upgrade" button')
def prefs__i_touch_the_upgrade_button(context):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_view.click_named_element('UpgradeButton')


@step('[prefs] I touch the "X" icon')
def prefs__i_touch_the_x_icon(context):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_view.click_named_element('CloseButton')


@step('[prefs] Only the contact I touched is listed')
def prefs__only_the_contact_i_touched_is_listed(context):
    pass


@step("[prefs] the current versions are installed")
def prefs__the_current_versions_are_installed(context):
    if 'fake' not in str(context._config.tags).split(','):
        current_aosp, current_app = get_current_versions(context.config.userdata['ota_server'])
        installed_aosp, installed_app = get_installed_versions()
        assert installed_aosp == current_aosp, "Expected installed aosp version %s, got %s" % (current_aosp, installed_aosp)
        assert installed_app == current_app, "Expected installed app version %s, got %s" % (current_app, installed_app)


@step("[prefs] the email notification popup disappears")
def prefs__the_email_notification_popup_disappears(context):
    if 'fake' not in str(context._config.tags).split(','):
        pass


@step("[prefs] the installed versions are displayed correctly")
def prefs__the_installed_versions_are_displayed_correctly(context):
    if 'fake' not in str(context._config.tags).split(','):
        installed_aosp, installed_app = get_installed_versions()
        assert context.aosp_version == installed_aosp, "Expected displayed aosp version %s, got %s" % (installed_aosp, context.aosp_version)
        assert context.app_version == installed_app, "Expected displayed app version %s, got %s" % (installed_app, context.app_version)


@step("[prefs] the Preferences window appears")
def prefs__the_preferences_window_appears(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert prefs_view.element_is_present('Preferences')


@step("[prefs] the Preferences window disappears")
def prefs__the_preferences_window_disappears(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert prefs_view.element_is_not_present('Preferences')


