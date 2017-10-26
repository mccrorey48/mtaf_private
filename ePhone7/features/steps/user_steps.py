from behave import *
from ePhone7.views import *
from lib.wrappers import fake
from lib.user_exception import UserException as Ux

headset_icon_rgbs = {'blue': [99, 139, 237, 369], 'green': [79, 187, 110, 367]}


@step("[user] A keypad appears")
@fake
def user__a_keypad_appears(context):
    pass


@step("[user] A keypad appears with a list of contacts")
@fake
def user__a_keypad_appears_with_a_list_of_contacts(context):
    pass


@step("[user] I enter the call park queue number")
@fake
def user__i_enter_the_call_park_queue_number(context):
    pass


@step("[user] I get the logo element from the home screen")
@fake
def user__i_get_the_logo_element_from_the_home_screen(context):
    context.logo_element = user_view.get_logo_element()


@step("[user] I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen")
@fake
def user__i_see_the_contacts_history_voicemail_and_dial_buttons_at_the_bottom_of_the_screen(context):
    assert user_view.Contacts is not None, "user_view.Contacts element not found"
    assert user_view.History is not None, "user_view.History element not found"
    assert user_view.Voicemail is not None, "user_view.Voicemail element not found"
    assert user_view.Dial is not None, "user_view.Dial element not found"


@step("[user] I touch a contact element")
@fake
def user__i_touch_a_contact_element(context):
    pass


@step("[user] I touch the Call Forward icon")
@fake
def user__i_touch_the_call_forward_icon(context):
    pass


@step("[user] I touch the Call Park icon")
@fake
def user__i_touch_the_call_park_icon(context):
    pass


@step("[user] I touch the Do Not Disturb icon")
@fake
def user__i_touch_the_do_not_disturb_icon(context):
    pass


@step("[user] I touch the Headset icon if it is {color}")
@fake
def user__i_touch_the_headset_icon_if_it_is_color(context, color):
    if color not in headset_icon_rgbs:
        raise Ux("Unknown color specified: %s" % color)
    icon = user_view.find_named_element("HeadsetButton")
    user_view.get_screenshot_as_png('headset_button')
    if user_view.get_element_color_and_count('headset_button', icon, color_list_index=1) == headset_icon_rgbs[color]:
        icon.click()


@step("[user] I touch the Home button")
@fake
def user__i_touch_the_home_button(context):
    user_view.send_keycode('KEYCODE_HOME')


@step("[user] I touch the Preferences icon")
@fake
def user__i_touch_the_preferences_icon(context):
    user_view.PrefsButton.click()
    # user_view.tap([(559, 74)])
    # if not prefs_view.element_is_present('Preferences'):
    #     # one retry
    #     user_view.tap([(559, 74)])
    # user_view.click_named_element('PrefsButton')


@step("[user] I use the keypad to filter the list of contacts")
@fake
def user__i_use_the_keypad_to_filter_the_list_of_contacts(context):
    pass


@step("[user] Only the contact I touched is listed")
@fake
def user__only_the_contact_i_touched_is_listed(context):
    pass


@step("[user] the Call Forward icon is blue")
@fake
def user__the_call_forward_icon_is_blue(context):
    pass


@step("[user] the Call Forward icon is red")
@fake
def user__the_call_forward_icon_is_red(context):
    pass


@step("[user] the Do Not Disturb icon is blue")
@fake
def user__the_do_not_disturb_icon_is_blue(context):
    pass


@step("[user] the Do Not Disturb icon is red")
@fake
def user__the_do_not_disturb_icon_is_red(context):
    pass


@step("[user] the Do Not Disturb icon turns blue")
@fake
def user__the_do_not_disturb_icon_turns_blue(context):
    pass


@step("[user] the Do Not Disturb icon turns red")
@fake
def user__the_do_not_disturb_icon_turns_red(context):
    pass


@step("[user] the Headset icon is {expect_color}")
@fake
def user__the_headset_icon_is_expectcolor(context, expect_color):
    if expect_color not in headset_icon_rgbs:
        raise Ux("Unknown color specified: %s" % expect_color)
    icon = user_view.find_named_element("HeadsetButton")
    user_view.get_screenshot_as_png('headset_button')
    actual_rgb = user_view.get_element_color_and_count('headset_button', icon, color_list_index=1)
    for color in headset_icon_rgbs:
        if actual_rgb == headset_icon_rgbs[color]:
            assert expect_color == color, "expected headset icon color %s, got %s" % (expect_color, color)
            break
    else:
        assert False, "expected color %s, got unknown (rgb counts = %s)" % (expect_color, actual_rgb)


@step("[user] the keypad disappears")
@fake
def user__the_keypad_disappears(context):
    pass


@step("[user] the logo width is at least {width} pixels")
@fake
def user__the_logo_width_is_at_least_width_pixels(context, width):
    assert int(context.logo_element.size['width']) >= int(width)


