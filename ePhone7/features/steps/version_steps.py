from behave import *
from ePhone7.views import *
import re


@given('I go to the preferences view')
def step_impl(context):
    user_view.goto_prefs()


@when('I touch the "System" menu category')
def step_impl(context):
    prefs_view.hide_list_items()
    prefs_view.click_element_by_key('System')


@when('I touch the "About" menu item')
def step_impl(context):
    prefs_view.click_element_by_key('About')


@then('The correct version is displayed')
def step_impl(context):
    about_popup = prefs_view.find_element_by_key('AppVersion')
    source = about_popup.text
    prefs_view.click_element_by_key('AboutOk')
    prefs_view.click_element_by_key('System')
    m = re.match('App Version : (\S*)', source.encode('utf8'))
    if m is None:
        print("Unknown Version")
    else:
        version = m.group(1)
        print("\nVersion = %s" % version)
        expected = context.config.userdata.get('version')
        assert version == expected, "Incorrect Version: expected %s, got %s" % (expected, version)
