from behave import *
from ePhone7.views import *
import re
from time import sleep


@step("[user] I see the Contacts, History, Voicemail and Dial buttons at the bottom of the screen")
def user__i_see_the_contacts_history_voicemail_and_dial_buttons_at_the_bottom_of_the_screen(context):
    if 'fake' not in str(context._config.tags).split(','):
        user_view.find_named_element('Contacts')
        user_view.find_named_element('History')
        user_view.find_named_element('Voicemail')
        user_view.find_named_element('Dial')


@step('[user] I touch the "Contacts" button')
def user__i_touch_the_contacts_button(context):
    if 'fake' not in str(context._config.tags).split(','):
        user_view.click_named_element('Contacts')


@step("[user] I touch the Dial button")
def user__i_touch_the_dial_button(context):
    if 'fake' not in str(context._config.tags).split(','):
        user_view.click_named_element('Dial')


@step("[user] I touch the History button")
def user__i_touch_the_history_button(context):
    if 'fake' not in str(context._config.tags).split(','):
        user_view.click_named_element('History')


@step("[user] I touch the Preferences icon")
def user__i_touch_the_preferences_icon(context):
    if 'fake' not in str(context._config.tags).split(','):
        user_view.tap([(559, 74)])
        if not prefs_view.element_is_present('Preferences'):
            # one retry
            user_view.tap([(559, 74)])
        # user_view.click_named_element('PrefsButton')
        pass


@step("[user] I touch the Voicemail button")
def user__i_touch_the_voicemail_button(context):
    if 'fake' not in str(context._config.tags).split(','):
        user_view.click_named_element('Voicemail')


