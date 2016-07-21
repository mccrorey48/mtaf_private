from ePhone7.views.user import UserView
from lib.android.actions import Actions
from lib.common.configure import cfg
from time import sleep
from lib.common.wrappers import Trace
from lib.softphone.softphone import get_softphone
import lib.common.logging_esi as logging
log = logging.get_logger('esi.keypad_view')


class KeypadView(UserView):

    @Trace(log)
    def __init__(self):
        UserView.__init__(self)
        self.actions = Actions(self)
        self.png_file_base = 'keypad'

    @Trace(log)
    def make_call(self):
        softphone = get_softphone()
        for n in list(cfg.site['Accounts']['Auto TesterC']['UserId']):
            self.actions.click_element_by_key('NumKey' + n)
        self.actions.click_element_by_key('FuncKeyCall')
        softphone.wait_for_call_status('start', 20)
        sleep(10)
        self.actions.click_element_by_key('EndActiveCall')
        softphone.wait_for_call_status('end', 20)

keypad_view = KeypadView()

