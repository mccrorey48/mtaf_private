from time import sleep

import lib.common.logging_esi as logging
from ePhone7.utils.configure import cfg
from ePhone7.views.user import UserView
from lib.common.wrappers import Trace
from lib.softphone.softphone import get_softphone

log = logging.get_logger('esi.keypad_view')


class KeypadView(UserView):

    @Trace(log)
    def __init__(self):
        super(KeypadView, self).__init__()
        self.png_file_base = 'keypad'

    @Trace(log)
    def make_call(self):
        softphone = get_softphone()
        for n in list(cfg.site['Accounts'][cfg.site['DefaultSoftphoneUser']]['UserId']):
            self.actions.click_element_by_key('NumKey' + n)
        self.actions.click_element_by_key('FuncKeyCall')
        softphone.wait_for_call_status('start', 20)
        sleep(10)
        self.actions.click_element_by_key('EndActiveCall')
        softphone.wait_for_call_status('end', 20)

keypad_view = KeypadView()

