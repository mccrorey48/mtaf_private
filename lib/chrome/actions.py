from lib.common.user_exception import UserException as Ux, UserFailException as Fx
import lib.common.logging_esi as logging
from lib.selenium.selenium_actions import SeleniumActions
from lib.chrome.remote import remote

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

    def get_url(self, url):
        if self.driver is None:
            raise Ux('remote is not open')
        if url == self.current_url:
            log.debug('current url is already %s' % url)
        else:
            log.debug('getting url %s' % url)
            remote.driver.get(url)
            self.current_url =  remote.driver.current_url

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

