from behave import *
from ppo.features.lib.pages import *

use_step_matcher("re")


@when("I open automationpractice website")
def step_impl(context):
    page = AutomationHomePage(context)
    page.visit("http://www.automationpractice.com")
    page.sign_in.click()


@step('I login with username "([^"]*)" and password "([^"]*)"')
def step_impl(context, username, password):
    page = LoginPage(context)
    page.email.send_keys(username)
    page.password.send_keys(password)
    page.signin_button.click()
    # page.login(username=username,passwd=password)


@then("I verify that I successfully logged in by logging out")
def step_impl(context):
    AutomationHomePage(context).sign_out.click()

@step("I hover on women menu item and click summer dresses")
def step_impl(context):
    page = AutomationHomePage(context).HeaderPage(context)
    page.hover(page.menu_women)
    page.DressesPage(context).summer_dresses.click()
    assert "SUMMER DRESSES" in SummerDressesCatalogPage(context).category_name.text


@step("I add a summer dress to cart")
def step_impl(context):
    page = SummerDressesCatalogPage(context).PrintedSummerDress1(context)
    # so that we can compare unit price in downstream steps
    # context.browser.execute_script('window.scrollTo(0,500)')
    page.hover(page.img_dress1)
    context.unitprice = page.product_price.text
    elem = page.add_cart_dress1
    elem.click()
    page.CartPopup(context).proceed_to_checkout.click()


@step("verify the item and price")
def step_impl(context):
    page = ShoppingCartSummaryPage(context)
    # context.browser.execute_script('window.scrollTo(0,1000)')
    assert context.unitprice in page.unit_price.text
    page.proceed_to_checkout.click()


@step("I verify the address and proceed")
def step_impl(context):
    page = AddressPage(context)
    assert "ADDRESSES" in page.page_heading.text, "page.page_heading.text = %s" % page.page_heading.text
    # context.browser.execute_script('window.scrollTo(0,500)')
    page.proceed_to_checkout.click()


@step("I verify shipping address and proceed")
def step_impl(context):
    page = ShippingAddressPage(context)
    assert "SHIPPING" in page.page_heading.text
    page.terms.click()
    page.proceed_to_checkout.click()


@step("I select payment method")
def step_impl(context):
    page = PaymentMethodPage(context)
    assert "PLEASE CHOOSE YOUR PAYMENT METHOD" in page.page_heading.text
    page.check.click()


@step("I confirm the order")
def step_impl(context):
    page = OrderSummaryPage(context)
    assert "ORDER SUMMARY" in page.page_heading.text
    page.confirm_order.click()


@then("I verify successful purchase")
def step_impl(context):
    page = OrderConfirmationPage(context)
    assert "ORDER CONFIRMATION" in page.page_heading.text