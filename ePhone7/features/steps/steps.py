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


@given("I go to the Contacts view")
def step_impl(context):
    user_view.goto_tab('Contacts')


@step("I go to the Personal tab")
def step_impl(context):
    contacts_view.goto_tab('Personal')


@when('I touch the "Sign in with Google" banner')
def step_impl(context):
    contacts_view.click_element_by_key('GoogleSignInBanner')
    pass


@then("A Google login screen appears")
def step_impl(context):
    pass


@step("I enter my Google user id and password")
def step_impl(context):
    pass


@then("My Google contacts appear on the Personal contacts list")
def step_impl(context):
    pass


@given("I am logged in to the ePhone7")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("I go to the Home screen")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@given("I touch the Contacts button")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("the Contacts view appears")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("I see the Personal, Coworkers, Favorites and Groups tabs at the top of the screen")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@given("I touch the History button")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("I see the All and New tabs at the top of the screen")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("the Voicemail view appears")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("I see the New, Saved and Trash tabs at the top of the screen")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@given("I touch the Dial button")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("the Dial view appears")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@given("I touch the Preferences button")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("the Preferences view appears")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass