from behave import *
from eConsole.views import *


@step('I click the "{item_text}" menu item')
def i_click_the_itemtext_menu_item(context, item_text):
    logged_in_view.click_settings_item_with_text(item_text)


@step("I click the Message Settings menu item")
def i_click_the_message_settings_menu_item(context):
    logged_in_view.click_named_element('MessageSettings')


@step("I navigate to the Manage Organization/Inventory Page")
def i_navigate_to_the_manage_organizationinventory_page(context):
    logged_in_view.ManageOrganization.click()


@step('the content is correct for the "{page}" page')
def the_content_is_correct_for_the_user_scope(context, page):
    user_scope = context.config.userdata['user_scope']
    view = all_views[snake_case(page)]
    err_msg = "Incorrect content for %s scope" % user_scope
    assert view.has_scope_content(context.config.userdata['user_scope']), err_msg


@step("the Settings Menu appears")
def the_settings_menu_appears(context):
    assert logged_in_view.element_is_present('MessageSettings'), "Message Settings menu item not found"


@step('the "{view_name}" page appears')
def the_viewname_page_appears(context, view_name):
    view_key = view_name.lower()
    view_key = ' '.join(view_key.split('/'))
    view_key = '_'.join(view_key.split()) + "_view"
    assert all_views[view_key].becomes_present(), "%s view not present" % view_name
    assert logged_in_view.element_becomes_not_present('LoadingGif', 10), "loading GIF present after 10 sec" % view_name


