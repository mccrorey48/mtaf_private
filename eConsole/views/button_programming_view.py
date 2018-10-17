import mtaf.mtaf_logging as logging
from eConsole.views.logged_in_view import LoggedInView

log = logging.get_logger('mtaf.btn_prog')


class ButtonProgrammingView(LoggedInView):

    locators = {
    }

    def __init__(self):
        super(ButtonProgrammingView, self).__init__()
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]
        self.view_name = 'button_programming_view'


button_programming_view = ButtonProgrammingView()
