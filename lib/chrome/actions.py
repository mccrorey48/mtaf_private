from selenium import webdriver
from lib.common.user_exception import UserException as Ux, UserFailException as Fx
import lib.common.logging_esi as logging
from lib.selenium.selenium_actions import SeleniumActions

log = logging.get_logger('esi.chrome_actions')


class Actions(SeleniumActions):

    def __init__(self, cfg, leaf_view=None):
        driver = webdriver.Remote(
            desired_capabilities=webdriver.DesiredCapabilities.CHROME,
            command_executor='http://localhost:4444/wd/hub')
        SeleniumActions.__init__(self, cfg, driver, leaf_view)
        self.leaf_view = leaf_view
        self.failureException = Fx


