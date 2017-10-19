from behave import *
from ePhone7.views import *
from lib.wrappers import fake
from ePhone7.config.configure import cfg
from time import sleep
from ePhone7.utils.get_softphone import get_softphone


@step("[voicemail] A keypad appears")
@fake
def voicemail__a_keypad_appears(context):
    pass


@step("[voicemail] A list of Coworker contacts appears")
@fake
def voicemail__a_list_of_coworker_contacts_appears(context):
    pass


@step("[voicemail] A voicemail detail window appears")
@fake
def voicemail__a_voicemail_detail_window_appears(context):
    assert voicemail_view.element_is_present("PlaybackStartStop"), '"PlaybackStartStop" element not present after 10 seconds'


@step("[voicemail] I can choose Cancel or OK by touching the corresponding button")
@fake
def voicemail__i_can_choose_cancel_or_ok_by_touching_the_corresponding_button(context):
    pass


@step("[voicemail] I see my existing new voicemails")
@fake
def voicemail__i_see_my_existing_new_voicemails(context):
    parents = voicemail_view.get_top_vm_parents()
    context.existing_vm_parent_texts = []
    for parent in parents:
        context.existing_vm_parent_texts.append({
            "CallerName": voicemail_view.find_named_sub_element(parent, "CallerName").text,
            "CallerNumber": voicemail_view.find_named_sub_element(parent, "CallerNumber").text,
            "CalledTime": voicemail_view.find_named_sub_element(parent, "CalledTime").text,
            "VmDuration": voicemail_view.find_named_sub_element(parent, "VmDuration").text
        })


@step("[voicemail] I see the New, Saved and Trash tabs at the top of the screen")
@fake
def voicemail__i_see_the_new_saved_and_trash_tabs_at_the_top_of_the_screen(context):
    assert voicemail_view.element_is_present('New')
    assert voicemail_view.element_is_present('Saved')
    assert voicemail_view.element_is_present('Trash')


@step("[voicemail] I touch a contact element")
@fake
def voicemail__i_touch_a_contact_element(context):
    pass


@step("[voicemail] I touch the Delete icon")
@fake
def voicemail__i_touch_the_delete_icon(context):
    pass


@step("[voicemail] I touch the Forward icon")
@fake
def voicemail__i_touch_the_forward_icon(context):
    pass


@step("[voicemail] I touch the handset icon")
@fake
def voicemail__i_touch_the_handset_icon(context):
    context.softphone = get_softphone()
    context.softphone.set_incoming_response(200)
    voicemail_view.click_named_element('VmCallButton')


@step("[voicemail] I touch the new voicemail element")
@fake
def voicemail__i_touch_the_new_voicemail_element(context):
    context.top_vm_parent.click()


@step("[voicemail] I touch the Save icon")
@fake
def voicemail__i_touch_the_save_icon(context):
    pass


@step("[voicemail] I touch the voicemail element")
@fake
def voicemail__i_touch_the_voicemail_element(context):
    pass


@step("[voicemail] I use the keypad to filter the list of contacts")
@fake
def voicemail__i_use_the_keypad_to_filter_the_list_of_contacts(context):
    pass


@step("[voicemail] the new voicemail is the first item listed")
@fake
def voicemail__the_new_voicemail_is_the_first_item_listed(context):
    sleep(10)
    parents = voicemail_view.get_top_vm_parents()
    context.top_vm_parent = parents[0]
    new_vm_parent_texts = []
    for parent in parents:
        new_vm_parent_texts.append({
            "CallerName": voicemail_view.find_named_sub_element(parent, "CallerName").text,
            "CallerNumber": voicemail_view.find_named_sub_element(parent, "CallerNumber").text,
            "CalledTime": voicemail_view.find_named_sub_element(parent, "CalledTime").text,
            "VmDuration": voicemail_view.find_named_sub_element(parent, "VmDuration").text
        })
    expect_name = cfg.site["DefaultSoftphoneUser"]
    got_name = new_vm_parent_texts[0]["CallerName"]
    assert got_name == expect_name, "Expect first CallerName to be %s, got %s" % (expect_name, got_name)
    for i in range(len(parents) - 1):
        # for text_name in "CallerName", "CallerNumber", "CalledTime", "VmDuration":
        # CalledTime changes since existing vms were checked so don't compare those values
        for text_name in "CallerName", "CallerNumber", "VmDuration":
            expect_name = context.existing_vm_parent_texts[i][text_name]
            got_name = new_vm_parent_texts[i + 1][text_name]
            assert got_name == expect_name, "Index %d: expect first %s to be %s, got %s" % (
                i, text_name, expect_name, got_name)


@step("[voicemail] the voicemail audio plays back")
@fake
def voicemail__the_voicemail_audio_plays_back(context):
    elem = voicemail_view.find_named_element("PlaybackStartStop")
    voicemail_view.get_screenshot_as_png('playback')
    color = voicemail_view.get_element_color_and_count('playback', elem, color_list_index=0)
    assert color[:3] == [56, 62, 77], "Voicemail playback/start/stop wrong color, expected (56, 62, 77), got %s" % color[:3]
    assert color[3] == 38160, "Voicemail paused, should be playing back (1st color count %s, expected %s" % (color[3], 38160)


@step("[voicemail] the voicemail detail window disappears")
@fake
def voicemail__the_voicemail_detail_window_disappears(context):
    assert voicemail_view.element_is_present("EndCall"), '"EndCall" element not present after 10 seconds'


@step("[voicemail] the voicemail is also available in the destination contact's new voicemails list")
@fake
def voicemail__the_voicemail_is_also_available_in_the_destination_contacts_new_voicemails_list(context):
    pass


@step("[voicemail] the voicemail is no longer listed")
@fake
def voicemail__the_voicemail_is_no_longer_listed(context):
    pass


@step("[voicemail] the voicemail is still the first item in the view")
@fake
def voicemail__the_voicemail_is_still_the_first_item_in_the_view(context):
    pass


@step("[voicemail] the voicemail is the first item listed")
@fake
def voicemail__the_voicemail_is_the_first_item_listed(context):
    pass


@step("[voicemail] the Voicemail view appears")
@fake
def voicemail__the_voicemail_view_appears(context):
    pass


@step("[voicemail] my phone calls the voicemail sender")
@fake
def my_phone_calls_the_voicemail_sender(context):
    context.softphone.wait_for_call_status('call', user_view.call_status_wait)


