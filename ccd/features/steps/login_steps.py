from behave import *
from ccd.views import *


@given('I go to the portal login page')
def step_impl(context):
    base_view.get_portal_url()


@when('I enter a valid user ID')
def step_impl(context):
    login_view.input_reseller_username()


@when('I enter a bad user ID')
def step_impl(context):
    login_view.input_bad_username()


@when('I enter no user ID')
def step_impl(context):
    pass


@when('I enter a valid password')
def step_impl(context):
    login_view.input_reseller_password()


@when('I enter a bad password')
def step_impl(context):
    login_view.input_bad_password()


@when('I enter no password')
def step_impl(context):
    pass


@when('I click the Login button')
def step_impl(context):
    login_view.click_login()


@then('the Manager Home page will load')
def step_impl(context):
    reseller_view.wait_for_page_title()


@then('the invalid alert will appear')
def step_impl(context):
    login_view.wait_for_invalid_login_alert()
