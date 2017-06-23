from behave import *
from ePhone7.views import *
from lib.wrappers import fake


@step("[active_call] a Record button is visible")
@fake
def activecall__a_record_button_is_visible(context):
    assert user_view.element_is_present('CallRecordButton')
    context.record_button = user_view.find_named_element('CallRecordButton')


@step('[active_call] an "Active Call" window appears')
def activecall__an_active_call_window_appears(context):
    pass


@step("[active_call] I end the call")
@fake
def activecall__i_end_the_call(context):
    user_view.end_call()


@when("[active_call] I select a coworker's mailbox")
def activecall__i_select_a_coworkers_mailbox(context):
    pass


@when('[active_call] I tap "Transfer to VM"')
def activecall__i_tap_transfer_to_vm(context):
    pass


@then('[active_call] I touch "OK" to complete the voicemail transfer')
def activecall__i_touch_ok_to_complete_the_voicemail_transfer(context):
    pass


@step("[active_call] the Record button is gray")
@fake
def activecall__the_record_button_is_gray(context):
    user_view.get_screenshot_as_png('record_button')
    expected_color = [119, 120, 122]
    actual_color = user_view.get_element_color('record_button', context.record_button)
    assert actual_color == expected_color, "expected color %s, got %s" % (expected_color, actual_color)


@step("[active_call] the Record button is white")
@fake
def activecall__the_record_button_is_white(context):
    user_view.get_screenshot_as_png('record_button')
    expected_color = [255, 255, 255]
    actual_color = user_view.get_element_color('record_button', context.record_button)
    assert actual_color == expected_color, "expected color %s, got %s" % (expected_color, actual_color)


@then('[active_call] the transfer dialpad appears')
def activecall__the_transfer_dialpad_appears(context):
    pass


