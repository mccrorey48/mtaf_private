import mtaf.mtaf_logging as logging
from eConsole.views.logged_in_view import LoggedInView

log = logging.get_logger('mtaf.ans_rules')


class AnsweringRulesView(LoggedInView):

    locators = {
        "Banner": {"by": "css selector", "value": "span[class='esi-header-text']",
                   "text": "Settings / Answering Rules"},
    }

    def __init__(self):
        super(AnsweringRulesView, self).__init__()
        self.presence_element_names = ["Banner"]
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]
        self.view_name = 'answering_rules_view'


answering_rules_view = AnsweringRulesView()
