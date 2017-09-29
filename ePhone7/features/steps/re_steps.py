from behave import *
from ePhone7.views import base_view, user_view
from lib.wrappers import fake

use_step_matcher('re')


@step('a (?:[^"]+) with (?:[^"]* )"(?P<text>[^"]+)"(?: [^"]*) appears')
@fake
def a__with__ptext__appears(context, text):
    assert base_view.element_with_text_is_present(text)


@step('I touch (?:[^"]*)?"(?P<text>[^"]+)"(?P<tail>[^"]*)')
@fake
def i_touch_ptextptail(context, text, tail):
    # matches: I touch <optional> "<text>" <optional>
    # where <optional> and <text> are any text not including a double quote
    # then looks for an element with full text content matching <text>
    if tail == 'tab':
        user_view.goto_tab(text)
    else:
        base_view.touch_element_with_text(text)


