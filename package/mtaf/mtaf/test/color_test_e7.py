from ePhone7.views import *
import six
base_view.open_appium('main')
if user_view.becomes_present():
    base_view.touch_element_with_text('Voicemail')
    if voicemail_view.becomes_present():
        voicemail_view.get_screenshot_as_png('voicemail')
        six.print_(voicemail_view.get_tab_color('voicemail', 'New'))
        six.print_(voicemail_view.get_tab_color('voicemail', 'Saved'))
        six.print_(voicemail_view.get_tab_color('voicemail', 'Trash'))
    else:
        six.print_("voicemail view did not appear")
else:
    six.print_("user view did not appear")
