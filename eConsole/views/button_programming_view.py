import mtaf.mtaf_logging as logging
from eConsole.views.logged_in_view import LoggedInView

log = logging.get_logger('mtaf.btn_prog')


class ButtonProgrammingView(LoggedInView):

    locators = {
        "Banner": {"by": "css selector", "value": "span[class='esi-header-text']",
                   "text": "Settings / Button Programming"},
    }

    def __init__(self):
        super(ButtonProgrammingView, self).__init__()
        self.presence_element_names = ["Banner"]
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]
        self.view_name = 'button_programming_view'


button_programming_view = ButtonProgrammingView()
