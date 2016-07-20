from ePhone7.views.user import UserView
from lib.android.actions import Actions
from lib.common.configure import cfg
from lib.common.user_exception import UserException as Ux
from lib.common.wrappers import Trace
from time import sleep
import lib.common.logging_esi as logging
log = logging.get_logger('esi.voicemail_view')
import re


class VoicemailView(UserView):

    @Trace(log)
    def __init__(self):
        UserView.__init__(self)
        self.actions = Actions(self)
        self.tab_names = ('New', 'Saved', 'Trash')
        self.png_file_base = 'voicemail'
        self.elems = []
        self.saved_vals = {}
        self.new_vals = {}

    @Trace(log)
    def receive_voicemail(self):
        from lib.softphone.softphone import get_softphone
        softphone = get_softphone()
        self.set_dnd(on=True)
        dst_cfg = cfg.site['Accounts']['R2d2User']
        dst_uri = 'sip:' + dst_cfg['UserId'] + '@' + dst_cfg['DomainName']
        softphone.make_call(dst_uri)
        softphone.wait_for_call_status('start', 10)
        softphone.leave_msg()
        self.set_dnd(on=False)
        softphone.teardown_call()

    @Trace(log)
    def call_first_vm_caller(self):
        from lib.softphone.softphone import get_softphone
        # expects the current display to be the detail screen for a voicemail from SoftphoneUser
        softphone = get_softphone()
        self.actions.click_element_by_key('VmCallButton')
        softphone.wait_for_call_status('start', 20)
        sleep(10)
        self.actions.click_element_by_key('EndActiveCall')
        softphone.wait_for_call_status('end', 20)

    @Trace(log)
    def no_vm_activity(self):
        try:
            self.actions.find_elements_by_key('VoicemailParent')
        except Ux as e:
            log.debug("no_vm_activity returning False, User Exception: %s" % e)
            return False
        return True

    @Trace(log)
    def save_voicemail(self):
        self.actions.click_element_by_key('SaveButton')

    @Trace(log)
    def delete_voicemail(self):
        self.actions.click_element_by_key('DeleteButton')

    @Trace(log)
    def swipe_get_vm_parents(self):
        self.swipe_down()
        self.elems = self.actions.find_elements_by_key('VoicemailParent')
        if len(self.elems) > 0:
            return True
        return False

    @Trace(log)
    def get_first_vm_parent(self):
        if not self.actions.wait_for_condition_true(self.swipe_get_vm_parents, seconds=60):
            raise Ux('timed out with no voicemails displayed')
        elem = self.elems[0]
        self.new_vals = {
            'caller_name': self.actions.find_sub_element_by_key(elem, 'CallerName').text,
            'vm_duration': self.actions.find_sub_element_by_key(elem, 'VmDuration').text,
            'caller_number': self.actions.find_sub_element_by_key(elem, 'CallerNumber').text,
            'called_time': self.actions.find_sub_element_by_key(elem, 'CalledTime').text
        }
        log.debug("first vm caller_name = %s" % self.new_vals['caller_name'])
        log.debug("first vm vm_duration = %s" % self.new_vals['vm_duration'])
        log.debug("first vm caller_number = %s" % self.new_vals['caller_number'])
        log.debug("first vm called_time = %s" % self.new_vals['called_time'])
        return elem

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
            if abs(int(m1.group(1)) - int(m2.group(1))) > 1:
                return False
            if m1.group(2) != m2.group(2):
                return False
        log.debug('vm_match returning True')
        return True

    @Trace(log)
    def verify_first_vm(self):
        self.actions.wait_for_condition_true(self.vm_match, seconds=120)

    @Trace(log)
    def clear_all_vm(self):
        while True:
            elems = self.actions.find_elements_by_key('VoicemailParent')
            if len(elems) == 0:
                break
            elems[0].click()
            sleep(5)
            self.actions.find_element_by_key('DeleteButton').click()
            self.swipe_down()
            sleep(5)

voicemail_view = VoicemailView()
