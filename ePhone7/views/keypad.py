from time import sleep

import lib.logging_esi as logging

from ePhone7.utils.configure import cfg
from ePhone7.views.user import UserView
from ePhone7.utils.get_softphone import get_softphone
from lib.wrappers import Trace
from lib.user_exception import UserException as Ux

log = logging.get_logger('esi.keypad_view')


class KeypadView(UserView):

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
        "FuncKeyCall": {"by": "id", "value": "com.esi_estech.ditto:id/dialButton" },
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

    numbers = {
        "Current OTA Server": "*682#",
        "Production OTA Server": "*7763#",
        "Alpha OTA Server": "*23742#",
        "Beta OTA Server": "*2382#",
        "Advanced Settings": "*1987"
    }


    def __init__(self):
        super(KeypadView, self).__init__()
        self.png_file_base = 'keypad'

    @Trace(log)
    def make_call_to_softphone(self):
        softphone = get_softphone()
        softphone.account_info.incoming_response = 200
        for n in list(cfg.site['Users'][cfg.site['DefaultSoftphoneUser']]['UserId']):
            self.click_named_element('NumKey' + n)
        self.click_named_element('FuncKeyCall')
        softphone.wait_for_call_status('call', 20)
        sleep(10)
        self.click_named_element('EndActiveCall')
        softphone.wait_for_call_status('idle', 20)

    @Trace(log)
    def dial_number(self, number):
        displayed = self.find_named_element('Digits').text
        displayed_len = len(displayed)
        for digit in number:
            retries = 1
            self.click_named_element(self.digit_names[digit])
            displayed = self.find_named_element('Digits').text
            while len(displayed) < displayed_len + 1:
                if retries == 0:
                    raise Ux("New dialed digit %s not displayed" % digit)
                # try again
                self.click_named_element(self.digit_names[digit])
                retries -= 1
                displayed = self.find_named_element('Digits').text
            if displayed[-1] != digit:
                self.click_named_element('Delete')
                self.click_named_element(self.digit_names[digit])

    @Trace(log)
    def dial_name(self, name):
        self.dial_number(self.numbers[name])

keypad_view = KeypadView()

