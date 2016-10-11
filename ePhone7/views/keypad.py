from time import sleep

import lib.logging_esi as logging

from ePhone7.utils.configure import cfg
from ePhone7.views.user import UserView
from lib.softphone.softphone import get_softphone
from lib.wrappers import Trace

log = logging.get_logger('esi.keypad_view')


class KeypadView(UserView):

    def __init__(self):
        super(KeypadView, self).__init__()
        self.png_file_base = 'keypad'

    @Trace(log)
    def make_call(self):
        softphone = get_softphone()
        for n in list(cfg.site['Accounts'][cfg.site['DefaultSoftphoneUser']]['UserId']):
            self.click_element_by_key('NumKey' + n)
        self.click_element_by_key('FuncKeyCall')
        softphone.wait_for_call_status('start', 20)
        sleep(10)
        self.click_element_by_key('EndActiveCall')
        softphone.wait_for_call_status('end', 20)

keypad_view = KeypadView()

