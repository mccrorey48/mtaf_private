import mtaf.mtaf_logging as logging

from eConsole.views.base_view import BaseView
from mtaf.decorators import Trace

log = logging.get_logger('mtaf.home')


class HomeView(BaseView):

    locators = {
        "eConsoleHelp": {"by": "link text", "value": "eConsole Help"},
    }

    def __init__(self):
        super(HomeView, self).__init__()
        self.presence_element_names = ["eConsoleHelp"]
        self.nav_tab_names = ["HOME", "MESSAGES", "CALL HISTORY", "CONTACTS", "PHONES", "SETTINGS"]
        self.view_name = 'home'

    @Trace(log)
    def goto_tab(self, tab_name, banner_title):
        self.click_named_element(tab_name)
        elem = self.find_named_element("NavBannerTitle")
        self.assert_equal(banner_title, elem.text,
                          "Expected banner title %s, got %s" % (banner_title, elem.text))


home_view = HomeView()
