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
        "Export": {"by": "css selector", "value": "button[ng-click='downloadHistory()']", "text": "Export"},
        "Filters": {"by": "css selector", "value": "button[ng-click='preHistoryFilters()']", "text": "Filters"},
        "HistoryName": {"by": "css selector", "value": "div[class='ng-table-header ng-scope']", "text": "Name"},
        "HistoryNumber": {"by": "css selector", "value": "div[class='ng-table-header ng-scope']", "text": "Number"},
        "HistoryDate": {"by": "css selector", "value": "div[class='ng-table-header ng-scope']", "text": "Date"},
        "HistoryDuration": {"by": "css selector", "value": "div[class='ng-table-header ng-scope']", "text": "Duration"},
        "HistoryActions": {"by": "css selector", "value": "div[class='ng-table-header ng-scope']", "text": "Actions"},
    }

    def __init__(self):
        super(CallHistoryView, self).__init__()
        self.presence_element_names = ["RecentCallHistory"]
        self.banner_texts = ['Call History']
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]
        self.view_name = 'call_history'
        self.content_scopes.update({
            "HistoryName": self.all_scopes,
            "HistoryNumber": self.all_scopes,
            "HistoryDate": self.all_scopes,
            "HistoryDuration": self.all_scopes,
            "HistoryActions": self.all_scopes,
            "Export": self.all_scopes,
            "Filters": self.all_scopes,
        })


call_history_view = CallHistoryView()
