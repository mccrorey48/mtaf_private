from behave import *
from ccd.views import *


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
    reseller_view.wait_for_page_title()
