from behave import *
from ccd.views import *
from time import sleep

use_step_matcher("re")


@when("I go to the domain conferences page")
def step_impl(context):
    domain_view.goto_conferences()


@step("I see if any test conferences are listed")
def step_impl(context):
    context.rows = domain_conferences_view.find_table_rows_by_text(1, 'Test Conference', partial=True)
    pass


@then("I click the trash can for the first test conference")
def step_impl(context):
    if len(context.rows):
        elem = domain_conferences_view.find_sub_element(context.rows[0], "TrashCanIconSub")
        domain_conferences_view.click_element(elem)


@step("I click Yes on the confirmation popup")
def step_impl(context):
    if len(context.rows):
        sleep(2)
        domain_view.click_element_by_name("ConfirmYes")


@then("I see the first test conference has been deleted")
def step_impl(context):
    if len(context.rows) > 0:
        rows = domain_conferences_view.find_table_rows_by_text(1, 'Test Conference', partial=True)
        assert len(rows) == len(context.rows) - 1, "conference not deleted"
        context.rows = rows


@then("I repeat until there are no test conferences listed")
def step_impl(context):
    while len(context.rows) > 0:
        context.execute_steps(u"""
            Then I click the trash can for the first test conference
            And I click Yes on the confirmation popup
            And I see the first test conference has been deleted
        """)


@when("I go to the domain users page")
def step_impl(context):
    domain_view.goto_users()


@step("I see if any test users are listed")
def step_impl(context):
    context.rows = domain_users_view.find_deletable_user_rows()
    pass


@then("I click the trash can for the first test user")
def step_impl(context):
    if len(context.rows):
        elem = domain_users_view.find_sub_element(context.rows[0], "TrashCanIconSub")
        domain_users_view.click_element(elem)


@then("I see the first test user has been deleted")
def step_impl(context):
    if len(context.rows) > 0:
        rows = domain_users_view.find_deletable_user_rows()
        assert len(rows) == len(context.rows) - 1, "user not deleted"
        context.rows = rows


@then("I repeat until there are no test users listed")
def step_impl(context):
    while len(context.rows) > 0:
        context.execute_steps(u"""
            Then I click the trash can for the first test user
            And I click Yes on the confirmation popup
            And I see the first test user has been deleted
        """)


@when("I go to the timeframes page")
def step_impl(context):
    domain_view.goto_time_frames()


@step("I see if any timeframes are listed")
def step_impl(context):
    context.rows = domain_time_frames_view.find_elements("TableRows")


@then("I click the trash can for the first timeframe")
def step_impl(context):
    if len(context.rows):
        sleep(2)
        elem = domain_time_frames_view.find_sub_element(context.rows[0], "TrashCanIconSub")
        domain_users_view.click_element(elem)


@step("I see the first timeframe has been deleted")
def step_impl(context):
    if len(context.rows) > 0:
        rows = domain_time_frames_view.find_elements("TableRows")
        assert len(rows) == len(context.rows) - 1, "user not deleted"
        context.rows = rows


@then("I repeat until there are no timeframes listed")
def step_impl(context):
    while len(context.rows) > 0:
        context.execute_steps(u"""
            Then I click the trash can for the first timeframe
            And I click Yes on the confirmation popup
            And I see the first timeframe has been deleted
        """)
