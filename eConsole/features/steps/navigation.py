from behave import *
from eConsole.views import *
from lib.wrappers import fake


@step("I click the button with my user name")
@fake
def i_click_the_button_with_my_user_name(context):
    pass


@step("I click the Logout menu item")
@fake
def i_click_the_logout_menu_item(context):
    pass


@step("I click the Mailbox Settings menu item")
@fake
def i_click_the_mailbox_settings_menu_item(context):
    pass


@step("the Settings Menu appears")
@fake
def the_settings_menu_appears(context):
    pass


@step("the {view_name} page appears")
@fake
def the_viewname_page_appears(context, view_name):
    views = {
        "call history": call_history_view,
        "contacts": contacts_view,
        "home": home_view,
        "login": login_view,
        "messages": messages_view,
        "phones": phones_view
    }
    assert views[view_name.lower()].becomes_present(), "%s view not present" % view_name


