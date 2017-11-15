from behave import *
from ePhone7.views import *
from lib.wrappers import fake
from ePhone7.config.configure import cfg
from ePhone7.utils.get_softphone import get_softphone
from ePhone7.utils.vvm_microservice import *
from time import time
import lib.logging_esi
from lib.filters import get_filter
from lib.user_exception import UserException as Ux
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


@step("[voicemail] I see my existing {category} voicemails")
@fake
def step_impl(context, category):
    vm_displayed_texts = voicemail_view.get_top_vm_texts()
    metadata = get_vm_metadata('R2d2User', category)
    context.existing_vm_metadata[category.lower()] = metadata
    fail_msg = "visible VM's did not match VM's from vvm API"
    assert all_views.voicemail.vm_match_all(vm_displayed_texts, metadata), fail_msg


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
    parents = voicemail_view.get_top_vm_parents()
    assert len(parents) > 0, "No VM parents found"
    parents[0].click()


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


@step('[voicemail] the new voicemail is no longer listed as "{vm_type}"')
@fake
def voicemail__the_new_voicemail_is_no_longer_listed(context, vm_type):
    start_time = time()
    timeout = 60
    vms_visible = []
    # wait timeout seconds for the new VM to disappear
    # if it's not the NEW tab, we haven't recorded whether or not there were already VMS (SAVED or TRASH) so:
    #     - if there are no VMs visible, the step passes (break the while loop)
    #     - if there is at least one VM visible:
    #           - if duration matches the new VM, keep waiting until timeout (continue the while loop)
    #           - else  the step passes (break the while loop)
    # if it's the NEW tab, we have a list of existing VM texts, so:
    #     - if there are no VMs visible:
    #           - if the list of existing VMs is not empty, it's an error, the visible list should never be empty
    #           - otherwise the step passes (break the while loop)
    #     - if there is at least one VM visible:
    #           - if the duration doesn't match the new VM's duration, the step passes (break the while loop)
    #           - else keep waiting (continue the while loop)
    context.top_vm = None
    while time() - start_time < timeout:
        vms_visible = voicemail_view.get_top_vm_parents()
        if vm_type != "NEW":
            if len(vms_visible) == 0:
                break
            else:
                context.top_vm = vms_visible[0]
                top_duration = voicemail_view.find_named_sub_element(vms_visible[0], 'VmDuration').text
                if top_duration == context.new_vm_duration:
                    continue
                break
        else:
            if len(vms_visible) == 0:
                assert len(context.existing_new_vm_texts) == 0, "unexpected empty NEW VM list"
                break
            else:
                top_duration = voicemail_view.find_named_sub_element(vms_visible[0], 'VmDuration').text
                if top_duration != context.new_vm_duration:
                    break
                continue
    else:
        assert False, "New voicemail did not disappear from top of %s list in %s seconds" % (vm_type, timeout)


@step("[voicemail] the new voicemail is the first \"{category}\" item listed")
@fake
def voicemail__the_new_voicemail_is_the_first_vmtype_item_listed(context, category):
    start_time = time()  # compare both timeouts to this start time
    api_timeout = 30
    view_timeout = 60
    # wait timeout seconds for the new VM to appear in both the VM metadata and on the ePhone7 display
    while time() - start_time < api_timeout:
        metadata = get_vm_metadata('R2d2User', category)
        if metadata[0]['vmid'] != context.existing_vm_metadata[category.lower()][0]['vmid']:
            break
    else:
        raise Ux('New voicemail not reported by vvm API within %d seconds' % api_timeout)
    context.new_vmid = metadata[0]['vmid']
    while time() - start_time < view_timeout:
        vm_displayed_texts = voicemail_view.get_top_vm_texts()
        if voicemail_view.vm_match_all(vm_displayed_texts, metadata):
            break
    else:
        assert False, "New voicemail did not appear at top of %s list in %s seconds" % (category, view_timeout)


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
