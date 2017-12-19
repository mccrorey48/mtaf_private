from time import time, sleep
import lib.logging_esi as logging
from lib.wrappers import Trace
from appium import webdriver
from appium.webdriver.common.touch_action import TouchAction
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from lib.user_exception import UserException as Ux
from time import strftime, localtime
from PIL import Image
import os
from pyand import ADB
import re
from urllib2 import URLError

log = logging.get_logger('esi.selenium_actions')

selenium_url = "http://localhost:4723/wd/hub"
desired_capabilities = {
    "nolaunch": {
        "appPackage": "com.esi_estech.ditto",
        "autoLaunch": False,
        "automationName": "Appium",
        "deviceName": "r2d2",
        "newCommandTimeout": 1200,
        "noReset": True,
        "platformName": "Android",
        "platformVersion": "4.4"
    },
    "main": {
        "appActivity": ".activities.MainViewActivity",
        "appPackage": "com.esi_estech.ditto",
        # "appWaitActivity": "activities.MainViewActivity",
        "appWaitPackage": "com.esi_estech.ditto",
        "automationName": "Appium",
        "deviceName": "r2d2",
        "dontStopAppOnReset": True,
        "newCommandTimeout": 1200,
        "noReset": True,
        "platformName": "Android",
        "platformVersion": "4.4"
    },
    "settings": {
        "appPackage": "com.esi_estech.ditto",
        "appium-version": "1.3.7",
        "autoLaunch": False,
        "deviceName": "r2d2",
        "newCommandTimeout": 1200,
        "platformName": "Android",
        "platformVersion": "4.4"
    }
}


class AndroidActions(object):
    driver = None
    cfg = None
    caps_tag = None

    def open_appium(self, caps_tag='nolaunch', caps_arg=None, connect_timeout=10):
        if caps_tag == 'query_device':
            adb = ADB()
            output = adb.run_cmd('shell dumpsys window windows')
            # print 'APK Version: ' + re.match('(?ms).*Packages:.*?versionName=(\d+\.\d+\.\d+)', output).group(1)
            package = re.match('(?ms).*mCurrentFocus=\S+\s+\S+\s+([^/]+)([^}]+)', output).group(1)
            activity = re.match('(?ms).*mCurrentFocus=\S+\s+\S+\s+([^/]+)/' + package + '([^}]+)', output).group(2)
            device_name = adb.run_cmd('shell getprop ro.product.model').strip()
            platform_version = adb.run_cmd('shell getprop ro.build.version.release').strip()
            caps = {
                    "appPackage": package,
                    "appActivity": activity,
                    "autoLaunch": False,
                    "automationName": "Appium",
                    "deviceName": device_name,
                    "newCommandTimeout": 1200,
                    "noReset": True,
                    "platformName": "Android",
                    "platformVersion": platform_version
                }
        elif caps_tag == 'caps_arg':
            caps = caps_arg
        else:
            if caps_tag not in desired_capabilities:
                raise Ux("unknown desired capabilities name %s" % caps_tag)
            caps = desired_capabilities[caps_tag]
        start_time = time()
        while time() - start_time < connect_timeout:
            try:
                AndroidActions.driver = webdriver.Remote(selenium_url, caps)
                self.caps_tag = caps_tag
                break
            except WebDriverException:
                log.info("retrying webdriver.Remote(%s, %s)" % (selenium_url, desired_capabilities[caps_tag]))
            except URLError as e:
                print "URLError attempting to connect to appium server: %s" % e
                raise Ux("URLError attempting to connect to appium server")
        else:
            raise Ux("failed to connect webdriver.Remote within %s seconds" % connect_timeout)

    @Trace(log)
    def close_appium(self):
        if self.driver is None:
            log.debug('appium is already closed')
        else:
            log.debug('closing appium')
            try:
                logcat = self.driver.get_log('logcat')
                timestamp = strftime('%m_%d_%y-%H_%M_%S', localtime())
                with open('log/e7_logcat_%s.log' % timestamp, 'w') as f:
                    for line in [item['message'] for item in logcat]:
                        f.write(line.encode('utf-8') + '\n')
                # self.driver.quit()
            except WebDriverException:
                log.debug("got WebDriverException, assuming appium already closed")
            AndroidActions.driver = None
            self.caps_tag = None

    class PresenceOfElementsByName(object):
        def __init__(self, name):
            self.name = name

        def __call__(self, actions):
            return actions.find_named_elements(self.name)

    @Trace(log)
    def get_element_color_and_count(self, screenshot_dir, filebase, elem, cropped_suffix='', color_list_index=1):
        im = Image.open(os.path.join(screenshot_dir, filebase + '.png'))
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
        cropped.save(os.path.join(screenshot_dir, 'cropped%s.png' % cropped_suffix))
        color_band = Image.new('RGBA', (crop_points[2] - crop_points[0], crop_points[3] - crop_points[1]), 'yellow')
        im.paste(color_band, crop_points, 0)
        im.save(os.path.join(screenshot_dir, filebase + '_after.png'))
        return self.get_image_color(cropped, color_list_index)

    @Trace(log)
    def get_image_color(self, image, color_list_index):
        colors = image.getcolors(1000000)
        # print "# of colors: %s" % len(colors)
        if len(colors) > color_list_index:
            current_color_and_count = sorted(colors, reverse=True, key=lambda x: x[0])[color_list_index]
            current_color = list(current_color_and_count[1])[:-1]
            current_count = current_color_and_count[0]
            return current_color + [current_count]
        else:
            return None

    @Trace(log)
    def get_cropped_color(self, img_path, crop_points):
        im = Image.open(img_path)
        cropped = im.crop(crop_points)
        (n, (r, g, b, depth)) = max(cropped.getcolors(1000), key=lambda x: x[0])
        return [r, g, b]

    def get_locator(self, name):
        cls = self.__class__
        while True:
            if not hasattr(cls, 'locators'):
                raise Ux("Unknown locator %s" % name)
            if name in cls.locators:
                return cls.locators[name]
            cls = cls.__base__

    @Trace(log)
    def get_source(self):
        return self.driver.page_source

    @Trace(log)
    def click_element(self, elem):
        elem.click()

    @Trace(log)
    def click_named_element(self, name):
        elem = self.find_named_element(name)
        text = elem.text
        x = int(elem.location['x'])
        y = int(elem.location['y'])
        w = int(elem.size['width'])
        h = int(elem.size['height'])
        xw = x + w
        yh = y + h
        xc = int(elem.location['x']) + (int(elem.size['width']) / 2)
        yc = int(elem.location['y']) + (int(elem.size['height']) / 2)
        log.debug("element attributes: text=%s, x=%s, w=%s, x+w=%s, xc=%s, y=%s, h=%s, y+h=%s, yc=%s" % (
            text, x, w, xw, xc, y, h, yh, yc))
        self.click_element(elem)

    @Trace(log, log_level='debug')
    def find_elements_by_locator(self, locator):
        elems = self.driver.find_elements(locator['by'], locator['value'])
        if 'text' in locator:
            return [elem for elem in elems if elem.text == locator['text']]
        else:
            return elems

    @Trace(log, log_level='debug')
    def find_sub_element_by_locator(self, parent, locator, timeout=10):
        elem = self.find_element_by_locator(locator, timeout=timeout, parent=parent)
        if elem is None:
            raise Ux("no unique matching element found with locator = %s" % locator)
        else:
            return elem

    @staticmethod
    @Trace(log, log_level='debug')
    def find_sub_elements_by_locator(parent, locator):
        elems = parent.find_elements(locator['by'], locator['value'])
        if 'text' in locator:
            return [elem for elem in elems if elem.text == locator['text']]
        else:
            return elems

    @Trace(log)
    def find_named_element(self, name, timeout=30):
        locator = self.get_locator(name)
        if 'parent_key' in locator:
            parent = self.find_named_element(locator['parent_key'])
            return self.find_sub_element_by_locator(parent, locator, timeout)
        elem = self.find_element_by_locator(locator, timeout)
        if elem is None:
            raise Ux("no unique matching element found with name = %s" % name)
        else:
            return elem

    @Trace(log)
    def keyevent(self, code):
        log.debug("sending keyevent(%s)" % code)
        self.driver.keyevent(code)

    @Trace(log)
    def hide_keyboard(self):
        self.driver.hide_keyboard()

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
    def swipe(self, origin_x, origin_y, destination_x, destination_y, duration_ms=500):
        self.driver.swipe(origin_x, origin_y, destination_x, destination_y, duration_ms)

    @Trace(log)
    def long_press_swipe(self, x1, y1, x2, y2, duration=500):
        TouchAction(self.driver).long_press(x=x1, y=y1, duration=duration).move_to(x=x2, y=y2).release().perform()

    @Trace(log)
    def tap(self, positions, duration=200):
        self.driver.tap(positions, duration)

    @Trace(log)
    def get_screenshot_as_file(self, filepath, scale=None):
        self.driver.get_screenshot_as_file(filepath)
        im = Image.open(filepath)
        if im.getbbox()[2] == 1024:
            log.debug("rotating screenshot -90 degrees")
            im = im.rotate(-90, expand=True)
        if scale is not None:
            bbox = im.getbbox()
            log.debug("im.getbbox() = %s" % repr(bbox))
            im.thumbnail((int(bbox[2] * scale), int(bbox[3] * scale)), Image.ANTIALIAS)
        log.debug("saving rotated screenshot to %s" % filepath)
        im.save(filepath)

    @Trace(log)
    def get_current_activity(self):
        return self.driver.current_activity

    @Trace(log)
    def wait_activity(self, activity, timeout):
        return self.driver.wait_activity(activity, timeout)

    @Trace(log)
    def element_is_present_by_locator(self, locator, timeout):
        return self.find_element_by_locator(locator, timeout) is not None

    @Trace(log)
    def element_is_present(self, name, timeout=10):
        locator = self.get_locator(name)
        return self.element_is_present_by_locator(locator, timeout)

    @Trace(log)
    def element_with_text_is_present(self, text, timeout=10):
        locator = {"by": "-android uiautomator", "value": 'new UiSelector().text("%s")' % text}
        return self.element_is_present_by_locator(locator, timeout)

    @Trace(log)
    def wait_for_no_elements_by_locator(self, locator, timeout):
        # waits 'timeout' seconds for zero elements with the indicated locator to be present
        # and returns True if that happens before timeout, False otherwise
        # Note:
        # - "not element_is_present()" is true when timeout expires before exactly one matching element is found;
        # - "element_becomes_not_present()" is true when zero matching elements are found before timeout expires
        start_time = time()
        poll_interval = 2
        while True:
            if 'parent_key' in locator:
                parent = self.find_named_element(locator['parent_key'])
                elems = self.find_sub_elements_by_locator(parent, locator)
            else:
                elems = self.find_elements_by_locator(locator)
            # if there are no elements found using "by" and "value", return True
            if len(elems) == 0:
                return True
            if time() - start_time > timeout:
                log.debug("timed out after %d seconds" % timeout)
                return False
            sleep(2)

    @Trace(log)
    def element_becomes_not_present(self, name, timeout=1):
        locator = self.get_locator(name)
        return self.wait_for_no_elements_by_locator(locator, timeout)

    @Trace(log)
    def element_with_text_is_not_present(self, text, timeout=1):
        locator = {"by": "-android uiautomator", "value": 'new UiSelector().text("%s")' % text}
        return self.wait_for_no_elements_by_locator(locator, timeout)

    @Trace(log)
    def find_named_sub_element(self, parent, name, timeout=20):
        locator = self.get_locator(name)
        try:
            return self.find_sub_element_by_locator(parent, locator, timeout)
        except WebDriverException as e:
            raise Ux('WebDriverException ' + e.message)

    @Trace(log)
    def find_named_elements(self, name, filter_fn=None):
        locator = self.get_locator(name)
        try:
            if 'parent_key' in locator:
                parent = self.find_named_element(locator['parent_key'])
                elems = self.find_sub_elements_by_locator(parent, locator)
            else:
                elems = self.find_elements_by_locator(locator)
            if filter_fn is None:
                return elems
            else:
                return filter(filter_fn, elems)
        except WebDriverException as e:
            raise Ux('WebDriverException ' + e.message)

    @Trace(log)
    def test_named_element_text(self, name, expected_text):
        try:
            self.actual_text = self.find_named_element(name, 10).text
        except Ux:
            self.actual_text = 'not found'
            return False
        return self.actual_text == expected_text

    @Trace(log)
    def wait_for_named_element_text(self, name, expected_text, seconds=30):
        start_time = time()
        while time() < start_time + seconds:
            if self.test_named_element_text(name, expected_text):
                return
            sleep(1.0)
        raise Ux('actual element text = "%s", expected "%s" after %d seconds' %
                 (self.actual_text, expected_text, seconds))

    @Trace(log)
    def wait_for_title(self, title, timeout=20):
        WebDriverWait(self.driver, timeout).until(EC.title_is(title))

    @staticmethod
    @Trace(log, log_level='debug')
    def wait_for_condition_true(condition_fn, failmsg_fn, timeout=30, poll_time=1.0, warn_time=5.0):
        start_time = time()
        while True:
            elapsed_time = time() - start_time
            if elapsed_time > timeout:
                raise Ux("%s after %.1f seconds" % (failmsg_fn(), elapsed_time))
            if elapsed_time > warn_time:
                log.warn("%s after %.1f seconds" % (failmsg_fn(), elapsed_time))
            if condition_fn():
                return True
            sleep(poll_time)

    @Trace(log, log_level='debug')
    def find_element_by_locator(self, locator, timeout=10, parent=None):
        # calls find_named_elements until exactly one element is returned, and returns that element
        # or times out and returns None
        if parent is None and "parent" in locator:
            parent = locator["parent"]
        start_time = time()
        elems = []
        while time() - start_time < timeout:
            if parent:
                elems = parent.find_elements(locator['by'], locator['value'])
            else:
                elems = self.driver.find_elements(locator['by'], locator['value'])
            if 'text' in locator:
                elems = [elem for elem in elems if elem.text == locator['text']]
            if len(elems) == 1:
                return elems[0]
        return None

android_actions = AndroidActions()
