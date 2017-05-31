from behave import *
from ePhone7.views import *
from lib.wrappers import fake

@step("[voicemail] A keypad appears")
def voicemail__a_keypad_appears(context):
    pass


@step("[voicemail] A list of Coworker contacts appears")
def voicemail__a_list_of_coworker_contacts_appears(context):
    pass


@step("[voicemail] A voicemail detail window appears")
def voicemail__a_voicemail_detail_window_appears(context):
    pass


@step("[voicemail] I can choose Cancel or OK by touching the corresponding button")
def voicemail__i_can_choose_cancel_or_ok_by_touching_the_corresponding_button(context):
    pass


@step("[voicemail] I see the New, Saved and Trash tabs at the top of the screen")
@fake
def voicemail__i_see_the_new_saved_and_trash_tabs_at_the_top_of_the_screen(context):
    assert voicemail_view.element_is_present('New')
    assert voicemail_view.element_is_present('Saved')
    assert voicemail_view.element_is_present('Trash')


@step("[voicemail] I touch a contact element")
def voicemail__i_touch_a_contact_element(context):
    pass


@step("[voicemail] I touch OK")
def voicemail__i_touch_ok(context):
    pass


@step("[voicemail] I touch the Delete icon")
def voicemail__i_touch_the_delete_icon(context):
    pass


@step("[voicemail] I touch the Forward icon")
def voicemail__i_touch_the_forward_icon(context):
    pass


@step("[voicemail] I touch the handset icon")
def voicemail__i_touch_the_handset_icon(context):
    pass


@step("[voicemail] I touch the New tab")
def voicemail__i_touch_the_new_tab(context):
    pass


@step("[voicemail] I touch the new voicemail element")
def voicemail__i_touch_the_new_voicemail_element(context):
    pass


@step("[voicemail] I touch the Save icon")
def voicemail__i_touch_the_save_icon(context):
    pass


@step("[voicemail] I touch the Saved tab")
def voicemail__i_touch_the_saved_tab(context):
    pass


@step("[voicemail] I touch the Trash tab")
def voicemail__i_touch_the_trash_tab(context):
    pass


@step("[voicemail] I touch the voicemail element")
def voicemail__i_touch_the_voicemail_element(context):
    pass


@step("[voicemail] I use the keypad to filter the list of contacts")
def voicemail__i_use_the_keypad_to_filter_the_list_of_contacts(context):
    pass


@step("[voicemail] the new voicemail is the first item listed")
def voicemail__the_new_voicemail_is_the_first_item_listed(context):
    pass


@step("[voicemail] the voicemail audio plays back")
def voicemail__the_voicemail_audio_plays_back(context):
    pass


@step("[voicemail] the voicemail detail window disappears")
def voicemail__the_voicemail_detail_window_disappears(context):
    pass


@step("[voicemail] the voicemail is also available in the destination contact's new voicemails list")
def voicemail__the_voicemail_is_also_available_in_the_destination_contacts_new_voicemails_list(context):
    pass


@step("[voicemail] the voicemail is no longer listed")
def voicemail__the_voicemail_is_no_longer_listed(context):
    pass


@step("[voicemail] the voicemail is still the first item in the view")
def voicemail__the_voicemail_is_still_the_first_item_in_the_view(context):
    pass


@step("[voicemail] the voicemail is the first item listed")
def voicemail__the_voicemail_is_the_first_item_listed(context):
    pass


@step("[voicemail] the Voicemail view appears")
def voicemail__the_voicemail_view_appears(context):
    pass


