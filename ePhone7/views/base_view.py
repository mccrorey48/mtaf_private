import os
from PIL import Image
from time import sleep, time

from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import WebDriverException

import lib.logging_esi as logging_esi
from ePhone7.config.configure import cfg
from lib.android import MockDriver
from lib.android import expand_zpath
from lib.selenium_actions import SeleniumActions
from lib.user_exception import UserException as Ux
from lib.wrappers import Trace

log = logging_esi.get_logger('esi.base_view')

keycodes = {'KEYCODE_%d' % k: k + 7 for k in range(10)}
keycodes['KEYCODE_HOME'] = 188
keycodes['KEYCODE_BACK'] = 4


class BaseView(SeleniumActions):

    current_activity = None
    caps_tag = None

    locators = {
        "ActiveCallScreen": {"by": "id", "value": "com.esi_estech.ditto:id/call_card_call_details"},
        "CallRecordButton": {"by": "id", "value": "com.esi_estech.ditto:id/recordButton"},
        "OtaServerOk": {"by": "id", "value": "com.esi_estech.ditto:id/confirm_button"},
        "CrashOkButton": {"by": "id", "value": "com.esi_estech.ditto:id/acra_crash_ok_button"},
        "CrashOkButton2": {"by": "id", "value": "android:id/button1", "text": "OK"},
        "E7HasStoppedOk": {"by": "id", "value": "android:id/button1"},
        "E7HasStoppedText": {"by": "id", "value": "android:id/message", "text": "Unfortunately, ePhone7 has stopped."},
        "NetworkErrorRetry": {"by": "id", "value": "com.esi_estech.ditto:id/e7AlertCancelButton"},
        "NetworkErrorText": {"by": "id", "value": "com.esi_estech.ditto:id/e7AlertDialogTitle", "text": "Network Error"},
        "RegRetryButton": {"by": "id", "value": "com.esi_estech.ditto:id/e7AlertCancelButton"},
        "ReleaseNotes": {"by": "id", "value": "com.esi_estech.ditto:id/release_notes"},
        "ReleaseNotesOK": {"by": "id", "value": "android:id/button1"}
    }

    def __init__(self):
        super(BaseView, self).__init__()
        self.cfg = cfg
        self.By = MobileBy

    def get_locator(self, name):
        locator = SeleniumActions.get_locator(self, name)
        if locator["by"] == "zpath":
            locator["by"] = "xpath"
            locator["value"] = expand_zpath(locator["value"])
        elif locator["by"] == "uiautomator":
            locator["by"] = "-android uiautomator"
            locator["value"] = "new UiSelector()." + locator["value"]
        return locator


    @Trace(log)
    def send_keycode(self, keycode):
        SeleniumActions.driver.keyevent(keycodes[keycode])

    @Trace(log)
    def send_keycode_back(self):
        self.send_keycode('KEYCODE_BACK')

    @Trace(log)
    def send_keycode_home(self):
        self.send_keycode('KEYCODE_HOME')

    @Trace(log)
    def send_keycode_number(self, number):
        if 0 <= number <= 9:
            self.send_keycode('KEYCODE_%d', number)
        else:
            raise Ux("%s is not a valid keycode number" % repr(number))

    @Trace(log)
    def hide_keyboard(self):
        SeleniumActions.driver.hide_keyboard()

    @Trace(log)
    def long_press(self, element=None, x=None, y=None, duration=1000):
        TouchAction(self.driver).long_press(element, x, y, duration).perform()

    @Trace(log)
    def long_press_scroll(self, origin_el, destination_el):
        TouchAction(self.driver).long_press(origin_el).move_to(destination_el).release().perform()

    @Trace(log)
    def short_press_scroll(self, origin_el, destination_el):
        TouchAction(self.driver).press(origin_el).move_to(destination_el).release().perform()

    @Trace(log)
    def swipe(self, origin_x, origin_y, destination_x, destination_y, duration):
        SeleniumActions.driver.swipe(origin_x, origin_y, destination_x, destination_y, duration)

    @Trace(log)
    def get_screenshot_as_png(self, filebase, screenshot_folder=None):
        if screenshot_folder is None:
            screenshot_folder = cfg.test_screenshot_folder
        sleep(5)
        fullpath = os.path.join(screenshot_folder, filebase + '.png')
        log.debug("saving screenshot to %s" % fullpath)
        SeleniumActions.driver.get_screenshot_as_file(fullpath)
        im = Image.open(fullpath)
        if im.getbbox()[2] == 1024:
            log.debug("rotating screenshot -90 degrees")
            im = im.rotate(-90, expand=True)
            log.debug("saving rotated screenshot to %s" % fullpath)
            im.save(fullpath)

    @staticmethod
    @Trace(log)
    def color_match(c1, c2, tolerance=5):
        for i in range(min(len(c1), len(c2))):
            if c2[i] > c1[i] + tolerance or c2[i] < c1[i] - tolerance:
                log.debug("color %s does not match %s" % (c1, c2))
                return False
        log.debug("color %s matches %s" % (c1, c2))
        return True

    @Trace(log)
    def get_tab_color(self, filebase, tab_name):
        # now = time()
        # timestamp = strftime('%H:%M:%S', localtime(now)) + '.%s' % int((now-int(now)) * 1000)
        # suffix = "%s_%s_%s.png" % (filebase, tab_name, timestamp)
        image_filename = os.path.join(self.cfg.test_screenshot_folder, filebase + '.png')
        log.debug('getting tab color from file %s' % image_filename)
        im = Image.open(image_filename)
        view_classname = self.__class__.__name__
        active_color = self.cfg.colors[view_classname]['active_color'][:-1]
        inactive_color = self.cfg.colors[view_classname]['inactive_color'][:-1]
        # print "active_color: " + repr(active_color)
        # print "inactive_color: " + repr(inactive_color)
        crop_points = tuple(self.cfg.colors[view_classname]['crop_points'][tab_name])
        log.debug("crop_points: %s" % repr(crop_points))
        cropped = im.crop(crop_points)
        # cropped.save(os.path.join(self.cfg.test_screenshot_folder, 'cropped_%s' % suffix))
        (n, (r, g, b, depth)) = max(cropped.getcolors(1000), key=lambda x: x[0])
        tab_color = [r, g, b]
        # color_band = Image.new('RGBA', (crop_points[2] - crop_points[0], crop_points[3] - crop_points[1]), 'yellow')
        # im.paste(color_band, crop_points, 0)
        # im.save(os.path.join(self.cfg.test_screenshot_folder, filebase + '_after_%s.png' % suffix))
        if self.color_match(tab_color, active_color):
            log.debug('tab_color is "active": %s' % repr(tab_color))
            return 'active_color'
        elif self.color_match(tab_color, inactive_color):
            log.debug('tab_color is "inactive": %s' % repr(tab_color))
            return 'inactive_color'
        else:
            exc_format = 'invalid color %s found for tab %s in view %s, active = %s, inactive = %s'
            raise Ux(exc_format % (repr(tab_color), tab_name, view_classname, repr(active_color), repr(inactive_color)))

    @Trace(log)
    def get_element_color(self, filebase, elem, cropped_suffix=''):
        return self.get_element_color_and_count(filebase, elem, cropped_suffix)[:3]

    def get_element_color_and_count(self, filebase, elem, cropped_suffix='', color_list_index=1):
        im = Image.open(os.path.join(self.cfg.test_screenshot_folder, filebase + '.png'))
        # calculate image crop points from element location['x'], location['y'], size['height'] and size['width']
        location = elem.location
        size = elem.size
        min_x = location['x']
        min_y = location['y']
        lim_x = min_x + size['width']
        lim_y = min_y + size['height']
        # print "min_x = %s, min_y = %s, lim_x = %s, lim_y = %s" % (min_x, min_y, lim_x, lim_y)
        # (x1, y1, x2, y2) = (min_y, 600-lim_x, lim_y, 600-min_x)
        (x1, y1, x2, y2) = (min_x, min_y, lim_x, lim_y)
        crop_points = [int(i) for i in (x1, y1, x2, y2)]
        # print "crop_points: " + repr(crop_points)
        cropped = im.crop(crop_points)
        cropped.save(os.path.join(self.cfg.test_screenshot_folder, 'cropped%s.png' % cropped_suffix))
        colors = cropped.getcolors(1000)
        color_band = Image.new('RGBA', (crop_points[2] - crop_points[0], crop_points[3] - crop_points[1]), 'yellow')
        im.paste(color_band, crop_points, 0)
        im.save(os.path.join(self.cfg.test_screenshot_folder, filebase + '_after.png'))
        current_color_and_count = sorted(colors, reverse=True, key=lambda x: x[0])[color_list_index]
        current_color = list(current_color_and_count[1])[:-1]
        current_count = current_color_and_count[0]
        return current_color + [current_count]

    @Trace(log)
    def tap_element(self, el, duration=200):
        center = (el.location['x'] + (el.size['width'] / 2), el.location['y'] + (el.size['height'] / 2))
        self.tap([center], duration)

    def update_remote(self, caps_tag, force=False, timeout=30):
        if force or caps_tag != self.caps_tag:
            start_time = time()
            while True:
                try:
                    driver = webdriver.Remote(cfg.site["SeleniumUrl"], cfg.caps[caps_tag])
                    break
                except WebDriverException:
                    if time() - start_time < timeout:
                        log.info("retrying webdriver.Remote(%s, %s)" % (cfg.site["SeleniumUrl"], cfg.caps[caps_tag]))
                    else:
                        raise Ux("timed out waiting to connect to webdriver")
            self.caps_tag = caps_tag
            driver.implicitly_wait(cfg.site['DefaultTimeout'])
            return driver

    @Trace(log)
    def open_appium(self, caps_tag='nolaunch', force=False, timeout=30):
        if cfg.site['Mock']:
            SeleniumActions.driver = MockDriver()
        else:
            log.debug('opening appium')
            try:
                SeleniumActions.driver = self.update_remote(caps_tag, force, timeout)
            except BaseException as e:
                raise Ux(str(e))

    @Trace(log)
    def close_appium(self):
        if SeleniumActions.driver is None:
            log.debug('appium is already closed')
        else:
            log.debug('closing appium')
            try:
                logcat = SeleniumActions.driver.get_log('logcat')
                with open('log/e7_logcat.log', 'w') as f:
                    for line in [item['message'] for item in logcat]:
                        f.write(line.encode('utf-8') + '\n')
                SeleniumActions.driver.quit()
            except WebDriverException:
                log.debug("got WebDriverException, assuming appium already closed")
            SeleniumActions.driver = None
            self.caps_tag = None

    @Trace(log)
    def startup(self, timeout=600):
        start_time = time()
        retrying_main = False
        tried_crash_ok = False
        tried_net_retry = False
        tried_reg_retry = False
        tried_e7_stopped = False
        tried_login = False
        tried_tnc = False
        tried_intro = False
        tried_ota = False
        while time() - start_time < timeout:
            try:
                current_activity = self.driver.current_activity
                log.debug("startup: current_activity = " + repr(current_activity))
                if current_activity == '.activities.MainViewActivity':
                    self.send_keycode_home()
                    break
                    # if retrying_main:
                    #     # get rid of the release notes screen if present
                    #     self.send_keycode_back()
                    #     break
                    # sleep(2)
                    # retrying_main = True
                elif current_activity == '.util.crashreporting.EPhoneCrashReportDialog':
                    if tried_crash_ok:
                        raise Ux("got activity .util.crashreporting.EPhoneCrashReportDialog twice")
                    # retrying_main = False
                    self.click_named_element('CrashOkButton')
                    tried_crash_ok = True
                    sleep(5)
                elif current_activity == '.activities.AutoLoginActivity':
                    # retrying_main = False
                    if self.element_is_present('NetworkErrorText'):
                        if tried_net_retry:
                            raise Ux("got Network Error Retry popup twice")
                        log.debug("startup: NetworkErrorText present")
                        self.click_named_element('NetworkErrorRetry')
                        tried_net_retry = True
                    elif self.element_is_present('E7HasStoppedText'):
                        if tried_e7_stopped:
                            raise Ux("got ePhone7 Stopped popup twice")
                        log.debug("startup: E7HasStoppedText present")
                        self.click_named_element('E7HasStoppedOk')
                        tried_e7_stopped = True
                    elif self.element_is_present('RegRetryButton'):
                        if tried_reg_retry:
                            raise Ux("got Registration Retry popup twice")
                        log.debug("startup: RegRetryButton present")
                        self.click_named_element('RegRetryButton')
                        tried_reg_retry = True
                elif current_activity == '.settings.ui.LoginActivity':
                    if tried_login:
                        raise Ux("got activity .settings.ui.LoginActivity twice")
                    from ePhone7.views import login_view
                    login_view.login()
                    tried_login = True
                elif current_activity == '.settings.ui.TermsAndConditionsScreen':
                    if tried_tnc:
                        raise Ux("got activity .settings.ui.TermsAndConditionsScreen twice")
                    from ePhone7.views import tnc_view
                    tnc_view.accept_tnc()
                    tried_tnc = True
                elif current_activity == '.OtaAppActivity':
                    if tried_ota:
                        raise Ux("got activity .OtaAppActivity twice")
                    self.send_keycode_back()
                    tried_ota = True
                elif current_activity == '.util.AppIntroActivity':
                    if tried_intro:
                        raise Ux("got activity .util.AppIntroActivity twice")
                    from ePhone7.views import app_intro_view
                    app_intro_view.skip_intro()
                    tried_intro = True
                else:
                    raise Ux('unexpected current_activity value: %s' % current_activity)
                sleep(5)
            except Ux as e:
                log.debug(e.msg)
                self.close_appium()
                self.open_appium()
        else:
            raise Ux('failed to restart ePhone7 within %d seconds' % timeout)

    @Trace(log)
    def wait_for_activity(self, activity, timeout=30):
        if not self.driver.wait_activity(activity, timeout):
            raise Ux('current activity is not %s' % activity)


base_view = BaseView()
