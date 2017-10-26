from behave import *
from ePhone7.views import *
from lib.wrappers import fake


@step("[history] I see the All and Missed tabs at the top of the screen")
@fake
def history__i_see_the_all_and_missed_tabs_at_the_top_of_the_screen(context):
    assert history_view.All is not None, 'history_view.All element not present'
    assert history_view.Missed is not None, 'history_view.Missed element not present'


@step("[history] I see the call at the top of the All History view")
@fake
def history__i_see_the_call_at_the_top_of_the_all_history_view(context):
    pass


@step("[history] I touch the handset icon")
@fake
def history__i_touch_the_handset_icon(context):
    pass


@step("[history] the call has a blue handset icon with an incoming arrow")
@fake
def history__the_call_has_a_blue_handset_icon_with_an_incoming_arrow(context):
    pass


@step("[history] the call has a green handset icon with an outgoing arrow")
@fake
def history__the_call_has_a_green_handset_icon_with_an_outgoing_arrow(context):
    pass


@step("[history] the History view appears")
@fake
def history__the_history_view_appears(context):
    assert history_view.element_with_text_is_present('All')
    assert history_view.element_with_text_is_present('Missed')


