import mtaf.mtaf_logging as logging
from eConsole.views.base_view import BaseView

log = logging.get_logger('mtaf.messages')


class MessagesView(BaseView):

    locators = {
        "NewTab": {"by": "class name", "value": "tab", "text": "New"},
        "SavedTab": {"by": "class name", "value": "tab", "text": "Saved"},
        "TrashTab": {"by": "class name", "value": "tab", "text": "Trash"},
    }

    def __init__(self):
        super(MessagesView, self).__init__()
        self.presence_element_names = ["NewTab", "SavedTab", "TrashTab"]
        self.banner_texts = ['Messages']
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]
        self.view_name = 'messages'


messages_view = MessagesView()
