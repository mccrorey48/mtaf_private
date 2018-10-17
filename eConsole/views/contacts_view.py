import mtaf.mtaf_logging as logging
from eConsole.views.logged_in_view import LoggedInView

log = logging.get_logger('mtaf.contacts')


class ContactsView(LoggedInView):

    locators = {
        "ActionsHeader": {"by": "css selector", "value": "th", "text": "Actions"},
        "AddButton": {"by": "css selector", "value": "button[ng-click='preAddContact()']"},
        "EmailHeader": {"by": "css selector", "value": "th", "text": "Email"},
        "ExportButton": {"by": "css selector", "value": "button[ng-click='preExportContact()']"},
        "GoogleButton": {"by": "css selector", "value": "button[ng-click='logIntoGoogle()']"},
        "GroupsHeader": {"by": "css selector", "value": "th", "text": "Groups"},
        "GroupsLabel": {"by": "css selector", "value": "label", "text": "Groups"},
        "ImportButton": {"by": "css selector", "value": "button[ng-click='preImportContact()']"},
        "NameHeader": {"by": "css selector", "value": "th", "text": "Name"},
        "NumberHeader": {"by": "css selector", "value": "th", "text": "Number"},
        "PresenceLabel": {"by": "css selector", "value": "label", "text": "Presence"},
        "SearchBox": {"by": "css selector", "value": "input[name='searchContacts']"},
        "SearchLabel": {"by": "css selector", "value": "label", "text": "Search"},
        "TypeLabel": {"by": "css selector", "value": "label", "text": "Type"},
    }

    def __init__(self):
        super(ContactsView, self).__init__()
        self.presence_element_names = ["TypeLabel", "PresenceLabel", "GroupsLabel", "SearchLabel"]
        self.banner_texts = ['Contacts']
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]
        self.view_name = 'contacts'
        self.content_scopes.update({
            "ActionsHeader": self.all_scopes,
            "AddButton": ['premier', 'office_mgr'],
            "EmailHeader": self.all_scopes,
            "ExportButton": ['premier', 'office_mgr'],
            "GoogleButton": ['premier', 'office_mgr'],
            "GroupsHeader": self.all_scopes,
            "GroupsLabel": self.all_scopes,
            "ImportButton": ['premier', 'office_mgr'],
            "NameHeader": self.all_scopes,
            "NumberHeader": self.all_scopes,
            "PresenceLabel": self.all_scopes,
            "SearchBox": self.all_scopes,
            "SearchLabel": self.all_scopes,
            "TypeLabel": self.all_scopes,
        })


contacts_view = ContactsView()
