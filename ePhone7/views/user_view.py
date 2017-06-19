from time import sleep

import lib.logging_esi as logging_esi
from ePhone7.config.configure import cfg
from ePhone7.utils.get_softphone import get_softphone
from ePhone7.views.base_view import BaseView
from ePhone7.views.prefs_view import prefs_view
from lib.user_exception import UserException as Ux
from lib.wrappers import Trace

log = logging_esi.get_logger('esi.user_view')


class UserView(BaseView):

    locators = {
        "InCallDial": {"by": "id", "value": "com.esi_estech.ditto:id/keypad_tab"},
        "Contacts": {"by": "zpath", "value": "//tw/rl[1]/ll/tv", "text": "Contacts"},
        "Dial": {"by": "id", "value": "com.esi_estech.ditto:id/keypad_text", "text": "Dial"},
        "DndButton": {"by": "accessibility id", "value": "Do not Disturb"},
        "EhelpButton": {"by": "accessibility id", "value": "eHelp"},
        "History": {"by": "zpath", "value": "//tw/rl[2]/ll/tv", "text": "History"},
        "IncomingCallAnswerToHeadset": {"by": "id", "value": "com.esi_estech.ditto:id/answer_to_headset_button"},
        "IncomingCallIgnore": {"by": "id", "value": "com.esi_estech.ditto:id/ignore_button"},
        "IncomingCallAnswerToSpeaker": {"by": "id", "value": "com.esi_estech.ditto:id/answer_to_speaker_button"},
        "IncomingCallLabel": {"by": "id", "value": "com.esi_estech.ditto:id/incoming_call_label"},
        "IncomingCallCallerImage": {"by": "id", "value": "com.esi_estech.ditto:id/incoming_call_caller_image"},
        "IncomingCallCallerName": {"by": "id", "value": "com.esi_estech.ditto:id/incoming_call_caller_name"},
        "IncomingCallCallerNumber": {"by": "id", "value": "com.esi_estech.ditto:id/incoming_call_caller_number"},
        "HomeScreenLogo": {"by": "id", "value": "com.esi_estech.ditto:id/home_screen_company_logo"},
        "PrefsButton": {"by": "id", "value": "com.esi_estech.ditto:id/settings_button"},
        "PrefsButtonz": {"by": "zpath", "value": "//rl/bt[4]"},
        "SettingsButton": {"by": "zpath", "value": "//sv/fl/fl[3]"},
        "SettingsButtonText": {"by": "zpath", "value": "//sv/fl/fl[3]/ll/tv"},
        "TestOtaAlertTitle": {"by": "id", "value": "com.esi_estech.ditto:id/alertTitle", "text": "Set OTA Server Address"},
        "UserHeaderName": {"by": "id", "value": "com.esi_estech.ditto:id/user_header_name"},
        "Voicemail": {"by": "zpath", "value": "//tw/rl[3]/ll/tv", "text": "Voicemail"}
    }

    def __init__(self):
        super(UserView, self).__init__()
        self.cfg = cfg
        self.tab_names = ('Contacts', 'History', 'Voicemail', 'Dial')
        self.png_file_base = 'user'
        self.expected_tab = None
        self.active_tab = None
        self.call_status_wait = 30
        self.softphones = {}

    # @Trace(log)
    # def logout(self):
    #     self.goto_prefs()
    #     prefs_view.logout()
    #     prefs_view.logout_confirm()
    #     self.wait_for_condition_true(lambda: remote.current_activity == '.settings.ui.LoginActivity')

    @Trace(log)
    def set_dnd(self, on=True):
        if on:
            desired_color = cfg.colors['UserView']['dnd_on_color'][:-1]
        else:
            desired_color = cfg.colors['UserView']['dnd_off_color'][:-1]
        elem = self.find_named_element('DndButton')
        self.get_screenshot_as_png('set_dnd', cfg.test_screenshot_folder)
        current_color = self.get_element_color('set_dnd', elem)
        if current_color != desired_color:
            self.click_element(elem)
            sleep(5)
        self.get_screenshot_as_png('set_dnd', cfg.test_screenshot_folder)
        current_color = self.get_element_color('set_dnd', elem)
        if current_color != desired_color:
            raise Ux('unable to set dnd icon to desired color %s, current color is %s' % (desired_color, current_color))

    @Trace(log)
    def swipe_up(self):
        self.swipe(300, 750, 300, 250, 1500)
        sleep(2)

    @Trace(log)
    def swipe_down(self):
        self.swipe(300, 250, 300, 750, 750)
        sleep(2)

    @Trace(log)
    def swipe_elem_to_center(self, elem):
        old_y = elem.location['y']
        new_y = 512
        if abs(old_y - new_y) > (elem.size['height'] + 100):
            self.swipe(300, old_y, 300, new_y, 750)
            sleep(2)

    @Trace(log)
    def end_call(self):
        self.active_call_view.end_call()

    @Trace(log)
    def goto_tab(self, tab_name):
        self.expected_tab = tab_name
        failmsg_fmt = 'expect active tab to be %s, got %s'
        self.wait_for_condition_true(self.verify_active_tab,
                                             lambda: failmsg_fmt % (self.expected_tab, self.active_tab), timeout=120)

    @Trace(log)
    def get_logo_element(self):
        return self.find_named_element('HomeScreenLogo')

    @Trace(log)
    def goto_prefs(self):
        self.wait_for_condition_true(self.verify_prefs_view,
                                             lambda: "prefs view not present", timeout=60)

    @Trace(log)
    def verify_prefs_view(self):
        self.click_named_element('PrefsButton')
        return prefs_view.verify_view()

    @Trace(log)
    def verify_active_tab(self):
        # for use with wait_for_condition_true
        # click the tab expected to become active
        # after a few seconds, test to see if it has become the active tab by looking at its color
        # if it is active, return true
        # if another tab is active, return false
        # if no tab is active, raise an exception
        self.click_named_element(self.expected_tab)
        sleep(5)
        self.get_screenshot_as_png(self.png_file_base, cfg.test_screenshot_folder)
        self.active_tab = None
        for tab_name in self.tab_names:
            tab_color = self.get_tab_color(self.png_file_base, tab_name)
            log.debug("get_tab_color(%s, %s) returned %s" % (self.png_file_base, tab_name, tab_color))
            if tab_color == 'active_color':
                self.active_tab = tab_name
                break
        return self.active_tab == self.expected_tab

    @Trace(log)
    def receive_call(self, caller_name=None, wait_for_status='early', wait_timeout=None):
        if caller_name is None:
            caller_name = cfg.site['DefaultSoftphoneUser']
        if wait_timeout is None:
            wait_timeout = self.call_status_wait
        self.softphones[caller_name] = get_softphone(caller_name)
        src_cfg = cfg.site['Users'][caller_name]
        dst_cfg = cfg.site['Users']['R2d2User']
        dst_uri = 'sip:' + dst_cfg['UserId'] + '@' + dst_cfg['DomainName']
        self.softphones[caller_name].make_call(dst_uri)
        self.softphones[caller_name].wait_for_call_status(wait_for_status, wait_timeout)
        return caller_name, src_cfg

    @Trace(log)
    def configure_called_answer_ring(self, called_name=None):
        if called_name is None:
            called_name = cfg.site['DefaultSoftphoneUser']
        self.softphones[called_name] = get_softphone(called_name)
        self.softphones[called_name].account_info.incoming_response = 180
        return self.softphones[called_name]


    @Trace(log)
    def incoming_call_screen_test(self):
        caller_name, src_cfg  = self.receive_call()
        self.find_named_element('IncomingCallAnswerToHeadset')
        self.find_named_element('IncomingCallAnswerToSpeaker')
        self.wait_for_named_element_text('IncomingCallCallerName', src_cfg['UserNameIncoming'])
        self.wait_for_named_element_text('IncomingCallCallerNumber', src_cfg['UserId'])
        self.softphones[caller_name].end_call()

    @Trace(log)
    def answer_call_test(self):
        caller_name, src_cfg = self.receive_call()
        self.click_named_element('IncomingCallAnswerToSpeaker')
        self.softphones[caller_name].wait_for_call_status('call', self.call_status_wait)
        self.end_call()
        self.softphones[caller_name].wait_for_call_status('idle', self.call_status_wait)

    @Trace(log)
    def auto_answer_call_test(self):
        softphone = get_softphone()
        dst_cfg = cfg.site['Users']['R2d2User']
        dst_uri = 'sip:' + dst_cfg['UserId'] + '@' + dst_cfg['DomainName']
        softphone.make_call(dst_uri)
        softphone.wait_for_call_status('call', self.call_status_wait)
        self.end_call()
        softphone.wait_for_call_status('idle', self.call_status_wait)

    @Trace(log)
    def ignore_call_test(self):
        softphone = get_softphone()
        dst_cfg = cfg.site['Users']['R2d2User']
        dst_uri = 'sip:' + dst_cfg['UserId'] + '@' + dst_cfg['DomainName']
        softphone.make_call(dst_uri)
        softphone.wait_for_call_status('early', self.call_status_wait)
        self.click_named_element('IncomingCallIgnore')
        # the softphone caller will hear ringing until the max number of rings occurs, then
        # the softphone status will change to "call" because pbx accepts the invite to play
        # the "unavailable" message
        #
        # this is probably not how it is supposed to work...I think the caller should be sent to the
        # "unavailable" message immediately when "ignore call" is touched. In this case the
        # 40 second wait for call status is way too long
        wait_time = softphone.wait_for_call_status('call', 40)
        log.debug('got "call" status in %s seconds' % wait_time)
        softphone.set_monitor_on()
        sleep(10)
        # could insert a sleep here and do a fingerprint analysis of the recorded audio file
        softphone.set_monitor_off()
        softphone.end_call()


user_view = UserView()
