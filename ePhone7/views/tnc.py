from lib.android.actions import Actions
from lib.common.remote import remote
from lib.common.wrappers import Trace
import lib.common.logging_esi as logging
log = logging.get_logger('esi.tnc_view')


class TncView:

    @Trace(log)
    def __init__(self):
        self.actions = Actions(self)

    @Trace(log)
    def not_tnc_activity(self):
        return remote.driver.current_activity != '.settings.ui.TernsAndConditionsScreen'

    @Trace(log)
    def accept_tnc(self):
        self.actions.click_element_by_key('Accept')
        self.actions.click_element_by_key('Continue')
        testfn = lambda: remote.driver.current_activity != '.settings.ui.TernsAndConditionsScreen'
        failmsg_fn = lambda: 'failed to leave activity .settings.ui.TermsAndConditionsScreen'
        self.actions.wait_for_condition_true(testfn, failmsg_fn)

tnc_view = TncView()
