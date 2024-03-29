import os
import lib.logging_esi as logging
from lib.wrappers import Trace
from selenium.webdriver import Chrome, Firefox
from eConsole.config.configure import cfg
from lib.angular_actions import AngularActions
from lib.user_exception import UserException as Ux
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, TimeoutException
from PIL import Image

log = logging.get_logger('esi.base_view')


class BaseView(AngularActions):

    locators = {
        "ShowContacts": {"by": "id", "value": "showContacts"},
        "Banner": {"by": "class name", "value": "esi-header"},
        "BannerText": {"by": "class name", "value": "esi-header-text"},
        "Logout": {"by": "id", "value": "logout"},
        "NavTabs": {"by": "css selector", "value": ".navbar-nav .nav-item"},
        "HomeTab": {"by": "css selector", "value": ".navbar-nav .nav-item:nth-child(1)"},
        "MessagesTab": {"by": "css selector", "value": ".navbar-nav .nav-item:nth-child(2)"},
        "CallHistoryTab": {"by": "css selector", "value": ".navbar-nav .nav-item:nth-child(3)"},
        "ContactsTab": {"by": "css selector", "value": ".navbar-nav .nav-item:nth-child(4)"},
        "PhonesTab": {"by": "css selector", "value": ".navbar-nav .nav-item:nth-child(5)"},
        "SettingsTab": {"by": "css selector", "value": ".navbar-nav .nav-item:nth-child(6)"},
        "MainButton": {"by": "id", "value": "mainButton"},
        "LoadingGif": {"by": "class name", "value": "loadingoverlay"},
        "MessageSettings": {"by": "css selector", "value": ".dropdown-item.ng-scope", "text": "Message Settings"}
    }

    def __init__(self):
        self.cfg = cfg
        self.page_title = 'ESI'
        self.current_browser = None
        self.log_file = None
        self.presence_element_names = ["ShowContacts"]
        self.nav_tab_names = []
        self.banner_texts = []
        super(BaseView, self).__init__()

    @Trace(log)
    def get_screenshot_as_png(self, filebase, screenshot_folder=None, scale=None):
        if screenshot_folder is None:
            screenshot_folder = cfg.site['screenshot_folder']
        try:
            os.mkdir(screenshot_folder)
        except OSError:
            pass
        fullpath = os.path.join(screenshot_folder, filebase + '.png')
        log.debug("saving screenshot to %s" % fullpath)
        self.driver.get_screenshot_as_file(fullpath)
        im = Image.open(fullpath)
        if im.getbbox()[2] == 1024:
            log.debug("rotating screenshot -90 degrees")
            im = im.rotate(-90, expand=True)
        if scale is not None:
            bbox = im.getbbox()
            log.debug("im.getbbox() = %s" % repr(bbox))
            im.thumbnail((int(bbox[2] * scale), int(bbox[3] * scale)), Image.ANTIALIAS)
        log.debug("saving rotated screenshot to %s" % fullpath)
        im.save(fullpath)
        return fullpath

    @Trace(log)
    def logout(self):
        self.click_named_element("MainButton")
        self.click_named_element("Logout")

    @Trace(log)
    def input_text(self, text, locator_name):
        log.debug('inputting text "%s" to element "%s"' % (text, locator_name))
        self.find_named_element(locator_name).send_keys(text)
        self.element_trigger_change(locator_name)

    @Trace(log)
    def click_named_element(self, name, timeout=5):
        elem = self.find_named_element(name)
        try:
            WebDriverWait(self.driver, timeout).until(lambda driver: self.element_is_clickable(elem))
        except TimeoutException:
            raise Ux("element named \"%s\" not clickable in %s seconds" % (name, timeout))
        log.debug('element "%s" is clickable' % name)
        try:
            elem.click()
        except WebDriverException as e:
            raise Ux("WebDriverException: %s" % e)
        self.wait_until_page_ready()

    @Trace(log)
    def element_is_clickable(self, elem):
        return elem.is_enabled() and elem.is_displayed()


    @Trace(log)
    def becomes_present(self):
        self.wait_until_angular_ready()
        if len(self.presence_element_names) == 0:
            raise Ux("becomes_present() not implemented here")
        for element_name in self.presence_element_names:
            if not self.element_is_present(element_name):
                return False
        if self.banner_texts:
            if not self.element_is_present("Banner"):
                return False
            elem = self.find_named_element("BannerText")
            texts = elem.text.split('/')
            for text in self.banner_texts:
                if texts.pop(0).strip() != text:
                    return False
        if len(self.nav_tab_names) > 0:
            locator = self.get_locator('NavTabs')
            driver_locator = (locator["by"], locator["value"])
            if len(WebDriverWait(self.driver, 5).until(EC.visibility_of_any_elements_located(driver_locator))) == 0:
                return False
        return True

    def get_portal_url(self):
        self.get_url(cfg.site['portal_url'])

    @staticmethod
    def get_url(url):
        if AngularActions.driver is None:
            raise Ux('remote is not open')
        log.debug('getting url %s' % url)
        AngularActions.driver.get(url)

    def open_browser(self, browser='chrome'):
        if self.current_browser is not None:
            log.debug('browser is already open')
        else:
            if browser.lower() == 'chrome':
                AngularActions.driver = Chrome()
            elif browser.lower() == 'firefox':
                self.log_file = open('/home/mmccrorey/firefox.log', 'w')
                AngularActions.driver = Firefox()
            else:
                raise Ux ('Unknown browser %s' % browser)
            AngularActions.driver.set_window_size(1280, 1024)
            self.current_browser = browser

    def close_browser(self):
        if self.current_browser is None:
            log.debug('browser is already closed')
        else:
            AngularActions.driver.quit()
            AngularActions.driver = None
            self.current_browser = None
            if self.log_file is not None:
                self.log_file.close()


base_view = BaseView()
