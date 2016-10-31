from behave import *
from ccd.views import *

use_step_matcher("re")


@step("there are no timeframes listed in the table")
def step_impl(context):
    rows = domain_time_frames_view.find_elements_by_key("TableRows")
    assert len(rows) == 0, "Expected no timeframes in table, found %d" % len(rows)


@step("I click the Add Time Frame button")
def step_impl(context):
    domain_time_frames_view.click_element_by_key('AddTimeFrame')


@then("an Add a Timeframe modal dialog appears")
def step_impl(context):
    domain_time_frames_view.find_element_by_key("TimeframeAddForm")


@when("I enter a timeframe name")
def step_impl(context):
    domain_time_frames_view.find_element_by_key("TimeframeName").send_keys('SVAuto')


@step("I click the Save button")
def step_impl(context):
    domain_time_frames_view.click_element_by_key('SaveButton')


@then("the new timeframe is listed in the table")
def step_impl(context):
    rows = domain_time_frames_view.find_elements_by_key("TableRows")
    assert len(rows) == 1, "Expected new timeframe in table, found %d" % len(rows)
