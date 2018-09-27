import mtaf.mtaf_logging as logging
from eConsole.views.logged_in_view import LoggedInView

log = logging.get_logger('mtaf.phones')


class PhonesView(LoggedInView):

    locators = {
        "DeviceStatus": {"by": "css selector", "value": "th span", "text": "Device Status"},
        "DeviceName": {"by": "css selector", "value": "th span", "text": "Device Name"},
        "DeviceType": {"by": "css selector", "value": "th span", "text": "Device Type"},
        "Line": {"by": "css selector", "value": "th span", "text": "Line"},
        "Actions": {"by": "css selector", "value": "th span", "text": "Actions"},
        "ButtonProgramming": {"by": "css selector", "value": "button[ng-click='goToButtonProgramming()']",
                              "text": "Button Programming"},
    }

    def __init__(self):
        super(PhonesView, self).__init__()
        self.presence_element_names = ['DeviceStatus', 'DeviceName', 'DeviceType', 'Line', 'Actions']
        self.banner_texts = ['Phones']
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]
        self.view_name = 'phones'
        self.content_scopes.update({
            "ButtonProgramming": self.all_scopes,
        })


phones_view = PhonesView()
