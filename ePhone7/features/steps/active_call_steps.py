from behave import *
from ePhone7.views import *
from lib.wrappers import fake
from ePhone7.config.configure import cfg
from time import sleep
import lib.logging_esi as logging
log = logging.get_logger('esi.active_steps')


@step("[active call] the active call screen appears")
@fake
def active_call__the_active_call_screen_appears(context):
    assert active_call_view.is_present(), 'Active call screen not present'


@step("[active_call] a Record button is visible")
@fake
def activecall__a_record_button_is_visible(context):
    assert user_view.element_is_present('CallRecordButton')
    context.record_button = user_view.find_named_element('CallRecordButton')


@step('[active_call] an "Active Call" window appears')
@fake
def activecall__an_active_call_window_appears(context):
    assert active_call_view.is_present()


@step("[active_call] I end the call")
@fake
def activecall__i_end_the_call(context):
    active_call_view.touch_end_call_button()


@step("[active_call] I see a green banner with the coworker's name")
@fake
def activecall__i_see_a_green_banner_with_the_coworkers_name(context):
    assert active_call_view.vm_xfer_dest_banner_present(), "vm transfer destination banner not present"
    expect_name = cfg.site['DefaultForwardAccount']
    actual_name = active_call_view.vm_xfer_dest_name()
    assert actual_name == expect_name, "expect vm transfer destination name = %s, got %s" % (expect_name, actual_name)


@step("[active_call] I see an orange banner with the caller's name")
@fake
def activecall__i_see_an_orange_banner_with_the_callers_name(context):
    assert active_call_view.vm_xfer_caller_banner_present()
    expect_name = cfg.site['DefaultSoftphoneUser']
    actual_name = active_call_view.vm_xfer_caller_name()
    assert actual_name == expect_name, "expect vm transfer caller name = %s, got %s" % (expect_name, actual_name)


@step("[active_call] I select a coworker's mailbox")
@fake
def activecall__i_select_a_coworkers_mailbox(context):
    # before forwarding the call to the coworker, count the voicemails in that mailbox
    # so we can verify later that a new one has been added
    context.vmid_count = len(voicemail_view.get_vmids(username=cfg.site['DefaultForwardAccount']))
    active_call_view.touch_default_forward_account_name()


@step('[active_call] I tap "Transfer to VM"')
@fake
def activecall__i_tap_transfer_to_vm(context):
    active_call_view.touch_transfer_to_vm()


@step('[active_call] I touch the "end call" button')
@fake
def activecall__i_touch_the_end_call_button(context):
    # this has a 5 second sleep because it is used after a transfer-to-voicemail
    # and the button is not immediately responsive
    sleep(5)
    active_call_view.touch_end_call_button()


@step("[active_call] the caller leaves a message and hangs up")
@fake
def activecall__the_caller_leaves_a_message_and_hangs_up(context):
    user_view.caller_leaves_voicemail()
    user_view.caller_ends_received_call()
    sleep(10)
    new_vmids = voicemail_view.get_vmids(username=cfg.site['DefaultForwardAccount'])
    new_count = len(new_vmids)
    expect_count = context.vmid_count + 1
    assert new_count == expect_count, "expected vmid count %d, got %d" % (expect_count, new_count)


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


@step('[active_call] the transfer dialog appears')
@fake
def activecall__the_transfer_dialog_appears(context):
    assert active_call_view.transfer_dialog_is_present()


