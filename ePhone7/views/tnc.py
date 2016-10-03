import lib.common.logging_esi as logging
from lib.android.remote import remote
from lib.common.wrappers import Trace
from ePhone7.views.base import BaseView

log = logging.get_logger('esi.tnc_view')


class TncView(BaseView):

    @Trace(log)
    def __init__(self):
        super(TncView, self).__init__()

    @Trace(log)
    def not_tnc_activity(self):
        return remote.driver.current_activity != '.settings.ui.TernsAndConditionsScreen'

    @Trace(log)
    def accept_tnc(self):
        self.actions.click_element_by_key('Accept')
        self.actions.click_element_by_key('Continue')
        testfn = lambda: remote.driver.current_activity != '.settings.ui.TernsAndConditionsScreen'
        failmsg_fn = lambda: 'activity is still .settings.ui.TermsAndConditionsScreen'
        self.actions.wait_for_condition_true(testfn, failmsg_fn)

tnc_view = TncView()
