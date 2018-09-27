import mtaf.mtaf_logging as logging
from eConsole.views.logged_in_view import LoggedInView

log = logging.get_logger('mtaf.messages')


class MessagesView(LoggedInView):

    locators = {
        "NewTab": {"by": "class name", "value": "tab", "text": "New"},
        "SavedTab": {"by": "class name", "value": "tab", "text": "Saved"},
        "TrashTab": {"by": "class name", "value": "tab", "text": "Trash"},
        "MessageName": {"by": "css selector", "value": "div[class='ng-table-header ng-scope']", "text": "Name"},
        "MessageNumber": {"by": "css selector", "value": "div[class='ng-table-header ng-scope']", "text": "Number"},
        "MessageDate": {"by": "css selector", "value": "div[class='ng-table-header ng-scope']", "text": "Date"},
        "MessageDuration": {"by": "css selector", "value": "div[class='ng-table-header ng-scope']", "text": "Duration"},
        "MessageActions": {"by": "css selector", "value": "div[class='ng-table-header ng-scope']", "text": "Actions"},
        "MessageSettingsButton": {"by": "css selector", "value": "a[href='#!/settings/mailbox']",
                                  "text": "Message Settings"},
    }

    def __init__(self):
        super(MessagesView, self).__init__()
        self.presence_element_names = ["NewTab", "SavedTab", "TrashTab"]
        self.banner_texts = ['Messages']
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]
        self.view_name = 'messages'
        self.content_scopes.update({
            "MessageName": self.all_scopes,
            "MessageNumber": self.all_scopes,
            "MessageDate": self.all_scopes,
            "MessageDuration": self.all_scopes,
            "MessageActions": self.all_scopes,
            "MessageSettingsButton": self.all_scopes,
        })


messages_view = MessagesView()
