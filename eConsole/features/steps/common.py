from behave import *
from eConsole.views import *
import re


def camel_case(text):
    words = re.split('[\s_]+', text)
    for i, word in enumerate(words[:]):
        word = word.lower()
        words[i] = word[0].upper() + word[1:]
    return ''.join(words)


@step("I click the {tab_text} tab")
def i_click_the_tabtext_tab(context, tab_text):
    tab_prefix = tab_text.lower()
    tab_prefix = tab_prefix[0].upper() + tab_prefix[1:]
    base_view.click_named_element(camel_case(tab_prefix) + 'Tab')


@step("I log in to the dashboard")
def i_log_in_to_the_dashboard(context):
    context.run_substep("I enter a valid %s user ID" % context.config.userdata['user_scope'])
    context.run_substep("I enter a valid %s password" % context.config.userdata['user_scope'])
    context.run_substep("I click the Login button")
    context.run_substep("the Home page appears")
