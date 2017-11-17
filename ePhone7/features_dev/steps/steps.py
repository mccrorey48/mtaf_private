from behave import *
from ePhone7.views import all_views
from lib.wrappers import fake
from ePhone7.utils.vvm_microservice import *

use_step_matcher("re")


@step("the (?P<view>\S+) view (?P<name>\S+) element is (?P<mode>\S*)\s?present")
@fake
def step_impl(context, view, name, mode):
    if mode.lower() == 'not':
        assert all_views[view][name] is None, '%s view element "%s" is present' % (view, name)
    else:
        assert all_views[view][name], '%s view element "%s" is not present' % (view, name)


@step("the (?P<view>\S+) view is (?P<mode>\S*)\s?present")
@fake
def step_impl(context, view, mode):
    if mode.lower() == 'not':
        assert all_views[view].becomes_not_present(), "%s view is present"
    else:
        assert all_views[view].becomes_present(), "%s view is not present"


# @step('I touch (?:[^"]*)?"(?P<text>[^"]+)"(?P<tail>[^"]*)')
@step('I touch (?:the )?"(?P<text>[^"]+)"(?P<tail>[^"]*)')
@fake
def i_touch_ptextptail(context, text, tail):
    # matches: I touch <optional> "<text>" <optional>
    # where <optional> and <text> are any text not including a double quote
    # then looks for an element with full text content matching <text>
    if tail == 'tab':
        all_views.user.goto_tab(text)
    else:
        all_views.base.touch_element_with_text(text)


@step("I send the (?P<name>\S+) keycode")
@fake
def step_impl(context, name):
    all_views.base.send_keycode('KEYCODE_%s' % name.upper())


@step('a (?:[^"]+) with (?:[^"]* )"(?P<text>[^"]+)"(?: [^"]*) appears')
@fake
def a__with__ptext__appears(context, text):
    assert all_views.base.element_with_text_is_present(text)


@step("I see my existing (?P<category>\S+) voicemails")
@fake
def step_impl(context, category):
    displayed_texts = all_views.voicemail.get_top_vm_texts()
    metadata_all = context.vvm_microservice.get_vm_metadata('new', ['callerName', 'callerNumber', 'duration',
                                                                     'dateRecorded'])
    fail_msg = "visible VM's did not match VM's from vvm API"
    assert all_views.voicemail.vm_match_all(displayed_texts, metadata_all), fail_msg
