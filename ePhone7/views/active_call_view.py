import lib.logging_esi as logging_esi
from ePhone7.config.configure import cfg
from ePhone7.views.base_view import BaseView
from lib.wrappers import Trace

log = logging_esi.get_logger('esi.active_call_view')


class ActiveCallView(BaseView):

    locators = {
        "CallParkButton": {"by": "accessibility id", "value": "Call Park Pickup"},
        "EndActiveCall": {"by": "id", "value": "com.esi_estech.ditto:id/endCallButton"},
        "RecordActiveCall": {"by": "id", "value": "com.esi_estech.ditto:id/recordImageButton"}
    }

    def __init__(self):
        super(ActiveCallView, self).__init__()
        self.cfg = cfg
        self.png_file_base = 'active_call'
        BaseView.active_call_view = self

    @Trace(log)
    def end_call(self):
        self.click_named_element('EndActiveCall')

active_call_view = ActiveCallView()
