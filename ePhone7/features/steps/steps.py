from behave import *
from ePhone7.views import *
import re


@given('I go to the preferences view')
def step_impl(context):
    # user_view.goto_prefs()
    pass


@when('I touch the "System" menu category')
def step_impl(context):
    # prefs_view.hide_list_items()
    # prefs_view.click_element_by_key('System')
    pass


@when('I touch the "About" menu item')
def step_impl(context):
    # prefs_view.click_element_by_key('About')
    pass


@then('The correct version is displayed')
def step_impl(context):
    # about_popup = prefs_view.find_element_by_key('AppVersion')
    # source = about_popup.text
    # prefs_view.click_element_by_key('AboutOk')
    # prefs_view.click_element_by_key('System')
    # m = re.match('App Version : (\S*)', source.encode('utf8'))
    # if m is None:
    #     print("Unknown Version")
    # else:
    #     version = m.group(1)
    #     print("\nVersion = %s" % version)
    #     expected = context.config.userdata.get('version')
    #     assert version == expected, "Incorrect Version: expected %s, got %s" % (expected, version)
    pass


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


@then("the Voicemail view appears")
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


@when("I touch the Voicemail button")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the New tab")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("I receive a new voicemail")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("The new voicemail is the first item listed")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the new voicemail element")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("A voicemail detail window appears")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("The voicemail audio plays back")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the handset icon")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("The voicemail detail window disappears")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("My phone calls the voicemail sender")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the Delete icon")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("The voicemail is no longer listed")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the Save icon")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the Saved tab")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("The voicemail is the first item listed")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the voicemail element")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the Trash tab")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the Forward icon")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("A list of Coworker contacts appears")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("A keypad appears")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I use the keypad filter the list of contacts")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("I touch a contact element")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("I can choose Cancel or OK by touching the corresponding button")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I choose OK")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("The voicemail is still the first item in the view")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("The voicemail is also available in the destination contact's new voicemails list")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the History button")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("I see the All and Missed tabs at the top of the screen")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@given("I receive a call")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("The incoming call window appears")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("I answer the call")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I end the call")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("The incoming call window disappears")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the All tab")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("I see the call at the top of the All History view")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("The call has a blue handset icon with an incoming arrow")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("I ignore the call")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("The caller ends the call")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("The call has a red handset icon with a missed arrow")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the Missed tab")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("I see the call at the top of the Missed History view")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("The caller leaves a voicemail")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("The call has a voicemail icon")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@given("I make a call to a coworker contact")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("The in-call window appears")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("The in-call window disappears")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@step("The call has a green handset icon with an outgoing arrow")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@then("My phone calls back the caller")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass


@when("I touch the voicemail icon")
def step_impl(context):
    """
    :type context: behave.runner.Context
    """
    pass