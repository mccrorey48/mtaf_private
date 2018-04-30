from time import sleep, time

from behave import *

from mtaf import mtaf_logging
from ePhone7.config.configure import cfg
from ePhone7.views import *
from mtaf.user_exception import UserException as Ux
from mtaf.trace import fake
from ePhone7.lib.utils.e7_microservices import get_vmids

log = mtaf_logging.get_logger('mtaf.active_steps')


@step('[active call] I touch "Dial"')
@fake
def active_call__i_touch_dial(context):
    active_call_view.click_named_element('InCallDial')


@step("[active call] the active call screen appears")
@fake
def active_call__the_active_call_screen_appears(context):
    assert active_call_view.becomes_present(), 'Active call screen not present'


@step("[active_call] a Record button is visible")
@fake
def activecall__a_record_button_is_visible(context):
    assert active_call_view.element_is_present('CallRecordButton')
    context.record_button = active_call_view.find_named_element('CallRecordButton')


@step('[active_call] an "Active Call" window appears')
@fake
def activecall__an_active_call_window_appears(context):
    assert active_call_view.becomes_present()


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


@step("[active_call] I see the keypad")
@fake
def activecall__i_see_the_keypad(context):
    assert active_call_view.element_is_present('InCallDialpad')


@step("[active_call] I select a coworker's mailbox")
@fake
def activecall__i_select_a_coworkers_mailbox(context):
    # before forwarding the call to the coworker, count the voicemails in that mailbox
    # so we can verify later that a new one has been added
    context.vmid_count = len(get_vmids(cfg.site['DefaultForwardAccount'], 'new'))
    active_call_view.touch_default_forward_account_name()


@step("[active_call] I select the Favorites tab")
@fake
def activecall__i_select_the_favorites_tab(context):
    pass


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


@step("[active_call] my Coworker contacts are listed on the contacts screen")
@fake
def activecall__my_coworker_contacts_are_listed_on_the_contacts_screen(context):
    pass


@step("[active_call] my favorite Coworker contacts are listed")
@fake
def activecall__my_favorite_coworker_contacts_are_listed(context):
    pass


@step("[active_call] the buttons are {w} pixels wide and {h} pixels high")
@fake
def activecall__the_buttons_are_w_pixels_wide_and_h_pixels_high(context, w, h):
    elems = active_call_view.find_named_elements('InCallDialKeys')
    # location = elems[0].location
    # assert location['x'] == 54 and location['y'] == 403, "Expected key 1 location (54, 403), got (%d, %d)" \
    #                                                      % (location['x'], location['y'])
    size = elems[0].size
    assert size['width'] == int(w) and size['height'] == int(h), "Expected key 1 size %dw, %dh), got %dh, %dw" \
                                                                 % (int(w), int(h), size['width'], size['height'])


@step("[active_call] the caller leaves a message and hangs up")
@fake
def activecall__the_caller_leaves_a_message_and_hangs_up(context):
    user_view.caller_leaves_voicemail()
    user_view.caller_ends_received_call()
    start_time = time()
    api_timeout = 60
    while time() - start_time < api_timeout:
        if len(get_vmids('DefaultForwardAccount', 'new')) > context.vmid_count:
            break
    else:
        raise Ux('vmid count not incremented before %s second timeout' % api_timeout)


@step("[active_call] the Coworkers tab is selected")
@fake
def activecall__the_coworkers_tab_is_selected(context):
    pass


@step("[active_call] the {expect_icon} icon is displayed")
@fake
def activecall__the_expecticon_icon_is_displayed(context, expect_icon):
    white_counts = {'speaker': 714, 'handset': 580, 'headset': 618}
    if expect_icon not in white_counts:
        raise Ux("Unexpected expect_icon value: %s" % expect_icon)
    call_icon = active_call_view.find_named_element('AudioPathIcon')
    user_view.get_screenshot_as_png('call_icon')
    expected_count = white_counts[expect_icon]
    actual_count = active_call_view.get_element_color_and_count('call_icon', call_icon)[-1]
    for icon in white_counts:
        if white_counts[icon] == actual_count:
            assert actual_count == expected_count, "Expected %s icon, got %s" % (expect_icon, icon)
            break
    else:
        assert False, "Expected %s icon, got unknown (white pixel count = %d" % (expect_icon, actual_count)


@step("[active_call] the in-call contacts screen appears")
@fake
def activecall__the_incall_contacts_screen_appears(context):
    pass


@step("[active_call] the Record button is gray")
@fake
def activecall__the_record_button_is_gray(context):
    user_view.get_screenshot_as_png('record_button')
    expected_color = [38, 40, 43]
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


