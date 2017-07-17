from behave import *
from ePhone7.views import *
from lib.wrappers import fake


@step("[user] A keypad appears")
def user__a_keypad_appears(context):
    pass


@step("[user] A keypad appears with a list of contacts")
def user__a_keypad_appears_with_a_list_of_contacts(context):
    pass


@step("[user] I enter the call park queue number")
def user__i_enter_the_call_park_queue_number(context):
    pass


@step("[user] I get the logo element from the home screen")
@fake
def user__i_get_the_logo_element_from_the_home_screen(context):
    context.logo_element = user_view.get_logo_element()


@step("[user] I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen")
@fake
def user__i_see_the_contacts_history_voicemail_and_dial_buttons_at_the_bottom_of_the_screen(context):
    user_view.find_named_element('Contacts')
    user_view.find_named_element('History')
    user_view.find_named_element('Voicemail')
    user_view.find_named_element('Dial')


@step("[user] I touch a contact element")
def user__i_touch_a_contact_element(context):
    pass


@step("[user] I touch the Call Forward icon")
def user__i_touch_the_call_forward_icon(context):
    pass


@step("[user] I touch the Call Park icon")
def user__i_touch_the_call_park_icon(context):
    pass


@step("[user] I touch the Do Not Disturb icon")
def user__i_touch_the_do_not_disturb_icon(context):
    pass


@step("[user] I touch the Home button")
@fake
def user__i_touch_the_home_button(context):
    user_view.send_keycode('KEYCODE_HOME')


@step("[user] I touch the Preferences icon")
@fake
def user__i_touch_the_preferences_icon(context):
    user_view.tap([(559, 74)])
    if not prefs_view.element_is_present('Preferences'):
        # one retry
        user_view.tap([(559, 74)])
    # user_view.click_named_element('PrefsButton')


@step("[user] I use the keypad to filter the list of contacts")
def user__i_use_the_keypad_to_filter_the_list_of_contacts(context):
    pass


@step("[user] Only the contact I touched is listed")
def user__only_the_contact_i_touched_is_listed(context):
    pass


@step("[user] the Call Forward icon is blue")
def user__the_call_forward_icon_is_blue(context):
    pass


@step("[user] the Call Forward icon is red")
def user__the_call_forward_icon_is_red(context):
    pass


@step("[user] the Do Not Disturb icon is blue")
def user__the_do_not_disturb_icon_is_blue(context):
    pass


@step("[user] the Do Not Disturb icon is red")
def user__the_do_not_disturb_icon_is_red(context):
    pass


@step("[user] the Do Not Disturb icon turns blue")
def user__the_do_not_disturb_icon_turns_blue(context):
    pass


@step("[user] the Do Not Disturb icon turns red")
def user__the_do_not_disturb_icon_turns_red(context):
    pass


@step("[user] the keypad disappears")
def user__the_keypad_disappears(context):
    pass


@step("[user] the logo width is at least {width} pixels")
@fake
def user__the_logo_width_is_at_least_width_pixels(context, width):
    assert int(context.logo_element.size['width']) >= int(width)


