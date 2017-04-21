import os
from time import sleep, time
import lib.logging_esi as logging_esi
from PIL import Image
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import WebDriverException
from lib.wrappers import Trace
from lib.android import expand_zpath

from ePhone7.utils.configure import cfg
from lib.android import MockDriver
from lib.selenium_actions import SeleniumActions
from lib.user_exception import UserException as Ux
from pyand import ADB, Fastboot
from ePhone7.utils.spud_serial import SpudSerial

log = logging_esi.get_logger('esi.settings_view')

keycodes = {'KEYCODE_%d' % k: k + 7 for k in range(10)}
keycodes['KEYCODE_HOME'] = 3
keycodes['KEYCODE_BACK'] = 4


class BaseView(SeleniumActions):

    current_activity = None
    caps_tag = None

    locators = {
        "ActiveCallScreen": {"by": "id", "value": "com.esi_estech.ditto:id/call_card_call_details"},
        "AdvancedOptions": {"by": "zpath", "value": "//sp/rl/v[1]/fl/ll/fl/rv/tv[1]"},
        "AdvancedItems": {"by": "id", "value": "android:id/title"},
        "AdvancedCheckbox": {"by": "id", "value": "com.esi_estech.ditto:id/checkbox"},
        "CallRecordEnableText": {"by": "id", "value": "android:id/title", "text": "Call Record Enable"},
        "CallRecordEnableBox": {"by": "zpath", "value": "com.esi_estech.ditto:id/confirm_button"},
        "CallRecordButton": {"by": "id", "value": "com.esi_estech.ditto:id/recordButton"},
        "OtaServerOk": {"by": "id", "value": "com.esi_estech.ditto:id/confirm_button"},
        "OtaAddressOk": {"by": "id", "value": "android:id/button1"},
        "CrashOkButton": {"by": "id", "value": "com.esi_estech.ditto:id/acra_crash_ok_button"},
        "CrashOkButton2": {"by": "id", "value": "android:id/button1", "text": "OK"},
        "E7HasStoppedOk": {"by": "id", "value": "android:id/button1"},
        "E7HasStoppedText": {"by": "id", "value": "android:id/message", "text": "Unfortunately, ePhone7 has stopped."},
        "NetworkErrorRetry": {"by": "id", "value": "com.esi_estech.ditto:id/e7AlertCancelButton"},
        "NetworkErrorText": {"by": "id", "value": "com.esi_estech.ditto:id/e7AlertDialogTitle", "text": "Network Error"},
        "RegRetryButton": {"by": "id", "value": "com.esi_estech.ditto:id/e7AlertCancelButton"},
        "TestOtaAlertTitle": {"by": "id", "value": "com.esi_estech.ditto:id/alertTitle", "text": "Set OTA Server Address"},
        "TestOtaEditText": {"by": "id", "value": "android:id/edit"},
        "TestOtaServerUrlText": {"by": "id", "value": "android:id/title", "text": "Test OTA Server URL"}
    }

    def __init__(self):
        super(BaseView, self).__init__()
        self.cfg = cfg
        self.By = MobileBy

    def get_locator(self, name):
        locator = SeleniumActions.get_locator(self, name)
        if locator is not None and locator["by"] == "zpath":
            locator["by"] = "xpath"
            locator["value"] = expand_zpath(locator["value"])
        return locator


    @Trace(log)
    def send_keycode(self, keycode):
        SeleniumActions.driver.keyevent(keycodes[keycode])

    @Trace(log)
    def hide_keyboard(self):
        SeleniumActions.driver.hide_keyboard()

    @Trace(log)
    def scroll(self, origin_el, destination_el):
        # SeleniumActions.driver.scroll(origin_el, destination_el)
        TouchAction(self.driver).long_press(origin_el).move_to(destination_el).release().perform()

    @Trace(log)
    def swipe(self, origin_x, origin_y, destination_x, destination_y, duration):
        SeleniumActions.driver.swipe(origin_x, origin_y, destination_x, destination_y, duration)

    @Trace(log)
    def tap(self, x, y, duration=200):
        SeleniumActions.driver.tap([(x, y)], duration)

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
    def color_match(c1, c2, tolerance = 5):
        for i in range(3):
            if c2[i] > c1[i] + tolerance or c2[i] < c1[i] - tolerance:
                return False
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
            log.debug('tab_coloetr is "active": %s' % repr(tab_color))
            return 'active_color'
        elif self.color_match(tab_color, inactive_color):
            log.debug('tab_color is "inactive": %s' % repr(tab_color))
            return 'inactive_color'
        else:
            exc_format = 'invalid color %s found for tab %s in view %s, active = %s, inactive = %s'
            raise Ux(exc_format % (repr(tab_color), tab_name, view_classname, repr(active_color), repr(inactive_color)))

    @Trace(log)
    def get_element_color(self, filebase, elem, cropped_suffix=''):
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
        current_color = list(sorted(colors, reverse=True, key=lambda x: x[0])[1][1])[:-1]
        return current_color

    @Trace(log)
    def tap_element(self, el, duration=200):
        center = (el.location['x'] + (el.size['width'] / 2), el.location['y'] + (el.size['height'] / 2))
        SeleniumActions.driver.tap([center], duration)

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
            SeleniumActions.driver = self.update_remote(caps_tag, force, timeout)

    @Trace(log)
    def close_appium(self):
        if SeleniumActions.driver is None:
            log.debug('appium is already closed')
        else:
            log.debug('closing appium')
            logcat = SeleniumActions.driver.get_log('logcat')
            with open('log/e7_logcat.log', 'w') as f:
                for line in [item['message'] for item in logcat]:
                    f.write(line.encode('utf-8') + '\n')
            SeleniumActions.driver.quit()
            SeleniumActions.driver = None
            self.caps_tag = None

    @Trace(log)
    def force_aosp_downgrade(self):

        actions = [
            {'cmd': 'reboot\n', 'new_cwd': '', 'expect': 'Hit any key to stop autoboot:', 'timeout': 30},
            {'cmd': '\n', 'expect': '=> ', 'timeout': 5},
            {'cmd': 'mmc dev 2\n', 'expect': 'mmc2(part 0) is current device\n=> '},
            {'cmd': 'mmc setdsr 2\n', 'expect': 'set dsr OK, force rescan\n=> '},
            {'cmd': 'fastboot\n', 'expect': '0x4\nUSB_RESET\nUSB_PORT_CHANGE 0x4\n'}
        ]

        serial_dev = '/dev/ttyUSB0'
        ss = SpudSerial(serial_dev)
        for action in actions:
            (reply, elapsed) = ss.do_action(action)
            log.debug('[%5.3fs] cmd %s, expect %s, received %d chars' % (elapsed, repr(action['cmd']), repr(action['expect']), len(reply)))
            ss.connection.reset_input_buffer()
        fb = Fastboot()
        fb_cmds = [
            "flash boot ePhone7/aosps/2.1.3/boot.img",
            "flash system ePhone7/aosps/2.1.3/system.img",
            "flash recovery ePhone7/aosps/2.1.3/recovery.img",
            "reboot"
        ]
        for cmd in fb_cmds:
            log.debug(">>> fastboot " + cmd)
            log.debug(fb.run_cmd(cmd))

    @Trace(log)
    def force_app_downgrade(self):
        serial_dev = '/dev/ttyUSB0'
        ss = SpudSerial(serial_dev)
        adb = ADB()
        adb.run_cmd("install -r ePhone7/apks/10_0_9.apk")
        action = {'cmd': 'reboot\n', 'new_cwd': '', 'timeout': 30}
        (reply, elapsed) = ss.do_action(action)
        log.debug('[%5.3fs] cmd %s, expect %s, received %d chars' % (elapsed, repr(action['cmd']), repr(action['expect']), len(reply)))


    @Trace(log)
    def startup(self):
        self.open_appium('nolaunch', force=True, timeout=60)
        retry_main = False
        while True:
            try:
                current_activity = self.driver.current_activity
                log.debug("startup: current_activity = " + current_activity)
                if current_activity == '.activities.MainViewActivity':
                    if retry_main:
                        break
                    sleep(10)
                    retry_main = True
                elif current_activity == '.util.crashreporting.EPhoneCrashReportDialog':
                    retry_main = False
                    self.click_named_element('CrashOkButton')
                    sleep(5)
                elif current_activity == '.activities.AutoLoginActivity':
                    retry_main = False
                    if self.element_is_present('NetworkErrorText'):
                        log.debug("startup: NetworkErrorText present")
                        self.click_named_element('NetworkErrorRetry')
                    elif self.element_is_present('E7HasStoppedText'):
                        log.debug("startup: E7HasStoppedText present")
                        self.click_named_element('E7HasStoppedOk')
                    elif self.element_is_present('RegRetryButton'):
                        log.debug("startup: RegRetryButton present")
                        self.click_named_element('RegRetryButton')
                elif current_activity == '.settings.ui.LoginActivity':
                    from ePhone7.views import login_view
                    login_view.login()
                elif current_activity == '.settings.ui.TermsAndConditionsScreen':
                    from ePhone7.views import tnc_view
                    tnc_view.accept_tnc()
                elif current_activity == '.util.AppIntroActivity':
                    from ePhone7.views import app_intro_view
                    app_intro_view.skip_intro()
                else:
                    raise Ux('unexpected current_activity value: %s' % current_activity)
            except WebDriverException:
                log.debug("startup: got WebDriverException (ignoring)")
                sleep(5)

    @Trace(log)
    def shutdown(self):
        self.close_appium()

    @Trace(log)
    def wait_for_activity(self, activity, timeout=30):
        if not self.driver.wait_activity(activity, timeout):
            raise Ux('current activity is not %s' % activity)


base_view = BaseView()
