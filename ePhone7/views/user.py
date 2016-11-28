from time import sleep

import lib.logging_esi as logging_esi
from lib.wrappers import Trace

from ePhone7.utils.configure import cfg
from ePhone7.views.base import BaseView
from ePhone7.views.prefs import prefs_view
from lib.user_exception import UserException as Ux

log = logging_esi.get_logger('esi.user_view')


class UserView(BaseView):

    locators = {
        "CallParkButton": {"by": "accessibility id", "value": "Call Park Pickup"},
        "Contacts": {"by": "zpath", "value": "//tw/rl[1]/ll/tv", "text": "Contacts"},
        "DndButton": {"by": "accessibility id", "value": "Do not Disturb"},
        "EndActiveCall": {"by": "id", "value": "com.esi_estech.ditto:id/endButtonImage"},
        "EhelpButton": {"by": "accessibility id", "value": "eHelp"},
        "History": {"by": "zpath", "value": "//tw/rl[2]/ll/tv", "text": "History"},
        "Keypad": {"by": "id", "parent": "com.esi_estech.ditto:id/keypad_tab", "value": "com.esi_estech.ditto:id/keypad_text", "text": "Dial"},
        "IncomingCallAnswerToHeadset": {"by": "id", "value": "com.esi_estech.ditto:id/answer_to_headset_button"},
        "IncomingCallIgnore": {"by": "id", "value": "com.esi_estech.ditto:id/ignore_button"},
        "IncomingCallAnswerToSpeaker": {"by": "id", "value": "com.esi_estech.ditto:id/answer_to_speaker_button"},
        "IncomingCallLabel": {"by": "id", "value": "com.esi_estech.ditto:id/incoming_call_label"},
        "IncomingCallCallerImage": {"by": "id", "value": "com.esi_estech.ditto:id/incoming_call_caller_image"},
        "IncomingCallCallerName": {"by": "id", "value": "com.esi_estech.ditto:id/incoming_call_caller_name"},
        "IncomingCallCallerNumber": {"by": "id", "value": "com.esi_estech.ditto:id/incoming_call_caller_number"},
        "PrefsButton": {"by": "id", "value": "com.esi_estech.ditto:id/settings_button"},
        "PrefsButtonz": {"by": "zpath", "value": "//rl[2]/bt[5]"},
        "SettingsButton": {"by": "zpath", "value": "//sv/fl/fl[3]"},
        "SettingsButtonText": {"by": "zpath", "value": "//sv/fl/fl[3]/ll/tv"},
        "UserHeaderName": {"by": "id", "value": "com.esi_estech.ditto:id/user_header_name"},
        "UserProximityStatus": {"by": "id", "value": "com.esi_estech.ditto:id/user_proximity_status"},
        "Voicemail": {"by": "zpath", "value": "//tw/rl[3]/ll/tv", "text": "Voicemail"}
    }

    def __init__(self):
        super(UserView, self).__init__()
        self.cfg = cfg
        self.tab_names = ('Contacts', 'History', 'Voicemail', 'Keypad')
        self.png_file_base = 'user'
        self.expected_tab = None
        self.active_tab = None
        self.call_status_wait = 30

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
        elem = self.find_element_by_key('DndButton')
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
        self.click_element_by_key('EndActiveCall')

    @Trace(log)
    def goto_settings(self):
        sleep(2.0)
        self.swipe(515, 12, 515, 250, 400)
        self.swipe(515, 12, 515, 250, 400)
        elem = self.find_element_by_key('SettingsButtonText')
        self.assert_element_text_ic(elem, 'settings', 'button')
        # Touch settings, settings menu appears with "Apps" item
        self.tap_element(elem)

    @Trace(log)
    def goto_tab(self, tab_name):
        self.expected_tab = tab_name
        failmsg_fmt = 'expect active tab to be %s, got %s'
        self.wait_for_condition_true(self.verify_active_tab,
                                             lambda: failmsg_fmt % (self.expected_tab, self.active_tab), timeout=120)

    @Trace(log)
    def goto_prefs(self):
        self.wait_for_condition_true(self.verify_prefs_view,
                                             lambda: "prefs view not present", timeout=60)

    @Trace(log)
    def verify_prefs_view(self):
        self.click_element_by_key('PrefsButton')
        return prefs_view.verify_view()

    @Trace(log)
    def verify_active_tab(self):
        # for use with wait_for_condition_true
        # click the tab expected to become active
        # after a few seconds, test to see if it has become the active tab by looking at its color
        # if it is active, return true
        # if another tab is active, return false
        # if no tab is active, raise an exception
        self.click_element_by_key(self.expected_tab)
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
    def incoming_call_screen_test(self):
        from ePhone7.utils.get_softphone import get_softphone
        softphone = get_softphone()
        src_cfg = cfg.site['Users'][cfg.site['DefaultSoftphoneUser']]
        dst_cfg = cfg.site['Users']['R2d2User']
        dst_uri = 'sip:' + dst_cfg['UserId'] + '@' + dst_cfg['DomainName']
        softphone.make_call(dst_uri)
        softphone.wait_for_call_status('early', self.call_status_wait)
        self.find_element_by_key('IncomingCallAnswerToHeadset')
        self.find_element_by_key('IncomingCallAnswerToSpeaker')
        self.wait_for_element_text_by_key('IncomingCallCallerName', src_cfg['UserNameIncoming'])
        self.wait_for_element_text_by_key('IncomingCallCallerNumber', src_cfg['UserId'])
        softphone.end_call()

    @Trace(log)
    def answer_call_test(self):
        from ePhone7.utils.get_softphone import get_softphone
        softphone = get_softphone()
        dst_cfg = cfg.site['Users']['R2d2User']
        dst_uri = 'sip:' + dst_cfg['UserId'] + '@' + dst_cfg['DomainName']
        softphone.make_call(dst_uri)
        softphone.wait_for_call_status('early', self.call_status_wait)
        self.click_element_by_key('IncomingCallAnswerToSpeaker')
        softphone.wait_for_call_status('call', self.call_status_wait)
        self.click_element_by_key('EndActiveCall')
        softphone.wait_for_call_status('idle', self.call_status_wait)

    @Trace(log)
    def auto_answer_call_test(self):
        from ePhone7.utils.get_softphone import get_softphone
        softphone = get_softphone()
        dst_cfg = cfg.site['Users']['R2d2User']
        dst_uri = 'sip:' + dst_cfg['UserId'] + '@' + dst_cfg['DomainName']
        softphone.make_call(dst_uri)
        softphone.wait_for_call_status('call', self.call_status_wait)
        self.click_element_by_key('EndActiveCall')
        softphone.wait_for_call_status('idle', self.call_status_wait)

    @Trace(log)
    def ignore_call_test(self):
        from ePhone7.utils.get_softphone import get_softphone
        softphone = get_softphone()
        dst_cfg = cfg.site['Users']['R2d2User']
        dst_uri = 'sip:' + dst_cfg['UserId'] + '@' + dst_cfg['DomainName']
        softphone.make_call(dst_uri)
        softphone.wait_for_call_status('early', self.call_status_wait)
        self.click_element_by_key('IncomingCallIgnore')
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
