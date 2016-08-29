from PIL import Image
import os
import unittest
from time import time, sleep, strftime, localtime

import lib.common.logging_esi as logging
from lib.common.configure import cfg
from lib.common.remote import remote
from lib.android.zpath import expand_zpath
from lib.common.wrappers import Trace
from selenium.common.exceptions import WebDriverException
from lib.common.user_exception import UserException as Ux, UserFailException as Fx

log = logging.get_logger('esi.action')
test_screenshot_folder = cfg.test_screenshot_folder
keycodes = {'KEYCODE_%d' % k: k + 7 for k in range(10)}


# get access to test case assert methods
class Tc(unittest.TestCase):
    def runTest(self):
        pass


class SeleniumActions(Tc):

    def __init__(self, leaf_view=None):
        Tc.__init__(self)
        self.leaf_view = leaf_view
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

    @Trace(log)
    def click_element_by_key(self, key, seconds=60):
        locator = cfg.get_locator(key, self.leaf_view)
        if "text" in locator:
            start_time = time()
            while time() < start_time + seconds:
                elem = self.find_element_by_key(key)
                found_text = elem.text
                if found_text == locator["text"]:
                    log.debug("found element with text = %s" % found_text)
                    elem.click()
                    return
            raise Ux('element text did not match, expected "%s", found "%s"' % (locator["text"], found_text))
        else:
            self.find_element_by_key(key).click()

    @staticmethod
    @Trace(log)
    def find_element_by_locator(locator, timeout=10):
        if locator['by'] == 'zpath':
            xpath = expand_zpath(locator['value'])
            log.debug("xpath = " + xpath)
            return remote.find_element_with_timeout("xpath", xpath, timeout=timeout)
        else:
            log.debug("%s = %s" % (locator['by'], locator['value']))
            return remote.find_element_with_timeout(locator['by'], locator['value'], timeout=timeout)

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
        if locator['by'] == 'accessibility id':
            log.debug("accessibility id = " + locator['value'])
            return remote.driver.find_elements_by_accessibility_id(locator['value'])

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
    def find_element_by_key(self, key, timeout=30):
        locator = cfg.get_locator(key, self.leaf_view)
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
        locator = cfg.get_locator(key, self.leaf_view)
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
        locator = cfg.get_locator(key, self.leaf_view)
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

    @Trace(log)
    def test_element_text_by_key(self, key, expected_text):
        try:
            self.actual_text = self.find_element_by_key(key, 10).text
        except Ux:
            self.actual_text = 'not found'
            return False
        return self.actual_text == expected_text

    @Trace(log)
    def wait_for_element_text_by_key(self, key, expected_text, seconds=30):
        start_time = time()
        while time() < start_time + seconds:
            if self.test_element_text_by_key(key, expected_text):
                return
            sleep(1.0)
        raise Ux('actual element text = "%s", expected "%s" after %d seconds' %
                 (self.actual_text, expected_text, seconds))

    @staticmethod
    @Trace(log)
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

