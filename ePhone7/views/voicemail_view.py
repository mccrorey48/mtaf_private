from mtaf import mtaf_logging
from mtaf.trace import Trace
from mtaf.filters import get_filter
from mtaf.user_exception import UserException as Ux

from ePhone7.config.configure import cfg
from ePhone7.views.user_view import UserView

import re
from datetime import datetime, timedelta
from time import sleep, time
import datetime
from selenium.common.exceptions import WebDriverException

log = mtaf_logging.get_logger('mtaf.voicemail_view')


class VoicemailView(UserView):
    locators = {
        "CalledTime": {"by": "id", "value": "com.esi_estech.ditto:id/calledTime"},
        "CallerName": {"by": "id", "value": "com.esi_estech.ditto:id/callerName"},
        "CallerNumber": {"by": "id", "value": "com.esi_estech.ditto:id/callerNumber"},
        "CancelForwardButton": {"by": "id", "value": "com.esi_estech.ditto:id/forward_dialog_cancel_button"},
        "DeleteButton": {"by": "id", "value": "com.esi_estech.ditto:id/delete_voicemail"},
        "EndCall": {"by": "uia_text", "value": "END CALL"},
        "ForwardDialogTitle": {"by": "id", "value": "com.esi_estech.ditto:id/forward_dialog_title"},
        "ForwardText": {"by": "id", "value": "com.esi_estech.ditto:id/forward_text"},
        "ForwardList": {"by": "id", "value": "android:id/list"},
        "ForwardButton": {"by": "id", "value": "com.esi_estech.ditto:id/forward_voicemail"},
        "NewTab": {"by": "id", "value": "com.esi_estech.ditto:id/new_vm_btn"},
        "NoVoicemails": {"by": "id", "value": "com.esi_estech.ditto:id/call_log_empty"},
        "OkForwardButton": {"by": "id", "value": "com.esi_estech.ditto:id/forward_dialog_ok_button"},
        "PlaybackStartStop": {"by": "id", "value": "com.esi_estech.ditto:id/playback_start_stop"},
        "SavedTab": {"by": "id", "value": "com.esi_estech.ditto:id/saved_vm_btn"},
        "SaveButton": {"by": "id", "value": "com.esi_estech.ditto:id/save_voicemail"},
        "SearchItem": {"by": "id", "value": "com.esi_estech.ditto:id/contact_search_item_layout"},
        "SearchNumber": {"by": "id", "value": "com.esi_estech.ditto:id/search_number"},
        "ShareButton": {"by": "id", "value": "com.esi_estech.ditto:id/share_voicemail"},
        "TrashTab": {"by": "id", "value": "com.esi_estech.ditto:id/deleted_vm_btn"},
        "VmButton": {"by": "id", "value": "com.esi_estech.ditto:id/vm_button"},
        "VmCallButton": {"by": "id", "value": "com.esi_estech.ditto:id/vm_call_button"},
        "VmDetailHeader": {"by": "id", "value": "com.esi_estech.ditto:id/vm_user_header_layout"},
        "VmDuration": {"by": "id", "value": "com.esi_estech.ditto:id/vmDuration"},
        "VmFrame": {"by": "id", "value": "com.esi_estech.ditto:id/swipeContainer"},
        "VmParents": {"by": "zpath", "value": "//rv/rl"},
        "Vm1Parent": {"by": "zpath", "value": "//rv/rl[1]"},
        "Vm1Texts": {"by": "zpath", "value": "(//rv/rl[1])/tv"},
    }

    def __init__(self):
        super(VoicemailView, self).__init__()
        self.tab_names = ('NewTab', 'SavedTab', 'TrashTab')
        self.png_file_base = 'voicemail'
        self.elems = []
        self.saved_vals = {}
        self.new_vals = {}
        self.presence_element_names = ['NewTab', 'SavedTab', 'TrashTab']

    @Trace(log)
    def call_first_vm_caller(self):
        from ePhone7.utils import get_softphone
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
    def wait_for_first_vm_match(self, caller_name, caller_number, vm_duration, timeout):
        start_time = time()
        first_name = None
        first_number = None
        first_duration = None
        while time() - start_time < timeout:
            first_name = self.all.CallerName[0].text
            first_number = self.all.CallerNumber[0].text
            first_duration = self.all.VmDuration[0].text
            if first_name == caller_name and first_number == caller_number and first_duration == vm_duration:
                break
        else:
            log.debug("%s seconds timeout reached with no vm match" % timeout)
        return {'CallerName': first_name, 'CallerNumber': first_number, 'VmDuration': first_duration}

    @Trace(log)
    def first_vm_opened(self):
        self.click_element(self.get_first_vm_parent())
        try:
            self.find_named_element('DeleteButton')
        except BaseException:
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
    def get_top_vm_texts(self):
        top_vm_texts = []
        parents = self.get_top_vm_parents()
        for parent in parents:
            top_vm_texts.append({
                "CallerName": voicemail_view.find_named_sub_element(parent, "CallerName").text,
                "CallerNumber": voicemail_view.find_named_sub_element(parent, "CallerNumber").text,
                "CalledTime": voicemail_view.find_named_sub_element(parent, "CalledTime").text,
                "VmDuration": voicemail_view.find_named_sub_element(parent, "VmDuration").text
            })
        return top_vm_texts

    @Trace(log)
    def vm_match_all(self, displayed_vm_texts, vm_metadata_all):
        if len(vm_metadata_all) < len(displayed_vm_texts):
            raise Ux("VM metadata has fewer elements than displayed_vm_texts")
        for i in range(len(displayed_vm_texts)):
            md = vm_metadata_all[i]
            log.debug("(vvm api) %s  %s  %s  %s sec" % (md['callerName'], md['callerNumber'],
                                                        md['dateRecorded'], md['duration']))
            vm_texts = displayed_vm_texts[i]
            log.debug('(vm view) %s  %s  %s  %s' % (vm_texts['CallerName'], vm_texts['CallerNumber'],
                                                    vm_texts['CalledTime'], vm_texts['VmDuration']))
            # check the name, number and duration for an exact text match
            if md['callerName'] != vm_texts['CallerName']:
                log.debug("%s != %s; returning False" % (md['callerName'], vm_texts['CallerName']))
                return False
            if md['callerNumber'] != vm_texts['CallerNumber']:
                log.debug("%s != %s; returning False" % (md['callerNumber'], vm_texts['CallerNumber']))
                return False
            # convert the vm_texts['VmDuration'] from "x min, y sec" to the equivalent number of seconds
            # to compare it to the md['duration'] value
            terms = vm_texts['VmDuration'].split()
            if len(terms) == 4 and terms[1] == 'min' and terms[3] == 'sec':
                secs_displayed = int(terms[0]) * 60 + int(terms[2])
            elif len(terms) == 2 and terms[1] == 'sec':
                secs_displayed = int(terms[0])
            else:
                raise Ux('VM duration string "%s" has unknown format' % vm_texts['VmDuration'])
            if not md['duration'] - 2 <= secs_displayed <= md['duration'] + 2:
                log.debug("%d sec != %s; returning False" % (md['duration'], vm_texts['VmDuration']))
                return False
            # check the displayed age against the metadata timestamp by calculating the vm age in minutes from the
            # metadata timestamp, then comparing it to a calculated valid range of ages (in minutes) represented by the
            # displayed age text
            md_age = self.get_age_minutes(md['dateRecorded'])
            vm_min_age, vm_max_age = get_age_range_minutes(vm_texts['CalledTime'])
            if not vm_min_age <= md_age <= vm_max_age:
                log.debug("vm index %d:  vm_min_age: %d,  md_age: %d,  vm_max_age: %d; returning False")
                return False
        return True

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

    @staticmethod
    @Trace(log)
    def get_age_minutes(timestamp):
        # timestamp is in format of vm metadata "dateRecorded" field: 'YYYY-MM-DD hh:mm:ss'
        utcnow = datetime.datetime.utcnow()
        timestamp_dt = datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
        delta = utcnow - timestamp_dt
        return delta.days * 24 * 60 + delta.seconds / 60


voicemail_view = VoicemailView()


def get_age_range_minutes(display_age, delta_minutes=2):
    # analyze the displayed vm age and return a min and max age (in minutes)
    # that would match the age of the timestamp in the vm metadata "dateRecorded" field
    # min_age = 0
    # max_age = 0
    if display_age == 'in 0 minutes':
        min_age = 0
        max_age = 0
    elif display_age.endswith(' minutes ago') or display_age == '1 minute ago':
        age = int(display_age.split()[0])
        min_age = age
        max_age = age
    elif display_age.endswith(' hours ago') or display_age == '1 hour ago':
        age = int(display_age.split()[0]) * 60
        min_age = age
        max_age = age + 59
    elif display_age == 'Yesterday':
        now = datetime.now()
        midnight = datetime(now.year, now.month, now.day)
        oldest = midnight - timedelta(days=1)
        newest = midnight - timedelta(minutes=1)
        min_age = int((now - newest).total_seconds())/60
        max_age = int((now - oldest).total_seconds())/60
    elif display_age.endswith(' days ago'):
        days = int(display_age.split()[0])
        now = datetime.now()
        midnight = datetime(now.year, now.month, now.day)
        oldest = midnight - timedelta(days=days)
        newest = midnight - timedelta(days=days - 1, minutes=1)
        min_age = int((now - newest).total_seconds())/60
        max_age = int((now - oldest).total_seconds())/60
    else:
        date = datetime.strptime(display_age, '%b %d, %Y')
        now = datetime.now()
        midnight = datetime(now.year, now.month, now.day)
        days = (now - date).days
        oldest = midnight - timedelta(days=days)
        newest = midnight - timedelta(days=days - 1, minutes=1)
        min_age = int((now - newest).total_seconds())/60
        max_age = int((now - oldest).total_seconds())/60
    return max(min_age - delta_minutes, 0), max_age + delta_minutes