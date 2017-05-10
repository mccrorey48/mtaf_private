from behave import *
from ePhone7.views import *
from time import sleep


@step("[dial] I dial the {code_name} direct code")
def dial__i_dial_the_codename_direct_code(context, code_name):
    if 'fake' not in str(context._config.tags).split(','):
        dial_view.dial_name(code_name)


@step("[dial] I touch the Call button")
def dial__i_touch_the_call_button(context):
    if 'fake' not in str(context._config.tags).split(','):
        dial_view.click_named_element('FuncKeyCall')


@step("[dial] the Dial view appears")
def dial__the_dial_view_appears(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert dial_view.element_is_present('DialPad')


