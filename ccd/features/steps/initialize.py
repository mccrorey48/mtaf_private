from behave import *
from ccd.views import *

use_step_matcher("re")


@when("I go to the domain conferences page")
def step_impl(context):
    domain_view.goto_conferences()


@step("I see if any test users are listed")
def step_impl(context):
    context.rows = domain_users_view.find_table_rows_by_text(1, 'Test Conference', partial=True)
    pass


@step("I see if any test conferences are listed")
def step_impl(context):
    context.rows = domain_conferences_view.find_table_rows_by_text(1, 'Test Conference', partial=True)
    pass


@then("I click the trash can for the first test conference")
def step_impl(context):
    if len(context.rows):
        elem = domain_conferences_view.find_sub_element_by_key(context.rows[0], "TrashCanIconSub")
        domain_conferences_view.click_element(elem)


@step("I click Yes on the confirmation popup")
def step_impl(context):
    if len(context.rows):
        domain_conferences_view.click_element_by_key("ConfirmYes")


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
            And I see the first row has been deleted
        """)




@when("I go to the domain users page")
def step_impl(context):
    pass


@step("I see one or more test users listed")
def step_impl(context):
    pass


@then("I click the trash can for the first row")
def step_impl(context):
    pass


@then("I repeat until there are no test users listed")
def step_impl(context):
    pass