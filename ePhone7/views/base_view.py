from mtaf import mtaf_logging
from mtaf.android_zpath import expand_zpath
from mtaf.android_actions import AndroidActions
from mtaf.user_exception import UserException as Ux, UserTimeoutException as Tx, UserFailException as Fx
from mtaf.trace import Trace

from ePhone7.config.configure import cfg
from ePhone7.lib.utils.spud_serial import SpudSerial
from ePhone7.lib.utils.usb_enable import usb_enable

import os
from time import sleep, time
from appium.webdriver.common.mobileby import MobileBy
from selenium.common.exceptions import WebDriverException

log = mtaf_logging.get_logger('mtaf.base_view')

keycodes = {'KEYCODE_%d' % k: k + 7 for k in range(10)}
keycodes['KEYCODE_HOME'] = 188
keycodes['KEYCODE_BACK'] = 4


class BaseView(AndroidActions):

    current_activity = None
    caps_tag = None

    locators = {
        "ActiveCallScreen": {"by": "id", "value": "com.esi_estech.ditto:id/call_card_call_details"},
        "OtaServerOk": {"by": "id", "value": "com.esi_estech.ditto:id/confirm_button"},
        "CrashOkButton": {"by": "id", "value": "com.esi_estech.ditto:id/acra_crash_ok_btn"},
        "CrashOkButton2": {"by": "id", "value": "android:id/button1", "text": "OK"},
        "E7HasStoppedOk": {"by": "id", "value": "android:id/button1"},
        "E7HasStoppedText": {"by": "id", "value": "android:id/message", "text": "Unfortunately, ePhone7 has stopped."},
        "RegRetryButton": {"by": "id", "value": "com.esi_estech.ditto:id/e7AlertCancelButton"},
        "ReleaseNotes": {"by": "id", "value": "com.esi_estech.ditto:id/release_notes"},
        "ReleaseNotesOK": {"by": "id", "value": "android:id/button1"},
        "RootFrameLayout": {"by": "zpath", "value": "/h/fl"}
    }

    def __init__(self):
        super(AndroidActions, self).__init__()
        self.cfg = cfg
        self.By = MobileBy
        self.locator_timeout = 10
        self.presence_element_names = []

    @Trace(log)
    def becomes_present(self):
        if len(self.presence_element_names) == 0:
            raise Ux("becomes_present() not implemented here")
        for element_name in self.presence_element_names:
            if not self[element_name]:
                return False
        return True

    @Trace(log)
    def becomes_not_present(self):
        if len(self.presence_element_names) == 0:
            raise Ux("becomes_not_present() not implemented here")
        for element_name in self.presence_element_names:
            if not self.missing[element_name]:
                return False
        return True

    @Trace(log)
    def get_locator(self, name):
        locator = AndroidActions.get_locator(self, name)
        if locator["by"] == "zpath":
            locator["by"] = "xpath"
            locator["value"] = expand_zpath(locator["value"])
        elif locator["by"] == "uia_text":
            locator["by"] = "-android uiautomator"
            locator["value"] = 'new UiSelector().text("%s")' % locator["value"]
        return locator

    @Trace(log)
    def send_keycode(self, keycode):
        log.debug("sending keyevent(%s)" % keycodes[keycode])
        self.keyevent(keycodes[keycode])

    @Trace(log)
    def send_keycode_back(self):
        self.send_keycode('KEYCODE_BACK')

    @Trace(log)
    def send_keycode_home(self):
        self.send_keycode('KEYCODE_HOME')

    @Trace(log)
    def send_keycode_number(self, number):
        if 0 <= number <= 9:
            self.send_keycode('KEYCODE_%d' % number)
        else:
            raise Ux("%s is not a valid keycode number" % repr(number))

    def touch_element_with_text(self, text, timeout=5):
        locator = {
            "by": "-android uiautomator",
            "value": "new UiSelector().text(\"%s\")" % text
        }
        elem = self.find_element_by_locator(locator, timeout)
        if elem is None:
            raise Ux("no unique matching element found with text = %s" % text)
        else:
            elem.click()

    @Trace(log)
    def swipe_named_element(self, name, direction):
        if direction not in ['left', 'right']:
            raise Ux('unknown direction %s' % direction)
        el = self.find_named_element(name)
        left_x = el.location["x"]
        right_x = left_x + el.size["width"] - 1
        y = el.location["y"] + (el.size["height"]/2)
        if direction == 'left':
            self.swipe(right_x, y, left_x, y, 1000)
        else:
            self.swipe(left_x, y, right_x, y, 1000)

    @Trace(log)
    def get_screenshot_as_png(self, filebase, screenshot_folder=None, scale=None):
        if screenshot_folder is None:
            screenshot_folder = cfg.site.ScreenshotFolder
        img_path = os.path.join(screenshot_folder, filebase + '.png')
        log.debug("saving screenshot to %s" % img_path)
        self.get_screenshot_as_file(img_path, scale)
        return img_path

    @staticmethod
    @Trace(log)
    def color_match(c1, c2, tolerance=5):
        for i in range(min(len(c1), len(c2))):
            if c2[i] > c1[i] + tolerance or c2[i] < c1[i] - tolerance:
                log.debug("color %s does not match %s" % (c1, c2))
                return False
        log.debug("color %s matches %s" % (c1, c2))
        return True

    @staticmethod
    @Trace(log)
    def color_is(c, color_name):
        # normalize the colors to the range 0-255
        cmax = max(c[:3])
        scale = 255.0 / cmax
        [r, g, b] = [int(x * scale) for x in c[:3]]
        count = c[3]
        log.debug('normalized color %s'% ([r, g, b]))
        if color_name == 'white star':
            return min([r, g, b]) > 245 and 230 < count < 238
        elif color_name == 'yellow star':
            return r == 255 and 195 < g < 215 and b < 30 and 230 < count < 238
        return False

    @Trace(log)
    def get_element_color_and_count(self, filebase, elem, cropped_suffix='', color_list_index=1):
        return self.get_element_color_and_count_using_folder(cfg.site.ScreenshotFolder, filebase, elem, cropped_suffix,
                                                             color_list_index)

    @Trace(log)
    def tap_element(self, el, duration=200):
        center = (el.location['x'] + (el.size['width'] / 2), el.location['y'] + (el.size['height'] / 2))
        self.tap([center], duration)

    @Trace(log)
    def close_appium_until_reboot(self, timeout=600):
        self.close_appium()
        ss = SpudSerial(cfg.site['SerialDev'], pwd_check=False)
        try:
            ss.expect('', 'mtp_open', timeout=timeout, dead_air_timeout=240)
        finally:
            usb_enable()
            self.open_appium(connect_timeout=60)


    @Trace(log)
    def startup(self, timeout=600, allow_reg_retry=True, auto_login_timeout = 60):
        start_time = time()
        reg_retry_handled = False
        current_activity = None
        auto_login_start_time = None
        while time() - start_time < timeout:
            try:
                previous_activity = current_activity
                current_activity = self.get_current_activity()
                log.debug("startup: current_activity = " + repr(current_activity))
                if current_activity == '.activities.MainViewActivity':
                    # sleep(10)
                    self.send_keycode_back()
                    self.send_keycode_home()
                    break
                elif current_activity == '.util.crashreporting.EPhoneCrashReportDialog':
                    self.click_named_element('CrashOkButton')
                elif current_activity == '.activities.AutoLoginActivity':
                    if previous_activity == '.activities.AutoLoginActivity':
                        if time() - auto_login_start_time > auto_login_timeout:
                            raise Ux('AutoLoginActivity timeout %s exceeded' % auto_login_timeout)
                    else:
                        auto_login_start_time = time()
                    if self.element_with_text_is_present('Authentication in progress', timeout=1):
                        sleep(5)
                        continue
                    if self.element_with_text_is_present('Network Error', timeout=1):
                        log.debug('startup: element with text "Network Error" is present')
                        self.touch_element_with_text('Retry', timeout=1)
                        sleep(2)
                        if self.element_with_text_is_present('Network Error', timeout=1):
                            log.debug('Retrying touching the Retry button')
                            self.touch_element_with_text('Retry', timeout=1)
                        try:
                            self.close_appium_until_reboot(timeout=300)
                        except Tx:
                            pass
                    elif self.element_is_present('E7HasStoppedText', timeout=1):
                        log.debug("startup: E7HasStoppedText present")
                        self.click_named_element('E7HasStoppedOk')
                    elif self.element_is_present('RegRetryButton'):
                        if not allow_reg_retry:
                            reg_retry_handled = True
                        log.debug("startup: RegRetryButton present")
                        self.click_named_element('RegRetryButton')
                elif current_activity == '.settings.ui.LoginActivity':
                    # performing auto login and sync, just wait it out
                    continue
                else:
                    raise Ux('unexpected current_activity value: %s' % current_activity)
                sleep(1)
            except Ux as e:
                log.debug(e.msg)
                self.close_appium()
                self.open_appium()
            except WebDriverException as e:
                log.debug('WebDriverException: %s, closing appium until reboot detected' % e.message)
                self.close_appium_until_reboot()
        else:
            raise Ux('failed to restart ePhone7 within %d seconds' % timeout)
        if reg_retry_handled and not allow_reg_retry:
            raise Fx("register retry message was handled, allow_reg_retry is False")

    @Trace(log)
    def wait_for_activity(self, activity, timeout=30):
        if not self.wait_activity(activity, timeout):
            raise Ux('current activity is not %s' % activity)


base_view = BaseView()
