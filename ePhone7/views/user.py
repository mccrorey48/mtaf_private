from time import sleep
import lib.common.logging_esi as logging_esi
from ePhone7.utils.configure import cfg
from lib.android.actions import Actions
from lib.common.user_exception import UserException as Ux
from lib.common.wrappers import Trace
from ePhone7.views.base import BaseView
from ePhone7.views.prefs import prefs_view

log = logging_esi.get_logger('esi.user_view')


class UserView(BaseView):

    @Trace(log)
    def __init__(self):
        super(UserView, self).__init__()
        self.cfg = cfg
        self.tab_names = ('Contacts', 'History', 'Voicemail', 'Keypad')
        self.png_file_base = 'user'
        self.expected_tab = None
        self.active_tab = None
        self.call_status_wait = 30
        self.actions = Actions(self)

    # @Trace(log)
    # def logout(self):
    #     self.goto_prefs()
    #     prefs_view.logout()
    #     prefs_view.logout_confirm()
    #     self.actions.wait_for_condition_true(lambda: remote.current_activity == '.settings.ui.LoginActivity')

    @Trace(log)
    def set_dnd(self, on=True):
        if on:
            desired_color = cfg.colors['UserView']['dnd_on_color'][:-1]
        else:
            desired_color = cfg.colors['UserView']['dnd_off_color'][:-1]
        elem = self.actions.find_element_by_key('DndButton')
        self.actions.get_screenshot_as_png('set_dnd', cfg.test_screenshot_folder)
        current_color = self.actions.get_element_color('set_dnd', elem)
        if current_color != desired_color:
            self.actions.click_element(elem)
            sleep(5)
        self.actions.get_screenshot_as_png('set_dnd', cfg.test_screenshot_folder)
        current_color = self.actions.get_element_color('set_dnd', elem)
        if current_color != desired_color:
            raise Ux('unable to set dnd icon to desired color %s, current color is %s' % (desired_color, current_color))

    @Trace(log)
    def swipe_up(self):
        self.actions.swipe(300, 750, 300, 250, 1500)
        sleep(2)

    @Trace(log)
    def swipe_down(self):
        self.actions.swipe(300, 250, 300, 750, 750)
        sleep(2)

    @Trace(log)
    def swipe_elem_to_center(self, elem):
        old_y = elem.location['y']
        new_y = 512
        if abs(old_y - new_y) > (elem.size['height'] + 100):
            self.actions.swipe(300, old_y, 300, new_y, 750)
            sleep(2)

    @Trace(log)
    def end_call(self):
        self.actions.click_element_by_key('EndActiveCall')

    @Trace(log)
    def goto_settings(self):
        sleep(2.0)
        self.actions.swipe(515, 12, 515, 250, 400)
        self.actions.swipe(515, 12, 515, 250, 400)
        elem = self.actions.find_element_by_key('SettingsButtonText')
        self.actions.assert_element_text_ic(elem, 'settings', 'button')
        # Touch settings, settings menu appears with "Apps" item
        self.actions.tap_element(elem)

    @Trace(log)
    def goto_tab(self, tab_name):
        self.expected_tab = tab_name
        failmsg_fmt = 'expect active tab to be %s, got %s'
        self.actions.wait_for_condition_true(self.verify_active_tab,
                                             lambda: failmsg_fmt % (self.expected_tab, self.active_tab), timeout=120)

    @Trace(log)
    def goto_prefs(self):
        self.actions.wait_for_condition_true(self.verify_prefs_view,
                                             lambda: "prefs view not present", timeout=60)

    @Trace(log)
    def verify_prefs_view(self):
        self.actions.click_element_by_key('PrefsButton')
        return prefs_view.verify_view()

    @Trace(log)
    def verify_active_tab(self):
        # for use with wait_for_condition_true
        # click the tab expected to become active
        # after a few seconds, test to see if it has become the active tab by looking at its color
        # if it is active, return true
        # if another tab is active, return false
        # if no tab is active, raise an exception
        self.actions.click_element_by_key(self.expected_tab)
        sleep(5)
        self.actions.get_screenshot_as_png(self.png_file_base, cfg.test_screenshot_folder)
        self.active_tab = None
        for tab_name in self.tab_names:
            tab_color = self.actions.get_tab_color(self.png_file_base, tab_name)
            log.debug("get_tab_color(%s, %s) returned %s" % (self.png_file_base, tab_name, tab_color))
            if tab_color == 'active_color':
                self.active_tab = tab_name
                break
        return self.active_tab == self.expected_tab

    @Trace(log)
    def incoming_call_screen_test(self):
        from lib.softphone.softphone import get_softphone
        softphone = get_softphone()
        src_cfg = cfg.site['Accounts'][cfg.site['DefaultSoftphoneUser']]
        dst_cfg = cfg.site['Accounts']['R2d2User']
        dst_uri = 'sip:' + dst_cfg['UserId'] + '@' + dst_cfg['DomainName']
        softphone.make_call(dst_uri)
        softphone.wait_for_call_status('early', self.call_status_wait)
        self.actions.find_element_by_key('IncomingCallAnswerToHeadset')
        self.actions.find_element_by_key('IncomingCallAnswerToSpeaker')
        self.actions.wait_for_element_text_by_key('IncomingCallCallerName', src_cfg['UserNameIncoming'])
        self.actions.wait_for_element_text_by_key('IncomingCallCallerNumber', src_cfg['UserId'])
        softphone.teardown_call()

    @Trace(log)
    def answer_call_test(self):
        from lib.softphone.softphone import get_softphone
        softphone = get_softphone()
        dst_cfg = cfg.site['Accounts']['R2d2User']
        dst_uri = 'sip:' + dst_cfg['UserId'] + '@' + dst_cfg['DomainName']
        softphone.make_call(dst_uri)
        softphone.wait_for_call_status('early', self.call_status_wait)
        self.actions.click_element_by_key('IncomingCallAnswerToSpeaker')
        softphone.wait_for_call_status('start', self.call_status_wait)
        self.actions.click_element_by_key('EndActiveCall')
        softphone.wait_for_call_status('end', self.call_status_wait)

    @Trace(log)
    def auto_answer_call_test(self):
        from lib.softphone.softphone import get_softphone
        softphone = get_softphone()
        dst_cfg = cfg.site['Accounts']['R2d2User']
        dst_uri = 'sip:' + dst_cfg['UserId'] + '@' + dst_cfg['DomainName']
        softphone.make_call(dst_uri)
        softphone.wait_for_call_status('start', self.call_status_wait)
        self.actions.click_element_by_key('EndActiveCall')
        softphone.wait_for_call_status('end', self.call_status_wait)

    @Trace(log)
    def ignore_call_test(self):
        from lib.softphone.softphone import get_softphone
        softphone = get_softphone()
        dst_cfg = cfg.site['Accounts']['R2d2User']
        dst_uri = 'sip:' + dst_cfg['UserId'] + '@' + dst_cfg['DomainName']
        softphone.make_call(dst_uri)
        softphone.wait_for_call_status('early', self.call_status_wait)
        self.actions.click_element_by_key('IncomingCallIgnore')
        # the softphone caller will hear ringing until the max number of rings occurs, then
        # the softphone status will change to "start" because pbx accepts the invite to play
        # the "unavailable" message
        #
        # this is probably not how it is supposed to work...I think the caller should be sent to the
        # "unavailable" message immediately when "ignore call" is touched. In this case the
        # 40 second wait for call status is way too long
        wait_time = softphone.wait_for_call_status('start', 40)
        log.debug('got "start" status in %s seconds' % wait_time)
        softphone.set_monitor_on()
        sleep(10)
        # could insert a sleep here and do a fingerprint analysis of the recorded audio file
        softphone.set_monitor_off()
        softphone.teardown_call()


user_view = UserView()
