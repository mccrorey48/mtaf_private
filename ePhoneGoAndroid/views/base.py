import os
from time import sleep

from mtaf import mtaf_logging
from PIL import Image
from appium import webdriver
from appium.webdriver.common.mobileby import MobileBy
from lib.wrappers import Trace
from lib.android_zpath import expand_zpath

from ePhoneGoAndroid.config.configure import cfg
from lib.android_zpath import MockDriver
from lib.android_actions import SeleniumActions
from lib.user_exception import UserException as Ux

log =mtaf_logging.get_logger('mtaf.base_view')

keycodes = {'KEYCODE_%d' % k: k + 7 for k in range(10)}


class BaseView(SeleniumActions):

    current_activity = None
    caps_tag = None

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
    def hide_keyboard(self):
        SeleniumActions.driver.hide_keyboard()

    @Trace(log)
    def scroll(self, origin_el, destination_el):
        SeleniumActions.driver.scroll(origin_el, destination_el)

    @Trace(log)
    def swipe(self, origin_x, origin_y, destination_x, destination_y, duration):
        SeleniumActions.driver.swipe(origin_x, origin_y, destination_x, destination_y, duration)

    @Trace(log)
    def get_screenshot_as_png(self, filebase, screenshot_folder):
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
        self.tap([center], duration)

    def update_remote(self, caps_tag):
        if caps_tag != self.caps_tag:
            driver = webdriver.Remote(cfg.site["SeleniumUrl"], cfg.caps[caps_tag])
            self.caps_tag = caps_tag
            driver.implicitly_wait(cfg.site['DefaultTimeout'])
            return driver

    @Trace(log)
    def open_appium(self, caps_tag='nolaunch'):
        if cfg.site['Mock']:
            SeleniumActions.driver = MockDriver()
        else:
            log.debug('opening appium')
            SeleniumActions.driver = self.update_remote(caps_tag)
        pass

    @Trace(log)
    def close_appium(self):
        if SeleniumActions.driver is None:
            log.debug('appium is already closed')
        else:
            log.debug('closing appium')
            SeleniumActions.driver.quit()
            SeleniumActions.driver = None
            self.caps_tag = None
        pass

    @Trace(log)
    def wait_for_activity(self, activity, timeout=30):
        if not self.driver.wait_activity(activity, timeout):
            raise Ux('current activity is not %s' % activity)

base_view = BaseView()
