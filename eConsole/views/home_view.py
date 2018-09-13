import mtaf.mtaf_logging as logging

from eConsole.views.logged_in_view import LoggedInView
from mtaf.decorators import Trace

log = logging.get_logger('mtaf.home')


class HomeView(LoggedInView):

    locators = {
        "eConsoleHelp": {"by": "link text", "value": "eConsole Help"},
        "QuickLinks": {"by": "css selector", "value": "div[class='card-header']", "text": "Quick Links"},
        "RecentCallActivity": {"by": "css selector", "value": "div[class='card-header']", "text": "Recent Call Activity"},
    }

    def __init__(self):
        super(HomeView, self).__init__()
        self.presence_element_names = ["eConsoleHelp"]
        self.content_scopes.update({
            "eConsoleHelp": self.all_scopes,
            "RecentCallActivity": self.all_scopes,
            "QuickLinks": self.all_scopes,
        })
        self.nav_tab_names = ["HOME", "MESSAGES", "CALL HISTORY", "CONTACTS", "PHONES", "SETTINGS"]
        self.view_name = 'home'

    @Trace(log)
    def goto_tab(self, tab_name, banner_title):
        self.click_named_element(tab_name)
        elem = self.find_named_element("NavBannerTitle")
        self.assert_equal(banner_title, elem.text,
                          "Expected banner title %s, got %s" % (banner_title, elem.text))


home_view = HomeView()
