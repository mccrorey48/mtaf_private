from behave import *
from ePhone7.views import *
from time import sleep


@step("[history] I see the All and Missed tabs at the top of the screen")
def history__i_see_the_all_and_missed_tabs_at_the_top_of_the_screen(context):
    if 'fake' not in str(context._config.tags).split(','):
        history_view.find_named_element('All')
        history_view.find_named_element('Missed')


@step("[history] the History view appears")
def history__the_history_view_appears(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert history_view.element_is_present('HistoryList')


