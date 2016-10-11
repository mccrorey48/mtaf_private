from lib.common.user_exception import UserException as Ux, UserFailException as Fx
import lib.common.logging_esi as logging
from lib.selenium.selenium_actions import SeleniumActions
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.common.by import By

log = logging.get_logger('esi.chrome_actions')


class Actions(SeleniumActions):

    def __init__(self):
        super(Actions, self).__init__()
        self.failureException = Fx
        self.keys = Keys
        self.By = By
        self.current_browser = None
        self.log_file = None

    @staticmethod
    def get_url(url):
        if SeleniumActions.driver is None:
            raise Ux('remote is not open')
        log.debug('getting url %s' % url)
        SeleniumActions.driver.get(url)

    def filter_dropdown_and_click_result_by_link_text(self, input_key, filter_text, link_text):
        input_elem = self.find_element_by_key(input_key)
        input_elem.send_keys(filter_text)
        link_elem = self.find_element_with_timeout("partial link text", link_text, parent=input_elem.parent)
        link_elem.click()

    @staticmethod
    def send_key_to_element(elem, key):
        elem.send_keys(key)

    def open_browser(self, browser='chrome'):
        if self.current_browser is not None:
            log.debug('browser is already open')
        else:
            if browser.lower() == 'chrome':
                SeleniumActions.driver = webdriver.Chrome()
            elif browser.lower() == 'firefox':
                self.log_file = open('/home/mmccrorey/firefox.log', 'w')
                SeleniumActions.driver = webdriver.Firefox()
            else:
                raise Ux ('Unknown browser %s' % browser)
            self.current_browser = browser

    def close_browser(self):
        if self.current_browser is None:
            log.debug('browser is already closed')
        else:
            SeleniumActions.driver.quit()
            SeleniumActions.driver = None
            self.current_browser = None
            if self.log_file is not None:
                self.log_file.close()
