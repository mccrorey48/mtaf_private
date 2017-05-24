import unittest
from time import time, sleep
import lib.logging_esi as logging
from lib.wrappers import Trace
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from lib.user_exception import UserException as Ux
from filters import get_filter

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
    def click_named_element(self, name, seconds=60):
        locator = self.get_locator(name)
        elem = self.find_named_element(name)
        self.click_element(elem)

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
        return self.find_element_by_locator(locator, timeout=timeout, parent=parent)

    @staticmethod
    @Trace(log, log_level='debug')
    def find_sub_elements_by_locator(parent, locator):
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
    def find_named_element(self, name, timeout=30):
        locator = self.get_locator(name)
        try:
            if 'parent_key' in locator:
                parent = self.find_named_element(locator['parent_key'])
                return self.find_sub_element_by_locator(parent, locator, timeout)
            return self.find_element_by_locator(locator, timeout)
        except WebDriverException as e:
            raise Ux('WebDriverException ' + e.message)

    @Trace(log)
    def tap(self, positions, duration=200):
        self.driver.tap(positions, duration)

    @Trace(log)
    def element_is_present(self, name, timeout=10):
        # waits 'timeout' seconds for exactly one element with the indicated name to be present
        # and returns True if that happens, False otherwise
        # Note;
        # - "not element_is_present()" is true when timeout expires before exactly one matching element is found;
        # - "element_is_not_present()" is true when zero matching elements are found before timeout expires
        locator = self.get_locator(name)
        start_time = time()
        while time() - start_time < timeout:
            try:
                if 'parent_key' in locator:
                    parent = self.find_named_element(locator['parent_key'])
                    elems = self.find_sub_elements_by_locator(parent, locator)
                else:
                    elems = self.find_elements_by_locator(locator)
            except Ux:
                return False
            except WebDriverException as e:
                raise Ux('WebDriverException ' + e.message)
            if len(elems) == 1:
                return True
        return False

    @Trace(log)
    def element_is_not_present(self, name, timeout=1):
        # waits 'timeout' seconds for zero elements with the indicated name to be present
        # and returns True if that happens, False otherwise
        # Note:
        # - "not element_is_present()" is true when timeout expires before exactly one matching element is found;
        # - "element_is_not_present()" is true when zero matching elements are found before timeout expires
        locator = self.get_locator(name)
        start_time = time()
        while True:
            if 'parent_key' in locator:
                parent = self.find_named_element(locator['parent_key'])
                elems = self.find_sub_elements_by_locator(parent, locator)
            else:
                elems = self.find_elements_by_locator(locator)
            if len(elems) == 0:
                return True
            if 'text' in locator:
                if len(elems) == 1 and elems[0] != locator['text']:
                    return True
            if time() - start_time > timeout:
                return False

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
            if 'text' in locator:
                elems = get_filter('text_all', locator['text'])(elems)
            if filter_fn is not None:
                elems = filter_fn(self, elems)
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
        # calls find_named_elements until exactly one element is returned, or times out and raises Ux exception
        if parent is None and "parent" in locator:
            parent = locator["parent"]
        start_time = time()
        elems = []
        while time() - start_time < timeout:
            if parent:
                elems = parent.find_elements(locator['by'], locator['value'])
            else:
                elems = self.driver.find_elements(locator['by'], locator['value'])
            if "text" in locator:
                elems = [elem for elem in elems if elem.text.strip() == locator["text"]]
            if len(elems) == 1:
                return elems[0]
        else:
            raise Ux("%s matching elements found with locator = %s" % (len(elems), repr(locator)))
