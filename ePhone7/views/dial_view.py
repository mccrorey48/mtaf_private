from time import sleep

import lib.logging_esi as logging
from ePhone7.config.configure import cfg
from ePhone7.utils.get_softphone import get_softphone
from ePhone7.views.user_view import UserView
from lib.wrappers import Trace
from appium.webdriver.common.touch_action import TouchAction

log = logging.get_logger('esi.keypad_view')


class DialView(UserView):

    locators = {
        "CurrentOtaPopup": {"by": "id", "value": "com.esi_estech.ditto:id/title_text", "text": "OTA Server" },
        "CurrentOtaPopupContent": {"by": "id", "value": "com.esi_estech.ditto:id/content_text"},
        "DialButton": {"by": "id", "value": "com.esi_estech.ditto:id/dial_call_button_view"},
        "DialPad": {"by": "id", "value": "com.esi_estech.ditto:id/dialpad_sliding_panel"},
        "Delete": {"by": "id", "value": "com.esi_estech.ditto:id/deleteButton"},
        "Digits": {"by": "id", "value": "com.esi_estech.ditto:id/digits"},
        "FuncKeyAll": {"by": "zpath", "value": "//tl/tr/ll"},
        "FuncKeyBksp": {"by": "id", "value": "com.esi_estech.ditto:id/dialpad_delete_button_container" },
        "FuncKeySearch": {"by": "id", "value": "com.esi_estech.ditto:id/dialpad_search_button_container" },
        "NumberButton": {"by": "id", "value": "com.esi_estech.ditto:id/keypad_symbols"},
        "NumKeyAll": {"by": "zpath", "value": "//gv/rl"},
        "NumKey1": {"by": "id", "value": "dial_one"},
        "NumKey2": {"by": "id", "value": "dial_two"},
        "NumKey3": {"by": "id", "value": "dial_three"},
        "NumKey4": {"by": "id", "value": "dial_four"},
        "NumKey5": {"by": "id", "value": "dial_five"},
        "NumKey6": {"by": "id", "value": "dial_six"},
        "NumKey7": {"by": "id", "value": "dial_seven"},
        "NumKey8": {"by": "id", "value": "dial_eight"},
        "NumKey9": {"by": "id", "value": "dial_nine"},
        "NumKeyStar": {"by": "id", "value": "dial_star"},
        "NumKey0": {"by": "id", "value": "dial_zero"},
        "NumKeyPound": {"by": "id", "value": "dial_pound"},
        "OtaUpdatePopup": {"by": "id", "value": "com.esi_estech.ditto:id/title_text", "text": "OTA Server Update" },
        "OtaUpdatePopupContent": {"by": "id", "value": "com.esi_estech.ditto:id/content_text"}

    }

    digit_names = {
        "0": "NumKey0",
        "1": "NumKey1",
        "2": "NumKey2",
        "3": "NumKey3",
        "4": "NumKey4",
        "5": "NumKey5",
        "6": "NumKey6",
        "7": "NumKey7",
        "8": "NumKey8",
        "9": "NumKey9",
        "*": "NumKeyStar",
        "#": "NumKeyPound"
    }

    digit_centers = {
        '1': [143, 491],
        '2': [301, 491],
        '3': [459, 491],
        '4': [143, 574],
        '5': [301, 574],
        '6': [459, 574],
        '7': [143, 657],
        '8': [301, 657],
        '9': [459, 657],
        '*': [143, 740],
        '0': [301, 740],
        '#': [459, 740]
    }

    digit_centers_old_keyboard = {
        '1': [142, 420],
        '2': [300, 420],
        '3': [470, 420],
        '4': [142, 520],
        '5': [300, 520],
        '6': [470, 520],
        '7': [142, 620],
        '8': [300, 620],
        '9': [470, 620],
        '*': [142, 725],
        '0': [300, 725],
        '#': [470, 725]
    }

    numbers = {
        "Current OTA Server": "*682#",
        "Production OTA Server": "*7763#",
        "Alpha OTA Server": "*23742#",
        "Beta OTA Server": "*2382#",
        "Advanced Settings": "*1987"
    }

    def __init__(self):
        super(DialView, self).__init__()
        self.png_file_base = 'keypad'
        self.presence_element_names = ['NumKey1']

    @Trace(log)
    def dial_advanced_settings(self):
        self.dial_named_number("Advanced Settings")

    @Trace(log)
    def dial_show_ota_server(self):
        self.dial_named_number("Current OTA Server")
        self.touch_dial_button()

    @Trace(log)
    def dial_set_alpha_ota_server(self, installed_aosp):
        # if the normal downgrade version has the old keyboard layout, set old_keyboard to True
        if int(installed_aosp.split('.')[1]) < 4:
            has_old_keyboard = True
        else:
            has_old_keyboard = False
        self.dial_named_number("Alpha OTA Server", old_keyboard=has_old_keyboard)

    @Trace(log)
    def dial_set_beta_ota_server(self):
        self.dial_named_number("Beta OTA Server")

    @Trace(log)
    def dial_set_production_ota_server(self):
        self.dial_named_number("Production OTA Server")

    @Trace(log)
    def make_call_to_softphone(self):
        softphone = get_softphone()
        softphone.account_info.incoming_response = 200
        for n in list(cfg.site['Users'][cfg.site['DefaultSoftphoneUser']]['UserId']):
            self.click_named_element('NumKey' + n)
        self.touch_dial_button()
        softphone.wait_for_call_status('call', 20)
        sleep(10)
        softphone.end_call()

    @Trace(log)
    def touch_dial_button(self):
        self.click_named_element('DialButton')

    @Trace(log)
    def dial_number(self, number, old_keyboard=False):
        # displayed = self.find_named_element('Digits').text
        # displayed_len = len(displayed)
        for digit in number:
            if old_keyboard:
                x, y = self.digit_centers_old_keyboard[digit]
            else:
                x, y = self.digit_centers[digit]
            TouchAction(self.driver).press(None, x, y).release().wait(250).perform()

    @Trace(log)
    def dial_named_number(self, name, old_keyboard=False):
        self.dial_number(self.numbers[name], old_keyboard=old_keyboard)

    @Trace(log)
    def get_number_buttons(self):
        return self.find_named_elements('NumberButton')

    @Trace(log)
    def touch_call_button(self):
        TouchAction(self.driver).press(None, 301, 821).release().perform()


dial_view = DialView()

