import mtaf.mtaf_logging as logging
from eConsole.views.logged_in_view import LoggedInView

log = logging.get_logger('mtaf.allow_blk_num')


class AllowBlockNumbersView(LoggedInView):

    locators = {
        "AddAllowedNumber": {"by": "id", "value": "allowed_number_btn"},
        "AddBlockedNumber": {"by": "id", "value": "block_number_btn"},
        "AllowedNumber": {"by": "id", "value": "allowed_number"},
        "AllowedNumbers": {"by": "css_selector", "value": "label", "text": "Allowed Numbers"},
        "AnonBlock": {"by": "id", "value": "anon-block"},
        "AnonBlockLabel": {"by": "css_selector", "value": "label", "text": "Block anonymous or unknown"},
        "Banner": {"by": "css selector", "value": "span[class='esi-header-text']", "text": "Settings / Block and Allow Numbers"},
        "BlockedNumber": {"by": "id", "value": "block_number"},
        "BlockedNumbers": {"by": "css_selector", "value": "label", "text": "Blocked Numbers"},
    }

    def __init__(self):
        super(AllowBlockNumbersView, self).__init__()
        self.presence_element_names = ["Banner"]
        self.content_scopes.update({
            "AddAllowedNumber": ['premier', 'office_mgr'],
            "AddBlockedNumber":  ['premier', 'office_mgr'],
            "AllowedNumber":  ['premier', 'office_mgr'],
            "AllowedNumbers":  ['premier', 'office_mgr'],
            "AnonBlock":  ['premier', 'office_mgr'],
            "AnonBlockLabel":  ['premier', 'office_mgr'],
            "Banner":  ['premier', 'office_mgr'],
            "BlockedNumber":  ['premier', 'office_mgr'],
            "BlockedNumbers":  ['premier', 'office_mgr'],
        })
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]
        self.view_name = 'allow_block_numbers_view'


allow_block_numbers_view = AllowBlockNumbersView()
