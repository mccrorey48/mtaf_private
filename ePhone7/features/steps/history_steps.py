from behave import *
from ePhone7.views import *
from mtaf.trace import fake


@step("[history] I see the All and Missed tabs at the top of the screen")
@fake
def history__i_see_the_all_and_missed_tabs_at_the_top_of_the_screen(context):
    assert history_view.All is not None, 'history_view.All element not present'
    assert history_view.Missed is not None, 'history_view.Missed element not present'


@step("[history] I see the call at the top of the All History view")
@fake
def history__i_see_the_call_at_the_top_of_the_all_history_view(context):
    history_view.get_top_call_record()


@step("[history] I see the call at the top of the Missed History view")
@fake
def i_see_the_call_at_the_top_of_the_missed_history_view(context):
    history_view.get_top_call_record()


@step("[history] I touch the handset icon")
@fake
def history__i_touch_the_handset_icon(context):
    history_view.touch_handset()


@step("[history] the call has a {color} handset icon")
@fake
def history__the_call_has_a_handset_icon(context, color):
    history_view.get_expect_icon_color(handset_color=color)


@step("[history] the History view appears")
@fake
def history__the_history_view_appears(context):
    assert history_view.element_with_text_is_present('All')
    assert history_view.element_with_text_is_present('Missed')
