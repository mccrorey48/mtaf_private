import mtaf.mtaf_logging as logging
from eConsole.views.base_view import BaseView

log = logging.get_logger('esi.home')


class MessageSettingsView(BaseView):

    locators = {
        "Greetings": {"by": "css selector", "value": "p", "text": "Greetings"},
    }

    def __init__(self):
        super(MessageSettingsView, self).__init__()
        self.presence_element_names = ["Greetings"]
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]


message_settings_view = MessageSettingsView()
