import mtaf.mtaf_logging as logging

from eConsole.views.base_view import BaseView
from mtaf.trace import Trace

log = logging.get_logger('mtaf.auto_attn')


class AutoAttendantsView(BaseView):

    locators = {
    }

    def __init__(self):
        super(AutoAttendantsView, self).__init__()
        self.presence_element_names = ["eConsoleHelp"]
        self.nav_tab_names = ["HOME", "USERS", "CONFERENCES", "CALL QUEUES", "INVENTORY", "CALL HISTORY", "SETTINGS"]
        self.view_name = 'auto_attendants'

    @Trace(log)
    def goto_tab(self, tab_name, banner_title):
        self.click_named_element(tab_name)
        elem = self.find_named_element("NavBannerTitle")
        self.assert_equal(banner_title, elem.text,
                          "Expected banner title %s, got %s" % (banner_title, elem.text))


auto_attendants_view = AutoAttendantsView()
