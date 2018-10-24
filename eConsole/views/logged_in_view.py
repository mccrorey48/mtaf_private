import mtaf.mtaf_logging as logging

from eConsole.views.base_view import BaseView
from mtaf.decorators import Trace

log = logging.get_logger('mtaf.login')


class LoggedInView(BaseView):

    locators = {
        "AllowBlockNumbers": {"by": "css selector", "value": "a[href='#!/settings/blockNumbers']"},
        "Banner": {"by": "css selector", "value": "span[class='esi-header-text']"},
        "BrandImage": {"by": "id", "value": "brand-image"},
        "CallHistoryTab": {"by": "css selector", "value": ".navbar-nav .nav-item:nth-child(3)"},
        "ContactsPullout": {"by": "id", "value": "cwContainer"},
        "ContactsPulloutValues": {"by": "css selector", "value": "#cwContainer .conNumber"},
        "ContactsTab": {"by": "css selector", "value": ".navbar-nav .nav-item:nth-child(4)"},
        "eHelp": {"by": "link text", "value": "eHelp"},
        "HomeTab": {"by": "css selector", "value": ".navbar-nav .nav-item:nth-child(1)"},
        "LoadingGif": {"by": "class name", "value": "loadingoverlay"},
        "Logout": {"by": "id", "value": "logout"},
        "MainButton": {"by": "id", "value": "mainButton"},
        "ManageOrganization": {"by": "id", "value": "org-view"},
        "MessageSettings": {"by": "css selector", "value": ".dropdown-item.ng-scope", "text": "Message Settings"},
        "MessagesTab": {"by": "css selector", "value": ".navbar-nav .nav-item:nth-child(2)"},
        "NavTabs": {"by": "css selector", "value": ".navbar-nav .nav-item"},
        "PhonesTab": {"by": "css selector", "value": ".navbar-nav .nav-item:nth-child(5)"},
        "ProvideFeedback": {"by": "link text", "value": "Provide feedback"},
        "SettingsDropdownItems": {"by": "css selector", "value": """a[ng-click="selectOnMenu('settings')"]"""},
        "SettingsTab": {"by": "id", "value": "navbarDropdown"},
        "SelectedTab": {"by": "css selector", "value": ".navbar-nav .nav-item .active"},
        "ShowContacts": {"by": "id", "value": "showContacts"},
        # only thing saved from the now-deleted "econs" branch was this locator:
        # "MessageSettings": {"by": "css selector", "value": "li.nav-item.dropdown.show > div > a:nth-child(2)"}
    }

    def __init__(self):
        super(LoggedInView, self).__init__()
        self.page_title = "ESI"
        self.presence_element_names = ["ShowContacts"]
        self.content_scopes = {
            "BrandImage": self.all_scopes,
            "eHelp": self.all_scopes,
            "ProvideFeedback": self.all_scopes,
            "MainButton": self.all_scopes,
            "ShowContacts": self.all_scopes,
        }
        self.view_name = 'login'

    @Trace(log)
    def click_settings_item_with_text(self, item_text):
        locator = self.get_locator("SettingsDropdownItems")
        locator["text"] = item_text
        self.find_element_by_locator(locator).click()

    @Trace(log)
    def logout(self):
        self.click_named_element("MainButton")
        self.click_named_element("Logout")


logged_in_view = LoggedInView()
