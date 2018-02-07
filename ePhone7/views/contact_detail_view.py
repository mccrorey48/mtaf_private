import lib.logging_esi as logging
from ePhone7.views.user_view import UserView
from lib.filters import get_filter

log = logging.get_logger('esi.contacts_view')


class ContactDetailView(UserView):

    locators = {
        "CloseIcon": {"by": "id", "value": "com.esi_estech.ditto:id/bottom_sheet_title_clear_button"},
        "EmailAddressesBanner": {"by": "id", "value": "com.esi_estech.ditto:id/header_string", "text": "Email Addresses"},
        "FavoriteIndicator": {"by": "id", "value": "com.esi_estech.ditto:id/favorite_indicator"},
        "GroupsBanner": {"by": "id", "value": "com.esi_estech.ditto:id/header_string", "text": "Groups"},
        'PhoneNumbersBanner': {'by': 'id', "value": "com.esi_estech.ditto:id/header_string", "text": "Phone Numbers"},
        'UserName': {'by': 'id', 'value': 'com.esi_estech.ditto:id/bottom_sheet_title'},
    }

    def __init__(self):
        super(ContactDetailView, self).__init__()
        self.tab_names = ('Personal', 'Coworkers', 'Favorites', 'Groups')
        self.png_file_base = 'contact_detail'
        self.displayed_elems = []
        self.displayed_numbers = []
        self.presence_element_names = ['EmailAddressesBanner', 'GroupsBanner', 'PhoneNumbersBanner', 'UserName']


contact_detail_view = ContactDetailView()
