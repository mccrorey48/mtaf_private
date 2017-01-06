import unittest
from time import time, sleep

import lib.logging_esi as logging
from lib.wrappers import Trace
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from lib.user_exception import UserException as Ux

log = logging.get_logger('esi.selenium_actions')


# get access to test case assert methods
class Tc(unittest.TestCase):
    def runTest(self):
        pass


class SeleniumActions(Tc):

    cfg = None
    driver = None

    def __init__(self):
        Tc.__init__(self)

    def get_locator(self, name):
        cls = self.__class__
        while True:
            if not hasattr(cls, 'locators'):
                return None
            if name in cls.locators:
                return cls.locators[name]
            cls = cls.__base__

    @Trace(log)
    def assert_element_text(self, elem, expected, elem_name='element'):
        # log.debug('%s text = %s should be %s' % (elem_name, elem.text, expected))
        self.assertEqual(elem.text, expected, "Expect %s text '%s', got '%s'" % (elem_name, expected, elem.text))

    @Trace(log)
    def assert_element_text_ic(self, elem, expected, elem_name='element'):
        # log.debug('%s text = %s should be %s (ignore case)' % (elem_name, elem.text, expected))
        self.assertEqual(elem.text.upper(), expected.upper(), "Expect %s text '%s', got '%s' (ignoring case)" %
                         (elem_name, expected, elem.text))

    @Trace(log)
    def assert_elements_count(self, elems, expected_count, elem_name='elements'):
        # log.debug('%s count = %d should be %d' % (elem_name, len(elems), expected_count))
        self.assertEqual(len(elems), expected_count, "Expect %s length %d, got %d" %
                         (elem_name, expected_count, len(elems)))

    @Trace(log)
    def get_source(self):
        return self.driver.page_source

    @Trace(log)
    def click_element(self, elem):
        elem.click()

    @Trace(log)
    def click_element_by_key(self, key, seconds=60):
        locator = self.get_locator(key)
        elem = self.find_element_by_key(key)
        self.click_element(elem)
        # msg = ''
        # start_time = time()
        # while time() < start_time + seconds:
        #     try:
        #         elem = self.find_element_by_key(key)
        #     except WebDriverException as e:
        #         msg = "WebDriverException: %s" % e.message
        #         continue
        #     if "text" in locator:
        #         found_text = elem.text
        #         if found_text != locator["text"]:
        #             msg = "element text did not match, expected %s, found %s" % (locator["text"], found_text)
        #             continue
        #         # log.debug("found element with text = %s" % found_text)
        #     if elem.is_displayed() and elem.is_enabled():
        #         # log.debug("element found and clickable, clicking")
        #         self.click_element(elem)
        #     else:
        #         # log.debug("element found but is not clickable, waiting")
        #         continue
        #     break
        # else:
        #     raise Ux(msg)

    @Trace(log, log_level='debug')
    def find_element_by_locator(self, locator, timeout=10):
        # log.debug("%s = %s" % (locator['by'], locator['value']))
        return self.find_element_with_timeout(locator['by'], locator['value'], timeout=timeout)

    @Trace(log, log_level='debug')
    def find_elements_by_locator(self, locator):
        if locator['by'] == 'xpath':
            # log.debug("xpath = " + locator['value'])
            return self.driver.find_elements_by_xpath(locator['value'])
        if locator['by'] == 'id':
            # log.debug("id = " + locator['value'])
            return self.driver.find_elements_by_id(locator['value'])
        if locator['by'] == 'accessibility id':
            # log.debug("accessibility id = " + locator['value'])
            return self.driver.find_elements_by_accessibility_id(locator['value'])
        if locator['by'] == 'css selector':
            # log.debug("css selector = " + locator['value'])
            return self.driver.find_elements_by_css_selector(locator['value'])

    @Trace(log, log_level='debug')
    def find_sub_element_by_locator(self, parent, locator, timeout=10):
        if locator['by'] == 'xpath':
            # log.debug("xpath = " + locator['value'])
            return self.find_element_with_timeout('xpath', locator['value'], parent=parent, timeout=timeout)
        if locator['by'] == 'id':
            # log.debug("id = " + locator['value'])
            return self.find_element_with_timeout('id', locator['value'], parent=parent, timeout=timeout)

    @staticmethod
    @Trace(log, log_level='debug')
    def find_sub_elements_by_locator(parent, locator, timeout=20):
        if locator['by'] == 'xpath':
            # log.debug("xpath = " + locator['value'])
            return parent.find_elements_by_xpath(locator['value'])
        if locator['by'] == 'id':
            # log.debug("id = " + locator['value'])
            return parent.find_elements_by_id(locator['value'])
        if locator['by'] == 'css':
            # log.debug("css selector= " + locator['value'])
            return parent.find_elements_by_css_selector(locator['value'])

    @Trace(log)
    def find_element_by_key(self, key, timeout=30):
        locator = self.get_locator(key)
        try:
            if 'parent_key' in locator:
                parent = self.find_element_by_key(locator['parent_key'])
                return self.find_sub_element_by_locator(parent, locator, timeout)
            return self.find_element_by_locator(locator, timeout)
        except WebDriverException as e:
            raise Ux('WebDriverException ' + e.message)

    @Trace(log)
    def element_is_present(self, key, timeout=1):
        # waits 'timeout' seconds for exactly one element with the indicated key to be present
        # and returns True if that happens, False otherwise
        locator = self.get_locator(key)
        try:
            if 'parent_key' in locator:
                parent = self.find_element_by_key(locator['parent_key'])
                self.find_sub_element_by_locator(parent, locator, timeout)
            else:
                self.find_element_by_locator(locator, timeout)
        except Ux:
            return False
        except WebDriverException as e:
            raise Ux('WebDriverException ' + e.message)
        return True

    @Trace(log)
    def find_sub_element_by_key(self, parent, key, timeout=20):
        locator = self.get_locator(key)
        try:
            return self.find_sub_element_by_locator(parent, locator, timeout)
        except WebDriverException as e:
            raise Ux('WebDriverException ' + e.message)

    @Trace(log)
    def find_elements_by_key(self, key, filter_fn=None):
        locator = self.get_locator(key)
        try:
            if 'parent_key' in locator:
                parent = self.find_element_by_key(locator['parent_key'])
                elems = self.find_sub_elements_by_locator(parent, locator)
            else:
                elems = self.find_elements_by_locator(locator)
            if filter_fn is not None:
                return filter_fn(self, elems)
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
    def find_element_with_timeout(self, method, value, parent=None, timeout=10):
        # calls find_elements until exactly one element is returned, or times out and raises Ux exception
        start_time = time()
        while True:
            if parent:
                elems = parent.find_elements(method, value)
            else:
                elems = self.driver.find_elements(method, value)
            if len(elems) == 1:
                return elems[0]
            if time() - start_time > timeout:
                raise Ux("%s matching elements found with %s = %s, timeout = %s, parent = %s" %
                         (len(elems), method, value, timeout, parent))
