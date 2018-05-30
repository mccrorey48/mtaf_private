from mtaf.user_exception import UserException as Ux
import mtaf.mtaf_logging as logging

from eConsole.views.base_view import BaseView
from mtaf.trace import Trace

log = logging.get_logger('mtaf.home')


class HomeView(BaseView):

    locators = {
        "eConsoleHelp": {"by": "partial link text", "value": "eConsole Help"},
    }

    def __init__(self):
        super(HomeView, self).__init__()
        self.presence_element_names = ["eConsoleHelp"]
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]

    @Trace(log)
    def goto_tab(self, tab_name, banner_title):
        self.click_named_element(tab_name)
        elem = self.find_named_element("NavBannerTitle")
        self.assert_equal(banner_title, elem.text,
                          "Expected banner title %s, got %s" % (banner_title, elem.text))


home_view = HomeView()
