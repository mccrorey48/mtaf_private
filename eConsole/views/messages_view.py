import lib.logging_esi as logging
from eConsole.views.base_view import BaseView

log = logging.get_logger('esi.home')


class MessagesView(BaseView):

    locators = {
        "NewTab": {"by": "class name", "value": "tab", "text": "New"},
        "SavedTab": {"by": "class name", "value": "tab", "text": "Saved"},
        "TrashTab": {"by": "class name", "value": "tab", "text": "Trash"},
    }

    def __init__(self):
        super(MessagesView, self).__init__()
        self.presence_element_names = ["NewTab", "SavedTab", "TrashTab"]
        self.banner_item_texts = ['Messages']
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]


messages_view = MessagesView()
