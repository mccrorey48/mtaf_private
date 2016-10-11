import Image
import os
import unittest
from time import time, sleep, strftime, localtime

import lib.common.logging_esi as logging
from common.helpers.configure import cfg
from common.helpers.remote import remote
from android.helpers.zpath import expand_zpath
from common.helpers.wrappers import Trace
from selenium.common.exceptions import WebDriverException
from common.helpers.user_exception import UserException as Ux, UserFailException as Fx

log = logging.get_logger('esi.action')
test_screenshot_folder = cfg.test_screenshot_folder


# get access to test case assert methods
class Tc(unittest.TestCase):
    def runTest(self):
        pass


class Actions(Tc):

    def __init__(self, view=None):
        Tc.__init__(self)
        self.view = view
        self.failureException = Fx

    @Trace(log)
    def assert_element_text(self, elem, expected, elem_name='element'):
        log.debug('%s text = %s should be %s' % (elem_name, elem.text, expected))
        self.assertEqual(elem.text, expected, "Expect %s text '%s', got '%s'" % (elem_name, expected, elem.text))

    @Trace(log)
    def assert_element_text_ic(self, elem, expected, elem_name='element'):
        log.debug('%s text = %s should be %s (ignore case)' % (elem_name, elem.text, expected))
        self.assertEqual(elem.text.upper(), expected.upper(), "Expect %s text '%s', got '%s' (ignoring case)" %
                         (elem_name, expected, elem.text))

    @Trace(log)
    def assert_elements_count(self, elems, expected_count, elem_name='elements'):
        log.debug('%s count = %d should be %d' % (elem_name, len(elems), expected_count))
        self.assertEqual(len(elems), expected_count, "Expect %s length %d, got %d" %
                         (elem_name, expected_count, len(elems)))

    @Trace(log)
    def assert_elements_count_less_equal(self, elems, maxcount, elem_name='elements'):
        log.debug('%s count = %d should be <= %d' % (elem_name, len(elems), maxcount))
        self.assertLessEqual(len(elems), maxcount, "Expect %s length <= %d, got %d" %
                             (elem_name, maxcount, len(elems)))

    @Trace(log)
    def assert_elements_count_greater_equal(self, elems, mincount, elem_name='elements'):
        log.debug('%s count = %d should be >= %d' % (elem_name, len(elems), mincount))
        self.assertGreaterEqual(len(elems), mincount, "Expect %s length >= %d, got %d" %
                                (elem_name, mincount, len(elems)))

    @staticmethod
    @Trace(log)
    def get_source():
        return remote.driver.page_source

    @staticmethod
    @Trace(log)
    def quit():
        remote.driver.quit()

    @staticmethod
    @Trace(log)
    def hide_keyboard():
        remote.driver.hide_keyboard()

    @staticmethod
    @Trace(log)
    def scroll(origin_el, destination_el):
        remote.driver.scroll(origin_el, destination_el)

    @staticmethod
    @Trace(log)
    def swipe(origin_x, origin_y, destination_x, destination_y, duration):
        remote.driver.swipe(origin_x, origin_y, destination_x, destination_y, duration)

    @staticmethod
    @Trace(log)
    def tap(x, y, duration=200):
        remote.driver.tap([(x, y)], duration)

    @staticmethod
    @Trace(log)
    def tap_element(el, duration=200):
        center = (el.location['x'] + (el.size['width'] / 2), el.location['y'] + (el.size['height'] / 2))
        remote.driver.tap([center], duration)

    @staticmethod
    @Trace(log)
    def click_element(el):
        el.click()

    @Trace(log)
    def click_element_by_key(self, key):
        self.find_element_by_key(key).click()

    @staticmethod
    @Trace(log)
    def find_element_by_locator(locator, timeout=10):
        if locator['by'] == 'zpath':
            xpath = expand_zpath(locator['value'])
            log.debug("xpath = " + xpath)
            return remote.find_element_with_timeout("xpath", xpath, timeout=timeout)
        if locator['by'] == 'xpath':
            log.debug("xpath = " + locator['value'])
            return remote.find_element_with_timeout("xpath", locator['value'], timeout=timeout)
        if locator['by'] == 'id':
            log.debug("id = " + locator['value'])
            return remote.find_element_with_timeout("id", locator['value'], timeout=timeout)

    @staticmethod
    @Trace(log)
    def find_elements_by_locator(locator):
        if locator['by'] == 'zpath':
            xpath = expand_zpath(locator['value'])
            log.debug("xpath = " + xpath)
            return remote.driver.find_elements_by_xpath(xpath)
        if locator['by'] == 'xpath':
            log.debug("xpath = " + locator['value'])
            return remote.driver.find_elements_by_xpath(locator['value'])
        if locator['by'] == 'id':
            log.debug("id = " + locator['value'])
            return remote.driver.find_elements_by_id(locator['value'])

    @staticmethod
    @Trace(log)
    def find_sub_element_by_locator(parent, locator, timeout=10):
        if locator['by'] == 'zpath':
            xpath = expand_zpath(locator['value'])
            log.debug("xpath = " + xpath)
            return remote.find_element_with_timeout('xpath', xpath, parent=parent, timeout=timeout)
        if locator['by'] == 'xpath':
            log.debug("xpath = " + locator['value'])
            return remote.find_element_with_timeout('xpath', locator['value'], parent=parent, timeout=timeout)
        if locator['by'] == 'id':
            log.debug("id = " + locator['value'])
            return remote.find_element_with_timeout('id', locator['value'], parent=parent, timeout=timeout)

    @staticmethod
    @Trace(log)
    def find_sub_elements_by_locator(parent, locator, timeout=20):
        if locator['by'] == 'zpath':
            xpath = expand_zpath(locator['value'])
            log.debug("xpath = " + xpath)
            return parent.find_elements_by_xpath(xpath)
        if locator['by'] == 'xpath':
            log.debug("xpath = " + locator['value'])
            return parent.find_elements_by_xpath(locator['value'])
        if locator['by'] == 'id':
            log.debug("id = " + locator['value'])
            return parent.find_elements_by_id(locator['value'])

    # key is a locator name
    @Trace(log)
    def find_element_by_key(self, key, timeout=20):
        locator = cfg.get_locator(key, self.view)
        try:
            if 'parent_key' in locator:
                parent = self.find_element_by_key(locator['parent_key'])
                return self.find_sub_element_by_locator(parent, locator, timeout)
            return self.find_element_by_locator(locator, timeout)
        except WebDriverException as e:
            raise Ux('WebDriverException ' + e.message)

    # "key" is the element whose locator is specified as a sub-element to
    # a parent key; in this case a specific parent element has been identified
    # from a list of candidates that match the parent key, and this element
    # is passed in as the "parent" argument
    @Trace(log)
    def find_sub_element_by_key(self, parent, key, timeout=20):
        locator = cfg.get_locator(key, self.view)
        try:
            return self.find_sub_element_by_locator(parent, locator, timeout)
        except WebDriverException as e:
            raise Ux('WebDriverException ' + e.message)

    # find all elements that match a locator named "key", put them in a list,
    # filter the list if filter_fn is not None
    #
    # filter_fn must take a list of elements and returns a filtered list of elements
    @Trace(log)
    def find_elements_by_key(self, key, filter_fn=None):
        locator = cfg.get_locator(key, self.view)
        try:
            if 'parent_key' in locator:
                parent = self.find_element_by_key(locator['parent_key'])
                elems = self.find_sub_elements_by_locator(parent, locator)
            else:
                elems = self.find_elements_by_locator(locator)
            if filter_fn is not None:
                return filter_fn(elems)
            else:
                return elems
        except WebDriverException as e:
            raise Ux('WebDriverException ' + e.message)

    @staticmethod
    @Trace(log)
    def wait_for_condition_true(condition_fn, seconds=30):
        start_time = time()
        while time() < start_time + seconds:
            if condition_fn():
                return True
            sleep(1.0)
        return False

    @staticmethod
    @Trace(log)
    def get_screenshot_as_png(filebase, screenshot_folder):
        sleep(5)
        fullpath = os.path.join(screenshot_folder, filebase + '.png')
        log.debug("saving %s" % fullpath)
        remote.driver.get_screenshot_as_file(fullpath)

    @staticmethod
    def color_match(c1, c2, tolerance=5):
        for i in range(3):
            if c2[i] > c1[i] + tolerance or c2[i] < c1[i] - tolerance:
                return False
        return True

    @Trace(log)
    def get_tab_color(self, filebase, tab_name):
        # now = time()
        # timestamp = strftime('%H:%M:%S', localtime(now)) + '.%s' % int((now-int(now)) * 1000)
        # suffix = "%s_%s_%s.png" % (filebase, tab_name, timestamp)
        image_filename = os.path.join(cfg.test_screenshot_folder, filebase + '.png')
        log.debug('getting tab color from file %s' % image_filename)
        im = Image.open(image_filename)
        view_classname = self.view.__class__.__name__
        active_color = cfg.colors[view_classname]['active_color'][:-1]
        inactive_color = cfg.colors[view_classname]['inactive_color'][:-1]
        # print "active_color: " + repr(active_color)
        # print "inactive_color: " + repr(inactive_color)
        crop_points = tuple(cfg.colors[view_classname]['crop_points'][tab_name])
        log.debug("crop_points: %s" % repr(crop_points))
        cropped = im.crop(crop_points)
        # cropped.save(os.path.join(cfg.test_screenshot_folder, 'cropped_%s' % suffix))
        (n, (r, g, b, depth)) = max(cropped.getcolors(1000), key=lambda x: x[0])
        tab_color = [r, g, b]
        # color_band = Image.new('RGBA', (crop_points[2] - crop_points[0], crop_points[3] - crop_points[1]), 'yellow')
        # im.paste(color_band, crop_points, 0)
        # im.save(os.path.join(cfg.test_screenshot_folder, filebase + '_after_%s.png' % suffix))
        if self.color_match(tab_color, active_color):
            log.debug('tab_color is "active": %s' % repr(tab_color))
            return 'active_color'
        elif self.color_match(tab_color, inactive_color):
            log.debug('tab_color is "inactive": %s' % repr(tab_color))
            return 'inactive_color'
        else:
            exc_format = 'invalid color %s found for tab %s in view %s, active = %s, inactive = %s'
            raise Ux(exc_format % (repr(tab_color), tab_name, view_classname, repr(active_color), repr(inactive_color)))

    @staticmethod
    @Trace(log)
    def get_element_color(filebase, elem, cropped_suffix=''):
        im = Image.open(os.path.join(cfg.test_screenshot_folder, filebase + '.png'))
        # calculate image crop points from element location['x'], location['y'], size['height'] and size['width']
        location = elem.location
        size = elem.size
        min_x = location['x']
        min_y = location['y']
        lim_x = min_x + size['width']
        lim_y = min_y + size['height']
        # print "min_x = %s, min_y = %s, lim_x = %s, lim_y = %s" % (min_x, min_y, lim_x, lim_y)
        (x1, y1, x2, y2) = (min_y, 600-lim_x, lim_y, 600-min_x)
        crop_points = (x1, y1, x2, y2)
        # print "crop_points: " + repr(crop_points)
        cropped = im.crop(crop_points)
        cropped.save(os.path.join(cfg.test_screenshot_folder, 'cropped%s.png' % cropped_suffix))
        colors = cropped.getcolors(1000)
        color_band = Image.new('RGBA', (crop_points[2] - crop_points[0], crop_points[3] - crop_points[1]), 'yellow')
        im.paste(color_band, crop_points, 0)
        im.save(os.path.join(cfg.test_screenshot_folder, filebase + '_after.png'))
        current_color = list(sorted(colors, reverse=True, key=lambda x: x[0])[1][1])[:-1]
        return current_color

