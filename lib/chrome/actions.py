from lib.common.user_exception import UserException as Ux, UserFailException as Fx
import lib.common.logging_esi as logging
from lib.selenium.selenium_actions import SeleniumActions
from lib.chrome.remote import remote
from selenium.webdriver.common.keys import Keys

log = logging.get_logger('esi.chrome_actions')


class Actions(SeleniumActions):

    def __init__(self, view=None):
        if view is None:
            raise Ux('Actions instantiation must include view parameter')
        self.view = view
        super(Actions, self).__init__(remote)
        self.failureException = Fx
        self.driver = None
        self.current_url = None
        self.keys = Keys

    def get_url(self, url):
        if self.driver is None:
            raise Ux('remote is not open')
        if url == self.current_url:
            log.debug('current url is already %s' % url)
        else:
            log.debug('getting url %s' % url)
            remote.driver.get(url)
            self.current_url = remote.driver.current_url

    def filter_dropdown_and_click_result_by_link_text(self, input_key, filter_text, link_text):
        input_elem = self.find_element_by_key(input_key)
        input_elem.send_keys(filter_text)
        link_elem = self.find_element_with_timeout("partial link text", link_text, parent=input_elem.parent)
        link_elem.click()

    @staticmethod
    def send_key_to_element(elem, key):
        elem.send_keys(key)

    @staticmethod
    def get_title():
        return remote.driver.title

    def open_browser(self):
        remote.open()
        self.driver = remote.driver

    def close_browser(self):
        remote.close()
        self.driver = None
        self.current_url = None
