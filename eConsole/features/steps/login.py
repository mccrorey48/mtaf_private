from behave import *
from eConsole.views import *
from eConsole.config.configure import cfg
from mtaf.decorators import fake


@step('I click the Login button')
@fake
def i_click_the_login_button(context):
    login_view.click_login_button()


@step('I enter a {user_scope} password')
@fake
def i_enter_a_password(context, user_scope):
    user = cfg.default_user[user_scope]
    password = cfg.accounts[user]['password']
    login_view.input_password(password)


@step('I enter a {user_scope} user ID')
@fake
def i_enter_a_user_id(context, user_scope):
    user = cfg.default_user[user_scope]
    login_view.input_username(user)


@step('I go to the portal login page')
@fake
def i_go_to_the_portal_login_page(context):
    base_view.get_url(cfg['portal_url'][context.config.userdata['portal_server']])


