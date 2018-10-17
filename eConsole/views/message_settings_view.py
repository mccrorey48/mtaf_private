import mtaf.mtaf_logging as logging
from eConsole.views.logged_in_view import LoggedInView

log = logging.get_logger('mtaf.msg_settings')


class MessageSettingsView(LoggedInView):

    locators = {
        "AnnounceCID": {"by": "css selector", "value": "input[ng-model='user.vmail_annc_cid']"},
        "AnnounceCIDLabel": {"by": "css selector", "value": "label[class='form-check-label']", "text": "Announce incoming call ID"},
        "AnnounceTime": {"by": "css selector", "value": "input[ng-model='user.vmail_annc_time']"},
        "AnnounceTimeLabel": {"by": "css selector", "value": "label[class='form-check-label']", "text": "Announce voice Mail received time"},
        "EmailNotificationLabel": {"by": "css selector", "value": "label[for='emailNotification']"},
        "EnableVM": {"by": "css selector", "value": "p", "text": "Greetings"},
        "EnableVMLabel": {"by": "css selector", "value": "label[class='form-check-label']", "text": "Enable Voice Mail"},
        "Greetings": {"by": "css selector", "value": "p", "text": "Greetings"},
        "Inbox": {"by": "css selector", "value": "p", "text": "Inbox"},
        "RecordedNameLabel": {"by": "css selector", "value": "label[class='col-md-3 my-auto']", "text": "Recorded Name"},
        "SortVM": {"by": "css selector", "value": "input[ng-model='user.vmail_sort_lifo']"},
        "SortVMLabel": {"by": "css selector", "value": "label[class='form-check-label']", "text": "Sort voice Mail inbox by latest first"},
        "UnifiedMessaging": {"by": "css selector", "value": "p", "text": "Unified Messaging"},
        "VMGreetingLabel": {"by": "css selector", "value": "label[for='vmGreeting']"},
    }

    def __init__(self):
        super(MessageSettingsView, self).__init__()
        self.presence_element_names = ["Greetings"]
        self.banner_texts = ['Settings', 'Message Settings']
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]
        self.view_name = 'message_settings'
        self.content_scopes.update({
            "AnnounceCIDLabel": self.all_scopes,
            "AnnounceCID": self.all_scopes,
            "AnnounceTimeLabel": self.all_scopes,
            "AnnounceTime": self.all_scopes,
            "EmailNotificationLabel": self.all_scopes,
            "EnableVMLabel": self.all_scopes,
            "EnableVM": self.all_scopes,
            "Inbox": self.all_scopes,
            "RecordedNameLabel": self.all_scopes,
            "SortVMLabel": self.all_scopes,
            "SortVM": self.all_scopes,
            "UnifiedMessaging": self.all_scopes,
            "VMGreetingLabel": self.all_scopes,
        })


message_settings_view = MessageSettingsView()
