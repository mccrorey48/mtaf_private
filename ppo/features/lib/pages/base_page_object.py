from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import *
import traceback
import time
from lib.user_exception import UserTimeoutException as Tx
import lib.logging_esi
log = lib.logging_esi.get_logger('ppo_base')


class BasePage(object):

    required_text = {}

    def __init__(self, browser, base_url='http://www.seleniumframework.com'):
        self.base_url = base_url
        self.browser = browser
        self.timeout = 30

    def find_element(self, *loc):
        return self.browser.find_element(*loc)

    def visit(self,url):
        self.browser.get(url)

    def hover(self,element):
            ActionChains(self.browser).move_to_element(element).perform()
            # I don't like this but hover is sensitive and needs some sleep time
            time.sleep(5)

    def __getattr__(self, attr_name):
        try:
            if attr_name in self.locator_dictionary.keys():
                locator = self.locator_dictionary[attr_name]
                try:
                    element = WebDriverWait(self.browser, self.timeout).until(EC.presence_of_element_located(locator))
                    try:
                        script = 'window.scrollTo(0,%s)' % element.location['y']
                        self.browser.execute_script(script)
                        element = WebDriverWait(self.browser, self.timeout).until(EC.visibility_of_element_located(locator))
                    except(TimeoutException, StaleElementReferenceException):
                        traceback.print_exc()
                    if attr_name in self.required_text:
                        WebDriverWait(self.browser, self.timeout).until(
                            EC.text_to_be_present_in_element(locator, self.required_text[attr_name]))
                    return self.find_element(*self.locator_dictionary[attr_name])
                except(TimeoutException, StaleElementReferenceException):
                    traceback.print_exc()
        except AttributeError:
            super(BasePage, self).__getattribute__("method_missing")(attr_name)

    @staticmethod
    def method_missing(what):
        print "No %s here!" % what