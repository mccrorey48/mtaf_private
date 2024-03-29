import lib.logging_esi as logging
from eConsole.views.base_view import BaseView

log = logging.get_logger('esi.home')


class ContactsView(BaseView):

    locators = {
        "TypeLabel": {"by": "css selector", "value": "div + form label", "text": "Type"},
        "PresenceLabel": {"by": "css selector", "value": "div + form label", "text": "Presence"},
        "GroupsLabel": {"by": "css selector", "value": "div + form label", "text": "Groups"},
        "SearchLabel": {"by": "css selector", "value": "div + form label", "text": "Search"}
    }

    def __init__(self):
        super(ContactsView, self).__init__()
        self.presence_element_names = ["TypeLabel", "PresenceLabel", "GroupsLabel", "SearchLabel"]
        self.banner_texts = ['Contacts']
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]


contacts_view = ContactsView()
