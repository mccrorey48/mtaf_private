import lib.logging_esi as logging_esi
from ePhone7.config.configure import cfg
from ePhone7.views.base_view import BaseView
from lib.wrappers import Trace

log = logging_esi.get_logger('esi.active_call_view')


class ActiveCallView(BaseView):

    locators = {
        "ActiveCallLabel": {"by": "id", "value": "com.esi_estech.ditto:id/call_state", "text": "Active Call"},
        "CallParkButton": {"by": "accessibility id", "value": "Call Park Pickup"},
        "EndActiveCall": {"by": "id", "value": "com.esi_estech.ditto:id/endCallButton"},
        "RecordActiveCall": {"by": "id", "value": "com.esi_estech.ditto:id/recordImageButton"},
        "TranferDialogTitle": {"by": "id", "value": "com.esi_estech.ditto:id/transfer_dialog_title"},
        "TransferToVm": {"by": "id", "value": "com.esi_estech.ditto:id/transfer_vm"}
    }

    def __init__(self):
        super(ActiveCallView, self).__init__()
        self.cfg = cfg
        self.png_file_base = 'active_call'
        BaseView.active_call_view = self

    @Trace(log)
    def end_call(self):
        self.click_named_element('EndActiveCall')

    @Trace(log)
    def is_present(self):
        return self.element_is_present('ActiveCallLabel')

    @Trace(log)
    def transfer_dialog_is_present(self):
        return self.element_is_present('TransferCallDialog')

    def touch_transfer_to_vm(self):
        self.click_named_element('TransferToVm')

active_call_view = ActiveCallView()
