from behave import *
from ePhone7.views import *
import re


@step("[prefs] I see the Need Help, Personal, Phone and System category elements")
def prefs__i_see_the_need_help_personal_phone_and_system_category_elements(context):
    pass


@step('[prefs] I touch the "About" menu item')
def prefs__i_touch_the_about_menu_item(context):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_view.click_named_element('About')


@step('[prefs] I touch the "System" menu category')
def prefs__i_touch_the_system_menu_category(context):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_view.hide_list_items()
        prefs_view.click_named_element('System')


@step('[prefs] I touch the "X" icon')
def prefs__i_touch_the_x_icon(context):
    if 'fake' not in str(context._config.tags).split(','):
        prefs_view.click_named_element('CloseButton')


@step('[prefs] the correct version is displayed')
def prefs__the_correct_version_is_displayed(context):
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


@step("[prefs] the Preferences window appears")
def prefs__the_preferences_window_appears(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert prefs_view.element_is_present('Preferences')


@step("[prefs] the Preferences window disappears")
def prefs__the_preferences_window_disappears(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert prefs_view.element_is_not_present('Preferences')


