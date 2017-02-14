from behave import *
from ePhoneGoAndroid.views import *

use_step_matcher("re")


@given("I see the terms and conditions screen")
def step_impl(context):
    pass


@when("I touch the checkbox")
def step_impl(context):
    pass


@then("A check mark appears in the box")
def step_impl(context):
    pass


@when("I touch the Continue button")
def step_impl(context):
    pass


@then("The login screen appears")
def step_impl(context):
    pass


@given("I see the Attention Alert Message")
def step_impl(context):
    assert login_view.element_is_present("AttentionAlertTitle", 10), "Expected Attention Alert Message but it did not appear"


@when("I touch OK")
def step_impl(context):
    login_view.click_element_by_name("AttentionOkButton")


@then("The Attention Alert Message disappears")
def step_impl(context):
    assert login_view.element_is_not_present("AttentionAlertTitle", 10), \
        "Expected Attention Alert Message to disappear but it did not"


@given("I see the Phone Permission Message")
def step_impl(context):
    assert login_view.element_is_present("PhonePermissionAlertTitle", 10), \
        "Expected Phone Permission Message but it did not appear"


@when("I touch ALLOW")
def step_impl(context):
    login_view.click_element_by_name("PermissionAllowButton")


@then("The Phone Permission Message disappears")
def step_impl(context):
    assert login_view.element_is_not_present("PhonePermissionAlertTitle", 10), \
        "Expected Phone Permission Message to disappear but it did not"


@given("I see the Record Audio Permission Message")
def step_impl(context):
    assert login_view.element_is_present("RecordAudioAlertTitle", 10), \
        "Expected Record Audio Permission Message but it did not appear"


@then("The Record Audio Permission Message disappears")
def step_impl(context):
    assert login_view.element_is_not_present("RecordAudioAlertTitle", 10), \
        "Expected Record Audio Permission Message to disappear but it did not"


@given("I see the Battery Usage Alert Message")
def step_impl(context):
    assert login_view.element_is_present("BatteryUsageAlertTitle", 10), "Expected Battery Usage Alert Message but it did not appear"


@when("I touch YES")
def step_impl(context):
    login_view.click_element_by_name("BatteryUsageYesButton")


@then("The Battery Usage Alert Message disappears")
def step_impl(context):
    assert login_view.element_is_not_present("BatteryUsageAlertTitle", 10), \
        "Expected Battery Usage Alert Message to disappear but it did not"
