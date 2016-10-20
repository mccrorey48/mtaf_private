from time import sleep

import lib.logging_esi as logging

from ePhone7.utils.configure import cfg
from ePhone7.views.user import UserView
from ePhone7.utils.get_softphone import get_softphone
from lib.wrappers import Trace

log = logging.get_logger('esi.keypad_view')


class KeypadView(UserView):

    locators = {
        "NumKeyAll": { "by": "zpath", "value": "//gv/rl" },
        "FuncKeyAll": { "by": "zpath", "value": "//tl/tr/ll" },
        "NumKey1": { "by": "zpath", "value": "//gv/rl[1]" },
        "NumKey2": { "by": "zpath", "value": "//gv/rl[2]" },
        "NumKey3": { "by": "zpath", "value": "//gv/rl[3]" },
        "NumKey4": { "by": "zpath", "value": "//gv/rl[4]" },
        "NumKey5": { "by": "zpath", "value": "//gv/rl[5]" },
        "NumKey6": { "by": "zpath", "value": "//gv/rl[6]" },
        "NumKey7": { "by": "zpath", "value": "//gv/rl[7]" },
        "NumKey8": { "by": "zpath", "value": "//gv/rl[8]" },
        "NumKey9": { "by": "zpath", "value": "//gv/rl[9]" },
        "NumKeyStar": { "by": "zpath", "value": "//gv/rl[10]" },
        "NumKey0": { "by": "zpath", "value": "//gv/rl[11]" },
        "NumKeyPound": { "by": "zpath", "value": "//gv/rl[12]" },
        "FuncKeyCall": { "by": "id", "value": "com.esi_estech.ditto:id/dialButton" },
        "FuncKeySearch": { "by": "id", "value": "com.esi_estech.ditto:id/dialpad_search_button_container" },
        "FuncKeyBksp": { "by": "id", "value": "com.esi_estech.ditto:id/dialpad_delete_button_container" }
    }

    def __init__(self):
        super(KeypadView, self).__init__()
        self.png_file_base = 'keypad'

    @Trace(log)
    def make_call(self):
        softphone = get_softphone()
        for n in list(cfg.site['Users'][cfg.site['DefaultSoftphoneUser']]['UserId']):
            self.click_element_by_key('NumKey' + n)
        self.click_element_by_key('FuncKeyCall')
        softphone.wait_for_call_status('start', 20)
        sleep(10)
        self.click_element_by_key('EndActiveCall')
        softphone.wait_for_call_status('end', 20)

keypad_view = KeypadView()

