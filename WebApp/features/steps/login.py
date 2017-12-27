from behave import *
from WebApp.views import *
from WebApp.config.configure import cfg
from selenium.common.exceptions import TimeoutException
from lib.user_exception import UserException as Ux


@step('I go to the start page')
def step_impl(context):
    base_view.get_url(cfg.site.app_url)


@step('I go to the login page')
def step_impl(context):
    start_view.goto_login()


@step('I enter a valid user ID')
def step_impl(context):
    login_view.input_username()


@step('I enter a valid password')
def step_impl(context):
    login_view.input_password()


@step('I click the Login button')
def step_impl(context):
    login_view.click_login()


@step('the User Home page will load')
def step_impl(context):
    try:
        user_home_view.wait_for_page_title()
    except TimeoutException:
        raise AssertionError("Timed out waiting for Manager Home Page to load")


@step('I enter a bad user ID')
def step_impl(context):
    login_view.input_bad_username()


@step('I enter no user ID')
def step_impl(context):
    pass


@step('I enter a bad password')
def step_impl(context):
    login_view.input_bad_password()


@step('I enter no password')
def step_impl(context):
    pass


@step('the invalid alert will appear')
def step_impl(context):
    try:
        login_view.wait_for_invalid_login_alert()
    except Ux:
        raise AssertionError('Invalid username/password alert not found')
