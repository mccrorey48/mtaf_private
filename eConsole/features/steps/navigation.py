from behave import *
from eConsole.views import *
from lib.wrappers import fake


@step("I click the Message Settings menu item")
@fake
def i_click_the_mailbox_settings_menu_item(context):
    base_view.click_named_element('MessageSettings')


@step("the Settings Menu appears")
@fake
def the_settings_menu_appears(context):
    assert base_view.element_is_present('MessageSettings'), "Message Settings menu item not found"


@step("the {view_name} page appears")
@fake
def the_viewname_page_appears(context, view_name):
    views = {
        "call history": call_history_view,
        "contacts": contacts_view,
        "home": home_view,
        "login": login_view,
        "messages": messages_view,
        "message settings": message_settings_view,
        "phones": phones_view
    }
    assert views[view_name.lower()].becomes_present(), "%s view not present" % view_name
    assert base_view.element_becomes_not_present('LoadingGif', 10), "loading GIF present after 10 sec" % view_name


