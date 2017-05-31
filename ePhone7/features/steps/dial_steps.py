from behave import *
from ePhone7.views import *


@step("[dial] A list of contacts containing the partial number appears above the keypad")
def dial__a_list_of_contacts_containing_the_partial_number_appears_above_the_keypad(context):
    pass


@step("[dial] A list of Coworker contacts containing the partial name appears above the keypad")
def dial__a_list_of_coworker_contacts_containing_the_partial_name_appears_above_the_keypad(context):
    pass


@step("[dial] A list of Personal contacts containing the partial name appears above the keypad")
def dial__a_list_of_personal_contacts_containing_the_partial_name_appears_above_the_keypad(context):
    pass


@step("[dial] I dial the {code_name} direct code")
def dial__i_dial_the_codename_direct_code(context, code_name):
    if 'fake' not in str(context._config.tags).split(','):
        if code_name == "Advanced Settings":
            dial_view.dial_star_1987()
        else:
            dial_view.dial_named_number(code_name)


@step("[dial] I enter a 10-digit phone number using the keypad")
def dial__i_enter_a_10digit_phone_number_using_the_keypad(context):
    pass


@step("[dial] I enter a Coworker contact number using the keypad")
def dial__i_enter_a_coworker_contact_number_using_the_keypad(context):
    pass


@step("[dial] I enter part of a Coworker contact number using the keypad")
def dial__i_enter_part_of_a_coworker_contact_number_using_the_keypad(context):
    pass


@step("[dial] I see the keypad")
def dial__i_see_the_keypad(context):
    pass


@step("[dial] I touch the Call button")
def dial__i_touch_the_call_button(context):
    if 'fake' not in str(context._config.tags).split(','):
        dial_view.touch_dial_button()


@step("[dial] I touch the contact listing I want to call")
def dial__i_touch_the_contact_listing_i_want_to_call(context):
    pass


@step("[dial] Only the contact I touched is listed")
def dial__only_the_contact_i_touched_is_listed(context):
    pass


@step("[dial] the Dial view appears")
def dial__the_dial_view_appears(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert dial_view.element_is_present('DialPad')


