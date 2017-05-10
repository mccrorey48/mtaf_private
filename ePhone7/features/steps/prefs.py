from behave import *
from ePhone7.views import *
import re
from lib.user_exception import UserException as Ux
import lib.logging_esi as logging
log = logging.get_logger('esi.prefs')


@step('[prefs] A submenu appears with a "Network" option')
def prefs__a_submenu_appears_with_a_network_option(context):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_view.element_is_present('MenuItemNetworkText')


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


@step('[prefs] I touch the "Check for System Update" option')
def prefs__i_touch_the_check_for_system_update_option(context):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_view.click_named_element('SystemUpdate')


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


@step("[prefs] I upgrade the phone if the versions are not correct")
def prefs__i_upgrade_the_phone_if_the_versions_are_not_correct(context):
    if 'fake' not in str(context._config.tags).split(','):
        current_app = context.config.userdata.get('current_app')
        current_aosp = context.config.userdata.get('current_aosp')
        log.debug("installed versions: app %s, aosp %s" % (context.app_version, context.aosp_version))
        log.debug("required versions: app %s, aosp %s" % (current_app, current_aosp))
        app_upgrade_required = current_app is not None and current_app != context.app_version
        aosp_upgrade_required = current_aosp is not None and current_aosp != context.aosp_version
    else:
        app_upgrade_required = True
        aosp_upgrade_required = True
    if aosp_upgrade_required or app_upgrade_required:
        log.debug("checking for updates")
        context.run_substep('I set the OTA server')
        context.run_substep('[user] I touch the Preferences icon')
        context.run_substep('[prefs] the Preferences window appears')
        context.run_substep('[prefs] I touch the "System" menu category')
        context.run_substep('[prefs] I touch the "Updates" menu item')
        if prefs_view.element_is_present('SystemUpdate'):
            context.run_substep('[prefs] I touch the "Check for System Update" option')
            context.run_substep('[prefs] an upgrade is found and an "Upgrade" button appears')
            context.run_substep('[prefs] I touch the "Upgrade" button')
        context.run_substep('I wait for the phone to upgrade and reboot')
        context.run_substep('I verify the system and app versions are current')


@step("[prefs] the Preferences window appears")
def prefs__the_preferences_window_appears(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert prefs_view.element_is_present('Preferences')


@step("[prefs] the Preferences window disappears")
def prefs__the_preferences_window_disappears(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert prefs_view.element_is_not_present('Preferences')


