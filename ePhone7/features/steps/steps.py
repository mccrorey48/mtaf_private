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
    # user_view.goto_tab('Contacts')
    pass


@step("I go to the Personal tab")
def step_impl(context):
    # contacts_view.goto_tab('Personal')
    pass


@when('I touch the "Sign in with Google" banner')
def step_impl(context):
    # contacts_view.click_element_by_key('GoogleSignInBanner')
    pass


@then("A Google login screen appears")
def step_impl(context):
    pass


@step("I enter my Google user id and password")
def step_impl(context):
    pass


@then("My Google contacts are shown on the display")
def step_impl(context):
    pass


@given("I log in to the ePhone7")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("I go to the Home view")
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


@when("I touch the Contacts button")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("I touch the Coworkers tab")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("My Coworker contacts are shown on the display")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("My Coworker contacts appear on the Coworkers contacts list")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the handset icon on a contact list item")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("My phone calls the contact")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("I touch the Favorites tab")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("My Favorite contacts are shown on the display")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("My Favorite contacts appear on the Coworkers contacts list")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the name of a contact that is not a Favorite")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("A contact detail screen appears with a white star icon")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the white star icon")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("The star turns yellow")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("The contact is shown on the display")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the name of a contact")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("A contact detail screen appears with a yellow star icon")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the yellow star icon")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("The start turns white")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I close the contact detail screen")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("The contact is not shown on the display")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("My Favorite contacts are shown on the display")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("I touch the name of a contact")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("A contact detail screen appears with a yellow star icon")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("I touch the yellow star icon")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("The start turns white")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@given("I touch the Groups tab")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("My Group Lists are shown on the display")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the Add button")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("A Create New Group popup appears")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I enter a group name")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("I touch the Create button")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("The personal group list is shown on the display")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the name of a personal Group list")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("The contact list for the group is displayed")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("Add and Delete buttons are visible")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("My Coworker contacts are displayed in a list with checkboxes")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch a check a box next to a contact")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("A check mark appears in the box")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the Done button")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("The contact is shown on the contact list for the group")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("The previously added contact is not on the list with checkboxes")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the Delete button")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("The Group list contacts are displayed in a list with checkboxes")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("The contact is not shown on the contact list for the group")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the name of a system Group list")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("Add and Delete buttons are not visible")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass