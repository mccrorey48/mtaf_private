import unittest
from time import time, sleep
import lib.logging_esi as logging
from lib.wrappers import Trace
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from lib.user_exception import UserException as Ux
from lib.user_exception import UserTimeoutException as Tx

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
                raise Ux("Unknown locator %s" % name)
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
    def tap(self, positions, duration=200):
        self.driver.tap(positions, duration)

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
        # - "element_is_not_present()" is true when zero matching elements are found before timeout expires
        start_time = time()
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

    @Trace(log)
    def element_is_not_present(self, name, timeout=1):
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
            return elems
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

