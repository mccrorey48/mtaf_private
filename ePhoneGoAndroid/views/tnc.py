import lib.logging_esi as logging

from ePhoneGoAndroid.views.base import BaseView
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
        self.png_file_base = 'tnc'

    @Trace(log)
    def accept_tnc(self):
        self.click_element_by_name('Accept')
        self.click_element_by_name('Continue')
        self.wait_for_activity('.util.AppIntroActivity')

tnc_view = TncView()