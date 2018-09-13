import mtaf.mtaf_logging as logging
from eConsole.views.logged_in_view import LoggedInView

log = logging.get_logger('mtaf.moh')


class MusicOnHoldView(LoggedInView):

    locators = {
        "Banner": {"by": "css selector", "value": "span[class='esi-header-text']",
                   "text": "Settings / Music on Hold"},
    }

    def __init__(self):
        super(MusicOnHoldView, self).__init__()
        self.presence_element_names = ["Banner"]
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]
        self.view_name = 'music_on_hold_view'


music_on_hold_view = MusicOnHoldView()
