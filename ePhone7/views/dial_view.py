from time import sleep

import lib.logging_esi as logging
from ePhone7.config.configure import cfg
from ePhone7.utils.get_softphone import get_softphone
from ePhone7.views.user_view import UserView
from lib.user_exception import UserException as Ux
from lib.wrappers import Trace
from appium.webdriver.common.touch_action import TouchAction

log = logging.get_logger('esi.keypad_view')


class DialView(UserView):

    locators = {
        "CurrentOtaPopup": {"by": "id", "value": "com.esi_estech.ditto:id/title_text", "text": "OTA Server" },
        "CurrentOtaPopupContent": {"by": "id", "value": "com.esi_estech.ditto:id/content_text"},
        "DialPad": {"by": "id", "value": "com.esi_estech.ditto:id/content_dial_pad"},
        "Delete": {"by": "id", "value": "com.esi_estech.ditto:id/deleteButton"},
        "Digits": {"by": "id", "value": "com.esi_estech.ditto:id/digits"},
        "NumKeyAll": {"by": "zpath", "value": "//gv/rl"},
        "FuncKeyAll": {"by": "zpath", "value": "//tl/tr/ll"},
        "NumKey1": {"by": "zpath", "value": "//gv/ll/tv[@text='1']"},
        "NumKey2": {"by": "zpath", "value": "//gv/ll/tv[@text='2']"},
        "NumKey3": {"by": "zpath", "value": "//gv/ll/tv[@text='3']"},
        "NumKey4": {"by": "zpath", "value": "//gv/ll/tv[@text='4']"},
        "NumKey5": {"by": "zpath", "value": "//gv/ll/tv[@text='5']"},
        "NumKey6": {"by": "zpath", "value": "//gv/ll/tv[@text='6']"},
        "NumKey7": {"by": "zpath", "value": "//gv/ll/tv[@text='7']"},
        "NumKey8": {"by": "zpath", "value": "//gv/ll/tv[@text='8']"},
        "NumKey9": {"by": "zpath", "value": "//gv/ll/tv[@text='9']"},
        "NumKeyStar": {"by": "zpath", "value": "//gv/ll/tv[@text='*']"},
        "NumKey0": {"by": "zpath", "value": "//gv/ll/tv[@text='0']"},
        "NumKeyPound": {"by": "zpath", "value": "//gv/ll/tv[@text='#']"},
        "DialButton": {"by": "id", "value": "com.esi_estech.ditto:id/dialButton" },
        "FuncKeySearch": {"by": "id", "value": "com.esi_estech.ditto:id/dialpad_search_button_container" },
        "FuncKeyBksp": {"by": "id", "value": "com.esi_estech.ditto:id/dialpad_delete_button_container" },
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

    digit_corners = {
        '1': [120, 395, 143, 444],
        '2': [289, 396, 312, 445],
        '3': [458, 396, 481, 445],
        '4': [120, 495, 143, 544],
        '5': [289, 495, 312, 544],
        '6': [458, 495, 481, 544],
        '7': [120, 594, 143, 643],
        '8': [289, 594, 312, 643],
        '9': [458, 594, 481, 643],
        '*': [122, 700, 140, 749],
        '0': [289, 692, 312, 741],
        '#': [456, 700, 482, 749]
    }

    digit_centers = {t[0]: [(t[1][0]+t[1][2])/2, (t[1][1]+t[1][3])/2] for t in [(key, digit_corners[key]) for key in digit_corners.keys()]}

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

    @Trace(log)
    def dial_advanced_settings(self):
        self.dial_named_number("Advanced Settings")

    @Trace(log)
    def dial_show_ota_server(self):
        self.dial_named_number("Current OTA Server")
        self.touch_dial_button()

    @Trace(log)
    def dial_set_alpha_ota_server(self):
        self.dial_named_number("Alpha OTA Server")

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
        self.end_call()
        softphone.wait_for_call_status('idle', 20)

    @Trace(log)
    def touch_dial_button(self):
        self.click_named_element('DialButton')

    @Trace(log)
    def dial_number(self, number):
        # displayed = self.find_named_element('Digits').text
        # displayed_len = len(displayed)
        for digit in number:
            x, y = self.digit_centers[digit]
            TouchAction(self.driver).press(None, x, y).release().wait(250).perform()

    @Trace(log)
    def dial_named_number(self, name):
        self.dial_number(self.numbers[name])

    @Trace(log)
    def touch_call_button(self):
        TouchAction(self.driver).press(None, 301, 821).release().perform()


dial_view = DialView()

