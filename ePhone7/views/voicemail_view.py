import re
from time import sleep

import lib.logging_esi as logging
from ePhone7.config.configure import cfg
from ePhone7.views.user_view import UserView
from lib.wrappers import Trace
from lib.user_exception import UserException as Ux
from ePhone7.utils.get_vmids import get_vmids
from lib.filters import get_filter
from selenium.common.exceptions import WebDriverException

log = logging.get_logger('esi.voicemail_view')


class VoicemailView(UserView):
    locators = {
        "CalledTime": {"by": "id", "value": "com.esi_estech.ditto:id/calledTime"},
        "CallerName": {"by": "id", "value": "com.esi_estech.ditto:id/callerName"},
        "CallerNumber": {"by": "id", "value": "com.esi_estech.ditto:id/callerNumber"},
        "DeleteButton": {"by": "id", "value": "com.esi_estech.ditto:id/delete_voicemail"},
        "EndCall": {"by": "uia_text", "value": "END CALL"},
        "ForwardButton": {"by": "id", "value": "com.esi_estech.ditto:id/forward_voicemail"},
        "New": {"by": "zpath", "value": "//bt[@text='NEW']"},
        "NoVoicemails": {"by": "id", "value": "com.esi_estech.ditto:id/call_log_empty"},
        "OkForwardButton": {"by": "id", "value": "com.esi_estech.ditto:id/forward_dialog_ok_button"},
        "PlaybackStartStop": {"by": "id", "value": "com.esi_estech.ditto:id/playback_start_stop"},
        "SaveButton": {"by": "id", "value": "com.esi_estech.ditto:id/save_voicemail"},
        "Saved": {"by": "zpath", "value": "//ll/bt[@text='SAVED']"},
        "ShareButton": {"by": "id", "value": "com.esi_estech.ditto:id/share_voicemail"},
        "Trash": {"by": "zpath", "value": "//ll/bt[@text='TRASH']"},
        "VmButton": {"by": "id", "value": "com.esi_estech.ditto:id/vm_button"},
        "VmCallButton": {"by": "id", "value": "com.esi_estech.ditto:id/vm_call_button"},
        "VmDetailHeader": {"by": "id", "value": "com.esi_estech.ditto:id/vm_user_header_layout"},
        "VmDuration": {"by": "id", "value": "com.esi_estech.ditto:id/vmDuration"},
        "VmFrame": {"by": "zpath", "value": "//rv"},
        "VmParents": {"by": "zpath", "value": "//rv/rl"},
        "Vm1Parent": {"by": "zpath", "value": "//rv/rl[1]"},
        "Vm1Texts": {"by": "zpath", "value": "(//rv/rl[1])/tv"},
    }

    def __init__(self):
        super(VoicemailView, self).__init__()
        self.tab_names = ('New', 'Saved', 'Trash')
        self.png_file_base = 'voicemail'
        self.elems = []
        self.saved_vals = {}
        self.new_vals = {}

    @Trace(log)
    def call_first_vm_caller(self):
        from ePhone7.utils.get_softphone import get_softphone
        # expects the current display to be the detail screen for a voicemail from cfg.site['DefaultSoftphoneUser']
        softphone = get_softphone()
        softphone.account_info.incoming_response = 200
        self.click_named_element('VmCallButton')
        softphone.wait_for_call_status('call', 20)
        sleep(10)
        softphone.end_call()
        softphone.wait_for_call_status('idle', 20)
        self.click_named_element('VmDetailHeader')

    @Trace(log)
    def save_open_voicemail(self):
        self.click_named_element('SaveButton')

    @Trace(log)
    def delete_voicemail_button(self):
        self.click_named_element('DeleteButton')

    @Trace(log)
    def swipe_get_vm_parents(self):
        frame = self.find_named_element('VmFrame')
        self.swipe_down()
        self.elems = self.find_named_elements("VmParents", filter_fn=get_filter("within_frame", frame=frame))
        if len(self.elems) > 0:
            return True
        return False

    @Trace(log)
    def get_first_vm_parent(self):
        self.wait_for_condition_true(self.swipe_get_vm_parents,
                                     lambda: 'no voicemails displayed', timeout=60)
        elem = self.elems[0]
        self.new_vals = {
            'caller_name': self.find_named_sub_element(elem, 'CallerName').text,
            'vm_duration': self.find_named_sub_element(elem, 'VmDuration').text,
            'caller_number': self.find_named_sub_element(elem, 'CallerNumber').text,
            'called_time': self.find_named_sub_element(elem, 'CalledTime').text
        }
        log.debug("first vm caller_name = %s" % self.new_vals['caller_name'])
        log.debug("first vm vm_duration = %s" % self.new_vals['vm_duration'])
        log.debug("first vm caller_number = %s" % self.new_vals['caller_number'])
        log.debug("first vm called_time = %s" % self.new_vals['called_time'])
        return elem

    @Trace(log)
    def first_vm_opened(self):
        self.click_element(self.get_first_vm_parent())
        try:
            self.find_named_element('DeleteButton')
        except:
            return False
        return True

    @Trace(log)
    def open_first_vm(self):
        self.wait_for_condition_true(self.first_vm_opened, lambda: 'first vm not opened', timeout=30)
        self.click_named_element('PlaybackStartStop')

    @Trace(log)
    def save_first_vm_vals(self):
        for key in self.new_vals:
            self.saved_vals[key] = self.new_vals[key]

    @Trace(log)
    def vm_match(self):
        re_called_time = re.compile('(\d+)\s+(minute|hour)')
        self.get_first_vm_parent()
        m1 = re_called_time.match(self.new_vals['called_time'])
        m2 = re_called_time.match(self.saved_vals['called_time'])
        log.debug("caller_name: expected %s, actual %s" % (self.saved_vals['caller_name'], self.new_vals['caller_name']))
        log.debug("vm_duration: expected %s, actual %s" % (self.saved_vals['vm_duration'], self.new_vals['vm_duration']))
        log.debug("caller_number: expected %s, actual %s" % (self.saved_vals['caller_number'], self.new_vals['caller_number']))
        log.debug("called_time: expected %s, actual %s" % (self.saved_vals['called_time'], self.new_vals['called_time']))
        if self.new_vals['caller_name'] != self.saved_vals['caller_name']:
            return False
        if self.new_vals['vm_duration'] != self.saved_vals['vm_duration']:
            return False
        if self.new_vals['caller_number'] != self.saved_vals['caller_number']:
            return False
        if m1 and m2:
            if abs(int(m1.group(1)) - int(m2.group(1))) > 4:
                return False
            if m1.group(2) != m2.group(2):
                return False
        log.debug('vm_match returning True')
        return True

    @Trace(log)
    def verify_first_vm(self):
        self.wait_for_condition_true(self.vm_match, lambda: 'first voicemail not a match', timeout=120)

    @Trace(log)
    def clear_all_vm(self):
        while True:
            elems = [elem for elem in self.find_named_elements('VmParents') if elem.size['width'] != 0]
            if len(elems) == 0:
                break
            self.click_element(elems[0])
            sleep(5)
            self.click_named_element('DeleteButton')
            self.swipe_down()
            sleep(5)

    @Trace(log)
    def forward_open_voicemail(self):
        self.click_named_element('ForwardButton')
        user_cfg = cfg.site['Users'][cfg.site['DefaultForwardAccount']]
        for n in list(user_cfg['UserId']):
            self.send_keycode_number(n)
        self.click_named_element('OkForwardButton')

    @Trace(log)
    def compare_vmid(self, vmid1):
        username=cfg.site['DefaultForwardAccount']
        fwd_vmids = get_vmids(username, 'new')
        for fwd_vmid in fwd_vmids:
            if vmid1 == fwd_vmid:
                return
        raise Ux("vmid %s not found in user %s's mailbox" % (vmid1, username))

    @Trace(log)
    def verify_forward(self):
        self.wait_for_condition_true(self.compare_vmid, lambda: 'voicemail was not a match', seconds=120)

    @Trace(log)
    def get_top_vm_parents(self):
        frame = self.find_named_element('VmFrame')
        parents = self.find_named_elements("VmParents", filter_fn=get_filter("within_frame", frame=frame))
        if len(parents) > 0:
            old_top_y = parents[0].location['y']
            for tries in range(10):
                self.swipe(300, 0, 300, 975)
                try:
                    top_y = parents[0].location['y']
                except WebDriverException as e:
                    print "got WebDriverException: %s" % e
                    parents = self.find_named_elements("VmParents", filter_fn=get_filter("within_frame", frame=frame))
                    if len(parents) == 0:
                        raise Ux("no VmParent elements found within VmFrame")
                    top_y = parents[0].location['y']
                if top_y == old_top_y:
                    break
                old_top_y = top_y
            else:
                raise Ux("could not scroll to too of vm list")
        return parents


voicemail_view = VoicemailView()
