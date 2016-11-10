from behave import *
from ccd.views import *
from selenium.common.exceptions import TimeoutException
from lib.user_exception import UserException as Ux


@given('I go to the portal login page')
def step_impl(context):
    base_view.get_portal_url()


@when('I enter a valid user ID')
def step_impl(context):
    login_view.input_reseller_username()


@when('I enter a valid password')
def step_impl(context):
    login_view.input_reseller_password()


@when('I click the Login button')
def step_impl(context):
    login_view.click_login()


@then('the Manager Home page will load')
def step_impl(context):
    try:
        reseller_view.wait_for_page_title()
    except TimeoutException:
        raise AssertionError("Timed out waiting for Manager Home Page to load")


@when('I enter a bad user ID')
def step_impl(context):
    login_view.input_bad_username()


@when('I enter no user ID')
def step_impl(context):
    pass


@when('I enter a bad password')
def step_impl(context):
    login_view.input_bad_password()


@when('I enter no password')
def step_impl(context):
    pass


@then('the invalid alert will appear')
def step_impl(context):
    try:
        login_view.wait_for_invalid_login_alert()
    except Ux:
        raise AssertionError('Invalid username/password alert not found')
