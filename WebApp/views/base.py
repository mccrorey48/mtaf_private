import lib.mtaf_logging as logging
from lib.trace import Trace
from lib.selenium_actions import SeleniumActions
from lib.user_exception import UserException as Ux, UserFailException as Fx

log = logging.get_logger('mtaf.base_view')


class BaseView(SeleniumActions):

    def __init__(self):
        self.page_title = 'Page title not initialized'
        super(BaseView, self).__init__()

    def get_locator(self, name):
        locator = SeleniumActions.get_short_locator(self, name)
        return locator

    @staticmethod
    def get_url(url):
        if SeleniumActions.driver is None:
            raise Ux('remote is not open')
        log.debug('getting url %s' % url)
        SeleniumActions.driver.get(url)

    @staticmethod
    def send_key_to_element(elem, key):
        elem.send_keys(key)

    @Trace(log)
    def wait_for_page_title(self):
        self.wait_for_title(self.page_title)


base_view = BaseView()
