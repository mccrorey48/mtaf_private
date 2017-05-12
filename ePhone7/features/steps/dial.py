from behave import *
from ePhone7.views import *


@step("[dial] I dial the {code_name} direct code")
def dial__i_dial_the_codename_direct_code(context, code_name):
    if 'fake' not in str(context._config.tags).split(','):
        dial_view.dial_name(code_name)


@step("[dial] I enter a 10-digit phone number using the keypad")
def dial__i_enter_a_10digit_phone_number_using_the_keypad(context):
    pass


@step("[dial] I enter a Coworker contact number using the keypad")
def dial__i_enter_a_coworker_contact_number_using_the_keypad(context):
    pass


@step("[dial] I touch the Call button")
def dial__i_touch_the_call_button(context):
    if 'fake' not in str(context._config.tags).split(','):
        dial_view.click_named_element('FuncKeyCall')


@step("[dial] the Dial view appears")
def dial__the_dial_view_appears(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert dial_view.element_is_present('DialPad')


