from behave import *

use_step_matcher("re")


@given("I don't do anything")
def step_impl(context):
    assert True


@then("nothing fails")
def step_impl(context):
    assert True


@given("I fail a step")
def step_impl(context):
    assert False, "fail this one"


@then("this happens")
def step_impl(context):
    assert True
