from behave import *
from ePhone7.views import *
from lib.wrappers import fake
from ePhone7.config.configure import cfg
from time import sleep
from ePhone7.utils.get_softphone import get_softphone
from time import time
import lib.logging_esi
from lib.filters import get_filter
log = lib.logging_esi.get_logger('esi.vm_steps')


@step("[voicemail] a keypad appears")
@fake
def voicemail__a_keypad_appears(context):
    assert voicemail_view.RootFrameLayout.size['height'] == 610


@step("[voicemail] a list of Coworker contacts appears")
@fake
def voicemail__a_list_of_coworker_contacts_appears(context):
    assert voicemail_view.ForwardDialogTitle is not None, '"ForwardDialogTitle" element not present after 10 seconds'


@step("[voicemail] a voicemail detail window appears")
@fake
def voicemail__a_voicemail_detail_window_appears(context):
    assert voicemail_view.PlaybackStartStop is not None, '"PlaybackStartStop" element not present after 10 seconds'


@step("[voicemail] I can choose Cancel or OK by touching the corresponding button")
@fake
def voicemail__i_can_choose_cancel_or_ok_by_touching_the_corresponding_button(context):
    pass


@step("[voicemail] I see my existing new voicemails")
@fake
def voicemail__i_see_my_existing_new_voicemails(context):
    parents = voicemail_view.get_top_vm_parents()
    context.existing_new_vm_texts = []
    for parent in parents:
        context.existing_new_vm_texts.append({
            "CallerName": voicemail_view.find_named_sub_element(parent, "CallerName").text,
            "CallerNumber": voicemail_view.find_named_sub_element(parent, "CallerNumber").text,
            "CalledTime": voicemail_view.find_named_sub_element(parent, "CalledTime").text,
            "VmDuration": voicemail_view.find_named_sub_element(parent, "VmDuration").text
        })
    log.debug('VM_DEBUG I see my existing new voicemails: %s' % context.existing_new_vm_texts)


@step("[voicemail] I see the New, Saved and Trash tabs at the top of the screen")
@fake
def voicemail__i_see_the_new_saved_and_trash_tabs_at_the_top_of_the_screen(context):
    assert voicemail_view.New, "voicemail_view.New element not present"
    assert voicemail_view.Saved, "voicemail_view.Saved element not present"
    assert voicemail_view.Trash, "voicemail_view.Trash element not present"


@step("[voicemail] I touch a contact element")
@fake
def voicemail__i_touch_a_contact_element(context):
    voicemail_view.all.SearchItem[0].click()


@step("[voicemail] I touch the Delete icon")
@fake
def voicemail__i_touch_the_delete_icon(context):
    voicemail_view.DeleteButton.click()


@step("[voicemail] I touch the Forward icon")
@fake
def voicemail__i_touch_the_forward_icon(context):
    voicemail_view.ForwardButton.click()


@step("[voicemail] I touch the handset icon")
@fake
def voicemail__i_touch_the_handset_icon(context):
    context.softphone = get_softphone()
    context.softphone.set_incoming_response(200)
    voicemail_view.click_named_element('VmCallButton')


@step("[voicemail] I touch the Save icon")
@fake
def voicemail__i_touch_the_save_icon(context):
    voicemail_view.SaveButton.click()


@step("[voicemail] I touch the top voicemail element")
@fake
def voicemail__i_touch_the_top_voicemail_element(context):
    context.top_vm.click()


@step("[voicemail] I use the keypad to filter the list of contacts")
@fake
def voicemail__i_use_the_keypad_to_filter_the_list_of_contacts(context):
    frame = voicemail_view.ForwardList
    items = filter(get_filter('within_frame', frame=frame), voicemail_view.all.SearchItem)
    assert len(items) > 1, "Expected number of search items > 1, got %d" % len(items)
    voicemail_view.ForwardText.send_keys(cfg.site['Users'][cfg.site['DefaultForwardAccount']['UserId']])
    frame = voicemail_view.ForwardList
    items = filter(get_filter('within_frame', frame=frame), voicemail_view.all.SearchItem)
    assert len(items) == 1, "Expected number of search items to be 1, got %d" % len(items)


@step("[voicemail] my phone calls the voicemail sender")
@fake
def voicemail__my_phone_calls_the_voicemail_sender(context):
    context.softphone.wait_for_call_status('call', user_view.call_status_wait)


@step("[voicemail] the new voicemail is no longer listed")
@fake
def voicemail__the_new_voicemail_is_no_longer_listed(context):
    sleep(10)
    parents = voicemail_view.get_top_vm_parents()
    if len(parents) > 0:
        caller_name = voicemail_view.find_named_sub_element(parents[0], "CallerName").text
        caller_number = voicemail_view.find_named_sub_element(parents[0], "CallerNumber").text
        vm_duration = voicemail_view.find_named_sub_element(parents[0], "VmDuration").text
        context.make_assertion("First VM item does not match new VM", True, (
            context.new_vm_text["CallerName"] != caller_name
            or context.new_vm_text["CallerNumber"] != caller_number
            or context.new_vm_text["VmDuration"] != vm_duration))


@step("[voicemail] the new voicemail is the first \"{vm_type}\" item listed")
@fake
def voicemail__the_new_voicemail_is_the_first_vmtype_item_listed(context, vm_type):
    start_time = time()
    timeout = 60
    vms_visible = []
    while time() - start_time < timeout:
        vms_visible = voicemail_view.get_top_vm_parents()
        if len(vms_visible):
            if vm_type != "NEW":
                break
            if len(vms_visible) > 1 and voicemail_view.find_named_sub_element(
                    vms_visible[1], "VmDuration").text == context.existing_new_vm_texts[0]["VmDuration"]:
                break
    else:
        assert False, "New voicemail did not appear at top of %s list in %s seconds" % (vm_type, timeout)
    context.top_vm = vms_visible[0]
    if vm_type == "NEW":
        vm_texts = []
        for vm in vms_visible:
            vm_texts.append({
                "CallerName": voicemail_view.find_named_sub_element(vm, "CallerName").text,
                "CallerNumber": voicemail_view.find_named_sub_element(vm, "CallerNumber").text,
                "CalledTime": voicemail_view.find_named_sub_element(vm, "CalledTime").text,
                "VmDuration": voicemail_view.find_named_sub_element(vm, "VmDuration").text
            })
        context.new_vm_text = vm_texts[0]
        expect_name = cfg.site["DefaultSoftphoneUser"]
        got_name = context.new_vm_text["CallerName"]
        context.make_assertion("first CallerName", expect_name, got_name)
        for i in range(len(vms_visible) - 1):
            # CalledTime changes since existing vms were checked so don't compare those values
            for text_name in "CallerName", "CallerNumber", "VmDuration":
                expect_name = context.existing_new_vm_texts[i][text_name]
                got_name = vm_texts[i + 1][text_name]
                context.make_assertion("Index %d: %s" % (i, text_name), expect_name, got_name)


@step("[voicemail] the voicemail audio plays back")
@fake
def voicemail__the_voicemail_audio_plays_back(context):
    elem = voicemail_view.find_named_element("PlaybackStartStop")
    voicemail_view.get_screenshot_as_png('playback')
    color = voicemail_view.get_element_color_and_count('playback', elem, color_list_index=0)
    assert color[:3] == [56, 62, 77], \
        "Voicemail playback/start/stop wrong first color, expected (56, 62, 77), got %s" % color[:3]
    # paused: color[3] == 10930     playing: color[3] == 38160
    assert color[3] == 38160, \
        "Voicemail paused, should be playing back (1st color count %s, expected %s" % (color[3], 38160)


@step("[voicemail] the voicemail detail window disappears")
@fake
def voicemail__the_voicemail_detail_window_disappears(context):
    assert voicemail_view.missing.PlaybackStartStop is True, '"PlaybackStartStop" element present after 10 seconds'


@step("[voicemail] the voicemail is also available in the destination contact's new voicemails list")
@fake
def voicemail__the_voicemail_is_also_available_in_the_destination_contacts_new_voicemails_list(context):
    pass


@step("[voicemail] the voicemail is still the first item in the view")
@fake
def voicemail__the_voicemail_is_still_the_first_item_in_the_view(context):
    pass


@step("[voicemail] the Voicemail view appears")
@fake
def voicemail__the_voicemail_view_appears(context):
    pass
