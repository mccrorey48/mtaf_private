from behave import *
from ePhone7.views import *


@step("[history] I see the All and Missed tabs at the top of the screen")
def history__i_see_the_all_and_missed_tabs_at_the_top_of_the_screen(context):
    assert history_view.All is not None, 'history_view.All element not present'
    assert history_view.Missed is not None, 'history_view.Missed element not present'


@step("[history] I see the call at the top of the All History view")
def history__i_see_the_call_at_the_top_of_the_all_history_view(context):
    history_view.get_top_call_record()


@step("[history] I see the call at the top of the Missed History view")
def history__i_see_the_call_at_the_top_of_the_missed_history_view(context):
    history_view.get_top_call_record()


@step("[history] I touch the All tab")
def history__i_touch_the_all_tab(context):
    history_view.goto_tab('All')


@step("[history] I touch the handset icon")
def history__i_touch_the_handset_icon(context):
    history_view.touch_handset()


@step("[history] I touch the Missed tab")
def history__i_touch_the_missed_tab(context):
    history_view.goto_tab('Missed')


@step("[history] the call has a {color} handset icon")
def history__the_call_has_a_color_handset_icon(context, color):
    history_view.get_expect_icon_color(handset_color=color)


@step("[history] the History view appears")
def history__the_history_view_appears(context):
    assert history_view.element_with_text_is_present('All')
    assert history_view.element_with_text_is_present('Missed')


