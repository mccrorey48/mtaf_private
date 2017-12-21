from behave import *
from WebApp.views import *
from describe import Value


@given('I log in as reseller')
def step_impl(context):
    base_view.get_portal_url()
    login_view.login_with_good_credentials()
    reseller_view.wait_for_page_title()


@given('I go to the reseller home page')
def step_impl(context):
    reseller_view.goto_home()
    reseller_home_view.wait_for_page_title()


@given('I go to the reseller domains page')
def step_impl(context):
    reseller_view.goto_domains()
    reseller_domains_view.wait_for_page_title()


@when('I click the home tab')
def step_impl(context):
    reseller_view.goto_home()


@when('I click the domains tab')
def step_impl(context):
    reseller_view.goto_domains()


@when('I click the inventory tab')
def step_impl(context):
    reseller_view.goto_inventory()


@when('I use the domain quick launch to select a domain')
def step_impl(context):
    reseller_home_view.goto_test_domain_quick()


@when('I select a domain from the table')
def step_impl(context):
    reseller_domains_view.goto_test_domain_select()


@when('I select a domain using the filter entry')
def step_impl(context):
    reseller_domains_view.goto_test_domain_filter()


@then('the selected domain home page will load')
def step_impl(context):
    base_view.test_domain_message_is_displayed()


@then('the reseller home page will load')
def step_impl(context):
    reseller_home_view.wait_for_page_title()


@then('the reseller domains page will load')
def step_impl(context):
    reseller_domains_view.wait_for_page_title()


@then('the reseller inventory page will load')
def step_impl(context):
    reseller_inventory_view.wait_for_page_title()


@then ('Exactly one domain is shown in the table')
def step_impl(context):
    Value(reseller_domains_view.get_visible_domain_name_elems()).should.have(1)


@then ('the selected domain is shown in the first row')
def step_impl(context):
    Value(reseller_domains_view.first_row_is_test_domain()).should.be.true()


@when('I click the domain name in the table')
def step_impl(context):
    reseller_domains_view.click_first_domain()




