from behave import *
from eConsole.views import *
from lib.wrappers import fake


@step('I click the Login button')
@fake
def i_click_the_login_button(context):
    login_view.click_login_button()


@step('I enter a password')
@fake
def i_enter_a_password(context):
    login_view.input_password(context.config.userdata['user_scope'])


@step('I enter a user ID')
@fake
def i_enter_a_user_id(context):
    login_view.input_username(context.config.userdata['user_scope'])


@step('I go to the portal login page')
@fake
def i_go_to_the_portal_login_page(context):
    base_view.get_portal_url()


