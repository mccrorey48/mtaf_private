from lib.common.user_exception import UserFailException as Fx
import lib.common.logging_esi as logging
from lib.selenium.selenium_actions import SeleniumActions
from lib.chrome.remote import remote

log = logging.get_logger('esi.chrome_actions')


class Actions(SeleniumActions):

    driver = None

    def __init__(self, view=None):
        SeleniumActions.__init__(self, remote.driver, view)
        self.view = view
        self.failureException = Fx

    @staticmethod
    def closeDriver():
        remote.driver.close()

