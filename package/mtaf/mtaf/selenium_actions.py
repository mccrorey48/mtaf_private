from time import time, sleep
import mtaf_logging
import os
from mtaf.decorators import Trace
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from user_exception import UserException as Ux, UserFailException as Fx
log = mtaf_logging.get_logger('mtaf.selenium_actions')


browsers = {
    'chrome': webdriver.Chrome,
    'firefox': webdriver.Firefox,
    'safari': webdriver.Safari,
    'ie': webdriver.Ie,
    'edge': webdriver.Edge,
    'opera': webdriver.Opera,
    'phantomjs': webdriver.PhantomJS
}

desired_capabilities = {
    'chrome': DesiredCapabilities.CHROME,
    'firefox': DesiredCapabilities.FIREFOX,
    'safari': DesiredCapabilities.SAFARI,
    'ie': DesiredCapabilities.INTERNETEXPLORER,
    'edge': DesiredCapabilities.EDGE,
    'opera': DesiredCapabilities.OPERA,
    'phantomjs': DesiredCapabilities.PHANTOMJS,
}

driver_type = 'browser'


class SeleniumActions(object):
    driver = None
    locator_timeout = 10
    element_filter = None
    service_log_path = None
    webdriver_log_path = None
    __instance = None

    def __init__(self):
        if SeleniumActions.__instance is None:
            SeleniumActions.__instance = self

    @staticmethod
    def get_instance():
        if SeleniumActions.__instance is None:
            SeleniumActions()
        return SeleniumActions.__instance

    @staticmethod
    def set_driver(driver):
        SeleniumActions.driver = driver

    @staticmethod
    def wait_until_page_ready():
        pass

    @staticmethod
    def get_driver():
        return SeleniumActions.driver

    class All(object):
        def __init__(self, view):
            self.view = view

        def __getitem__(self, item_name):
            return self.__getattr__(item_name)

        def __getattr__(self, attr_name):
            return self.view.find_named_elements(attr_name)

    class Missing(object):
        def __init__(self, view):
            self.view = view

        def __getitem__(self, item_name):
            return self.__getattr__(item_name)

        def __getattr__(self, attr_name):
            return self.view.element_becomes_not_present(attr_name, self.view.locator_timeout)

    def __getitem__(self, item_name):
        return self.__getattr__(item_name)

    def __getattr__(self, attr_name):
        if attr_name == 'all':
            return self.All(self)
        elif attr_name == 'missing':
            return self.Missing(self)
        try:
            elements = WebDriverWait(self, self.locator_timeout).until(
                self.PresenceOfElementsByName(attr_name))
        except TimeoutException:
            return None
        if len(elements) != 1:
            raise Ux("self.PresenceOfElementsByName(%s) returned %s elements" % (attr_name, len(elements)))
        return elements[0]

    def get_url(self, url):
        log.debug('getting url %s' % url)
        self.get_driver().get(url)

    def get_title(self):
        log.debug('getting page title')
        return self.get_driver().title

    def get_current_url(self,):
        log.debug('getting current_url')
        return self.get_driver().current_url

    @Trace(log)
    def open_browser(self, browser_name='chrome'):
        if self.get_driver() is not None:
            log.debug('browser is already open')
        else:
            browser_name = browser_name.lower()
            if browser_name in browsers.keys():
                if browser_name == 'chrome':
                    mtaf_log_dir = os.getenv('MTAF_LOG_DIR', './log')
                    self.service_log_path = os.path.join(mtaf_log_dir, 'service.log')
                    self.webdriver_log_path = os.path.join(mtaf_log_dir, 'webdriver.log')
                    self.set_driver(browsers[browser_name](service_log_path=self.service_log_path))
                else:
                    self.set_driver(browsers[browser_name]())
                self.get_driver().set_window_size(1280, 1024)
            else:
                raise Ux('Unknown browser %s' % browser_name)

    @Trace(log)
    def close_browser(self):
        if self.get_driver() is None:
            log.debug('browser is already closed')
        else:
            self.get_driver().quit()
            self.set_driver(None)
            if self.service_log_path is not None and self.webdriver_log_path is not None:
                self.process_log(self.service_log_path, self.webdriver_log_path)

    class PresenceOfElementsByName(object):
        def __init__(self, name):
            self.name = name

        def __call__(self, actions):
            return actions.find_named_elements(self.name)

    def get_locator(self, name):
        cls = self.__class__
        while True:
            if not hasattr(cls, 'locators'):
                raise Ux("Unknown locator %s" % name)
            if name in cls.locators:
                return cls.locators[name]
            cls = cls.__base__

    @staticmethod
    def assert_equal(a, b, msg=''):
        if msg == '':
            msg = "%s does not equal %s" % (a, b)
        if a != b:
            raise AssertionError(msg)

    @Trace(log)
    def get_source(self):
        return self.get_driver().page_source

    @Trace(log)
    def click_element(self, elem):
        elem.click()

    @Trace(log)
    def send_keys(self, elem, val):
        elem.send_keys(val)

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

    @Trace(log)
    def click_link_text(self, text):
        loc = {"by": "link text", "value": text}
        elem = self.find_element_by_locator(loc)
        self.click_element(elem)

    @Trace(log, log_level='debug')
    def find_elements_by_locator(self, locator):
        self.wait_until_page_ready()
        elems = self.get_driver().find_elements(locator['by'], locator['value'])
        if 'text' in locator:
            return [elem for elem in elems if elem.text == locator['text']]
        else:
            return elems

    @Trace(log, log_level='debug')
    def find_sub_element_by_locator(self, parent, locator, timeout=10):
        self.wait_until_page_ready()
        elem = self.find_element_by_locator(locator, timeout=timeout, parent=parent)
        if elem is None:
            raise Ux("no unique matching element found with locator = %s" % locator)
        else:
            return elem

    @Trace(log, log_level='debug')
    def find_sub_elements_by_locator(self, parent, locator):
        self.wait_until_page_ready()
        elems = parent.find_elements(locator['by'], locator['value'])
        if 'text' in locator:
            return [elem for elem in elems if elem.text == locator['text']]
        else:
            return elems

    @Trace(log)
    def find_named_element(self, name, timeout=30):
        self.wait_until_page_ready()
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
    def wait_for_no_elements_by_locator(self, locator, timeout, poll_interval=2):
        # waits 'timeout' seconds for zero elements with the indicated locator to be present
        # and returns True if that happens before timeout, False otherwise
        # Note:
        # - "not element_is_present()" is true when timeout expires before exactly one matching element is found;
        # - "element_becomes_not_present()" is true when zero matching elements are found before timeout expires
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
            sleep(poll_interval)

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
        self.wait_until_page_ready()
        locator = self.get_locator(name)
        try:
            return self.find_sub_element_by_locator(parent, locator, timeout)
        except WebDriverException as e:
            raise Ux('WebDriverException ' + e.message)

    @Trace(log)
    def find_named_elements(self, name, filter_fn=None):
        self.wait_until_page_ready()
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
    def wait_for_named_element_text(self, name, expected_text, seconds=30):
        start_time = time()
        while time() < start_time + seconds:
            try:
                elem = self.find_named_element(name, 10)
            except Ux as e:
                raise Ux("could not locate element named %s: %s" % (name, e))
            try:
                if elem.text == expected_text:
                    return
            except WebDriverException as e:
                raise Ux("could not get text of element named %s: %s", (name, e))

            sleep(1.0)
        else:
            raise Ux('actual element text = "%s", expected "%s" after %d seconds' %
                     (self.actual_text, expected_text, seconds))

    @Trace(log)
    def wait_for_title(self, title, timeout=20):
        WebDriverWait(self.get_driver(), timeout).until(EC.title_is(title))

    @staticmethod
    @Trace(log, log_level='debug')
    def wait_for_condition_true(condition_fn, failmsg_fn, timeout=30, poll_time=1.0, warn_time=5.0):
        start_time = time()
        while True:
            elapsed_time = time() - start_time
            if elapsed_time > timeout:
                raise Fx("%s after %.1f seconds" % (failmsg_fn(), elapsed_time))
            if elapsed_time > warn_time:
                log.warn("%s after %.1f seconds" % (failmsg_fn(), elapsed_time))
            if condition_fn():
                return True
            sleep(poll_time)

    @Trace(log, log_level='debug')
    def find_element_by_locator(self, locator, timeout=10, parent=None, displayed_only=True):
        # calls find_named_elements until exactly one element is returned, and returns that element
        # or times out and returns None
        self.wait_until_page_ready()
        if parent is None and "parent" in locator:
            parent = locator["parent"]
        start_time = time()
        elems = []
        while time() - start_time < timeout:
            if parent:
                elems = parent.find_elements(locator['by'], locator['value'])
            else:
                elems = self.get_driver().find_elements(locator['by'], locator['value'])
            if self.element_filter is not None:
                elems = filter(self.elem_filter, elems)
            if 'text' in locator:
                elems = [elem for elem in elems if elem.text == locator['text']]
            elif 'partial text' in locator:
                elems = [elem for elem in elems if elem.text.find(locator['partial text']) != -1]
            if displayed_only:
                elems = filter(lambda x: x.is_displayed(), elems)
            if len(elems) == 1:
                return elems[0]
        return None


selenium_actions = SeleniumActions.get_instance()
