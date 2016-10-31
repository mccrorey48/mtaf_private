from behave import *

use_step_matcher("re")


@given("I go to the Contacts view")
def step_impl(context):
    pass


@step("I go to the Personal tab")
def step_impl(context):
    pass


@when('I touch the "Sign in with Google" banner')
def step_impl(context):
    pass


@then("A Google login screen appears")
def step_impl(context):
    pass


@step("I enter my Google user id and password")
def step_impl(context):
    pass


@then("My Google contacts appear on the Personal contacts list")
def step_impl(context):
    pass