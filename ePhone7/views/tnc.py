import lib.logging_esi as logging

from ePhone7.views.base import BaseView
from lib.wrappers import Trace

log = logging.get_logger('esi.tnc_view')


class TncView(BaseView):

    locators = {
        "Accept": {"by": "id", "value": "com.esi_estech.ditto:id/TnC_checkBox_continue"},
        "Continue": {"by": "id", "value": "com.esi_estech.ditto:id/TnC_continueBtn"},
        "Login": {"by": "id", "value": "com.esi_estech.ditto:id/login_button"}
    }

    def __init__(self):
        super(TncView, self).__init__()

    @Trace(log)
    def not_tnc_activity(self):
        return self.current_activity != '.settings.ui.TernsAndConditionsScreen'

    @Trace(log)
    def accept_tnc(self):
        self.click_element_by_key('Accept')
        self.click_element_by_key('Continue')
        testfn = lambda: self.current_activity != '.settings.ui.TernsAndConditionsScreen'
        failmsg_fn = lambda: 'activity is still .settings.ui.TermsAndConditionsScreen'
        self.wait_for_condition_true(testfn, failmsg_fn)

tnc_view = TncView()
