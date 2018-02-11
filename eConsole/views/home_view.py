from time import sleep

import lib.logging_esi as logging

from eConsole.views.base_view import BaseView
from lib.wrappers import Trace

log = logging.get_logger('esi.home')


class HomeView(BaseView):

    locators = {
        "eConsoleHelp": {"by": "partial link text", "value": "eConsole Help"},
    }

    def __init__(self):
        super(HomeView, self).__init__()
        self.presence_element_names = ["eConsoleHelp"]
        self.banner_item_texts = []
        self.nav_tab_names = ["HOME", "MESSAGES", "CONTACTS", "PHONES", "CALL HISTORY", "SETTINGS"]

    @Trace(log)
    def goto_tab(self, tab_name, banner_title):
        self.click_named_element(tab_name)
        elem = self.find_named_element("NavBannerTitle")
        self.assert_element_text(elem, banner_title, "Banner Title")


home_view = HomeView()
