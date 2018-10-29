import os
import mtaf.mtaf_logging as logging
from mtaf.decorators import Trace
from eConsole.config.configure import cfg
from mtaf.angular_actions import AngularActions
from mtaf.user_exception import UserException as Ux, UserFailException as Fx
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.common.exceptions import WebDriverException, TimeoutException
from PIL import Image

log = logging.get_logger('mtaf.base')


class BaseView(AngularActions):

    def __init__(self):
        super(BaseView, self).__init__()
        self.cfg = cfg
        self.page_title = 'ESI'
        self.log_file = None
        self.service_log_path = None
        self.webdriver_log_path = None
        self.presence_element_names = []
        self.all_scopes = ['select', 'premier', 'office_mgr']
        self.content_scopes = {}
        self.nav_tab_names = []
        self.banner_texts = []
        self.view_name = 'base'

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
        self.get_driver().get_screenshot_as_file(fullpath)
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
    def input_text(self, text, locator_name):
        log.debug('inputting text "%s" to element "%s"' % (text, locator_name))
        self.find_named_element(locator_name).send_keys(text)
        self.element_trigger_change()

    @Trace(log)
    def click_named_element(self, name, timeout=5):
        elem = self.find_named_element(name)
        try:
            WebDriverWait(self.get_driver(), timeout).until(lambda driver: self.element_is_clickable(elem))
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
            elem = self.find_named_element("Banner")
            texts = elem.text.split('/')
            for text in self.banner_texts:
                if texts.pop(0).strip() != text:
                    return False
        if len(self.nav_tab_names) > 0:
            locator = self.get_locator('NavTabs')
            driver_locator = (locator["by"], locator["value"])
            if len(WebDriverWait(self.get_driver(), 15).until(
                    expected_conditions.visibility_of_all_elements_located(driver_locator))) != len(self.nav_tab_names):
                return False
        return True

    @Trace(log)
    def has_scope_content(self, scope):
        self.wait_until_angular_ready()
        for element_name in self.content_scopes.keys():
            if scope not in self.content_scopes[element_name]:
                continue
            if not self.element_is_present(element_name):
                raise Fx('element "%s" not present' % element_name)


base_view = BaseView()
