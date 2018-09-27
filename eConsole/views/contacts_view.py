import mtaf.mtaf_logging as logging
from eConsole.views.logged_in_view import LoggedInView

log = logging.get_logger('mtaf.contacts')


class ContactsView(LoggedInView):

    locators = {
        "TypeLabel": {"by": "css selector", "value": "label", "text": "Type"},
        "PresenceLabel": {"by": "css selector", "value": "label", "text": "Presence"},
        "GroupsLabel": {"by": "css selector", "value": "label", "text": "Groups"},
        "SearchLabel": {"by": "css selector", "value": "label", "text": "Search"},
        "SearchBox": {"by": "css selector", "value": "input[name='searchContacts']"},
        "NameHeader": {"by": "css selector", "value": "th", "text": "Name"},
        "NumberHeader": {"by": "css selector", "value": "th", "text": "Number"},
        "GroupsHeader": {"by": "css selector", "value": "th", "text": "Groups"},
        "EmailHeader": {"by": "css selector", "value": "th", "text": "Email"},
        "ActionsHeader": {"by": "css selector", "value": "th", "text": "Actions"},
        "GoogleButton": {"by": "css selector", "value": "button[ng-click='logintoGoogle()']"},
        "ImportButton": {"by": "css selector", "value": "button[ng-click='preImportContact()']"},
        "ExportButton": {"by": "css selector", "value": "button[ng-click='preExportContact()']"},
        "AddButton": {"by": "css selector", "value": "button[ng-click='preAddContact()']"},
    }

    def __init__(self):
        super(ContactsView, self).__init__()
        self.presence_element_names = ["TypeLabel", "PresenceLabel", "GroupsLabel", "SearchLabel"]
        self.banner_texts = ['Contacts']
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]
        self.view_name = 'contacts'
        self.content_scopes.update({
            "TypeLabel": self.all_scopes,
            "PresenceLabel": self.all_scopes,
            "GroupsLabel": self.all_scopes,
            "SearchLabel": self.all_scopes,
            "SearchBox": self.all_scopes,
            "NameHeader": self.all_scopes,
            "NumberHeader": self.all_scopes,
            "GroupsHeader": self.all_scopes,
            "EmailHeader": self.all_scopes,
            "ActionsHeader": self.all_scopes,
            "GoogleButton": ['premier', 'office_mgr'],
            "ImportButton": ['premier', 'office_mgr'],
            "ExportButton": ['premier', 'office_mgr'],
            "AddButton": ['premier', 'office_mgr'],
        })


contacts_view = ContactsView()
