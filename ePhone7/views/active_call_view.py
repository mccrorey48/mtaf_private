from mtaf import mtaf_logging
from mtaf.trace import Trace

from ePhone7.config.configure import cfg
from ePhone7.views.base_view import BaseView

log = mtaf_logging.get_logger('mtaf.active_call_view')


class ActiveCallView(BaseView):

    locators = {
        "ActiveCallControls": {"by": "id", "value": "com.esi_estech.ditto:id/incall_controls"},
        "ActiveCallDial": {"by": "id", "value": "com.esi_estech.ditto:id/dialpadButton"},
        "ActiveCallDialKeys": {"by": "id", "value": "com.esi_estech.ditto:id/dialpad_key_number"},
        "ActiveCallDialpad": {"by": "id", "value": "com.esi_estech.ditto:id/in_call_dialpad"},
        "ActiveCallLabel": {"by": "id", "value": "com.esi_estech.ditto:id/inCallScreenFrame"},
        "AudioPathIcon": {"by": "zpath", "value": "//ll[4]/iv"},
        "CallCardName": {"by": "accessibility id", "value": "Call Park Pickup"},
        "CallParkButton": {"by": "accessibility id", "value": "Call Park Pickup"},
        "CallRecordButton": {"by": "zpath", "value": "//ll[6]/ll/iv"},
        "DefaultForwardAccountName": {"by": "uia_text", "value": cfg.site['DefaultForwardAccount']},
        "EndActiveCall": {"by": "id", "value": "com.esi_estech.ditto:id/endCallButton"},
        "PrimaryCallBanner": {"by": "id", "value": "com.esi_estech.ditto:id/primary_call_button_container"},
        "PrimaryCallName": {"by": "id", "value": "com.esi_estech.ditto:id/call_card_name"},
        "RecordActiveCall": {"by": "id", "value": "com.esi_estech.ditto:id/recordImageButton"},
        "SecondaryCallBanner": {"by": "id", "value": "com.esi_estech.ditto:id/secondaryCallInfo"},
        "SecondaryCallName": {"by": "id", "value": "com.esi_estech.ditto:id/secondaryCallName"},
        "TransferDialogTitle": {"by": "id", "value": "com.esi_estech.ditto:id/transfer_dialog_title"},
        "TransferToVm": {"by": "id", "value": "com.esi_estech.ditto:id/transfer_vm"}
    }

    def __init__(self):
        super(ActiveCallView, self).__init__()
        self.cfg = cfg
        self.png_file_base = 'active_call'
        BaseView.active_call_view = self
        self.presence_element_names = ['ActiveCallLabel']

    @Trace(log)
    def vm_xfer_dest_banner_present(self):
        return self.element_is_present('SecondaryCallBanner')

    @Trace(log)
    def vm_xfer_caller_banner_present(self):
        return self.element_is_present('PrimaryCallBanner')

    @Trace(log)
    def vm_xfer_dest_name(self):
        return self.find_named_element('PrimaryCallName').text

    @Trace(log)
    def vm_xfer_caller_name(self):
        return self.find_named_element('SecondaryCallName').text

    @Trace(log)
    def touch_end_call_button(self):
        self.click_named_element('EndActiveCall')

    @Trace(log)
    def transfer_dialog_is_present(self):
        return self.element_is_present('TransferDialogTitle')

    def touch_transfer_to_vm(self):
        self.click_named_element('TransferToVm')

    @Trace(log)
    def touch_default_forward_account_name(self):
        self.click_named_element('DefaultForwardAccountName')


active_call_view = ActiveCallView()
