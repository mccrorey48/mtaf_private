import mtaf.mtaf_logging as logging
from eConsole.views.logged_in_view import LoggedInView

log = logging.get_logger('mtaf.msg_settings')


class MessageSettingsView(LoggedInView):

    locators = {
        "Greetings": {"by": "css selector", "value": "p", "text": "Greetings"},
    }

    def __init__(self):
        super(MessageSettingsView, self).__init__()
        self.presence_element_names = ["Greetings"]
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]
        self.view_name = 'message_settings'


message_settings_view = MessageSettingsView()
