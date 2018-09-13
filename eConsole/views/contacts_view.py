import mtaf.mtaf_logging as logging
from eConsole.views.logged_in_view import LoggedInView

log = logging.get_logger('mtaf.contacts')


class ContactsView(LoggedInView):

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
        self.view_name = 'contacts'


contacts_view = ContactsView()
