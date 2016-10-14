import lib.logging_esi as logging
import lib.filters as filters
from lib.wrappers import Trace
from selenium.webdriver import Chrome, Firefox
from selenium.webdriver.common.keys import Keys

from ccd.utils.configure import cfg
from lib.selenium_actions import SeleniumActions
from lib.user_exception import UserException as Ux, UserFailException as Fx
import re

log = logging.get_logger('esi.base_view')


class BaseView(SeleniumActions):

    locators = {
        "TestDomainMessage": {"by": "id", "value": "domain-message"},
        "TableRows": {"by": "xpath", "value": "//table/tbody/tr"},
        "RowDataSub": {"by": "xpath", "value": "td[column]"},
    }

    def __init__(self):
        self.cfg = cfg
        self.page_title = 'Page title not initialized'
        self.failureException = Fx
        self.keys = Keys
        self.current_browser = None
        self.log_file = None
        super(BaseView, self).__init__()

    @Trace(log)
    def find_table_rows_by_text(self, column, text, partial=False):
        match_rows = []
        rows = self.find_elements_by_key("TableRows")
        data_locator = self.get_locator("RowDataSub")
        data_locator["value"] = re.sub("column", "%s" % column, data_locator["value"])
        for row in rows:
            if partial:
                if text not in self.find_sub_element_by_locator(row, data_locator).text:
                    continue
            else:
                if text != self.find_sub_element_by_locator(row, data_locator).text:
                    continue
            match_rows.append(row)
        return match_rows

    def get_portal_url(self):
        self.get_url(cfg.site['PortalUrl'])

    @Trace(log)
    def wait_for_page_title(self):
        self.wait_for_title(self.page_title, timeout=15)

    @Trace(log)
    def test_domain_message_is_displayed(self):
        self.find_element_by_key("TestDomainMessage")

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
                SeleniumActions.driver = Chrome()
            elif browser.lower() == 'firefox':
                self.log_file = open('/home/mmccrorey/firefox.log', 'w')
                SeleniumActions.driver = Firefox()
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
base_view = BaseView()
