import mtaf.mtaf_logging as logging
from eConsole.views.logged_in_view import LoggedInView

log = logging.get_logger('mtaf.call_history')


class CallHistoryView(LoggedInView):

    locators = {
        "RecentCallHistory": {"by": "id", "value": "recent-call-history"},
        "Name": {"by": "css selector", "value": "th span", "text": "Name"},
        "Number": {"by": "css selector", "value": "th span", "text": "Number"},
        "Date": {"by": "css selector", "value": "th span", "text": "Date"},
        "Duration": {"by": "css selector", "value": "th span", "text": "Duration"},
        "Actions": {"by": "css selector", "value": "th span", "text": "Actions"},
    }

    def __init__(self):
        super(CallHistoryView, self).__init__()
        self.presence_element_names = ["RecentCallHistory"]
        self.banner_texts = ['Call History']
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]
        self.view_name = 'call_history'


call_history_view = CallHistoryView()
