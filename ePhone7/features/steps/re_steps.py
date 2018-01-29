from behave import *
from ePhone7.views import all_views
from mtaf.trace import fake

use_step_matcher("re")


@step('a (?:[^"]+) with (?:[^"]* )"(?P<text>[^"]+)"(?: [^"]*) appears')
@fake
def a__with__ptext__appears(context, text):
    assert all_views.base.element_with_text_is_present(text)


@step("I send the (?P<name>\S+) keycode")
@fake
def i_send_the_pnames_keycode(context, name):
    all_views.base.send_keycode('KEYCODE_%s' % name.upper())


@step('I touch (?:the )?"(?P<text>[^"]+)"(?P<tail>[^"]*)')
@fake
def i_touch_the_ptextptail(context, text, tail):
    # matches: I touch <optional> "<text>" <optional>
    # where <optional> and <text> are any text not including a double quote
    # then looks for an element with full text content matching <text>
    if tail == 'tab':
        all_views.user.goto_tab(text)
    else:
        all_views.base.touch_element_with_text(text)


@step('the "(?P<view>\S+)" view is (?P<mode>\S*)\s?present')
@fake
def the_pviews_view_is_pmodesspresent(context, view, mode):
    if mode.lower() == 'not':
        assert all_views[view].becomes_not_present(), "%s view is present"
    else:
        assert all_views[view].becomes_present(), "%s view is not present"


@step('the "(?P<view>\S+)" view (?P<mode>dis)?appears')
@fake
def the_pviews_view_pmodedisappears(context, view, mode):
    if mode == 'dis':
        context.run_substep('the "%s" view is not present' % view)
    else:
        context.run_substep('the "%s" view is present' % view)


@step("the (?P<view>\S+) view (?P<name>\S+) element is (?P<mode>\S*)\s?present")
@fake
def the_pviews_view_pnames_element_is_pmodesspresent(context, view, name, mode):
    if mode.lower() == 'not':
        assert all_views[view][name] is None, '%s view element "%s" is present' % (view, name)
    else:
        assert all_views[view][name], '%s view element "%s" is not present' % (view, name)


