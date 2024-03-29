import lib.logging_esi as logging
from eConsole.views.base_view import BaseView

log = logging.get_logger('esi.home')


class CallHistoryView(BaseView):

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


call_history_view = CallHistoryView()
