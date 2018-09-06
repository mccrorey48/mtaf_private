import mtaf.mtaf_logging as logging

from eConsole.views.base_view import BaseView
from mtaf.decorators import Trace

log = logging.get_logger('mtaf.manage_home')


class ManageHomeView(BaseView):

    locators = {
        "AutoAttendants": {"by": "link text", "value": "Auto Attendants"},
    }

    def __init__(self):
        super(ManageHomeView, self).__init__()
        self.presence_element_names = ["AutoAttendants"]
        self.nav_tab_names = ["HOME", "USERS", "CONFERENCES", "CALL QUEUES", "INVENTORY", "CALL HISTORY", "SETTINGS"]
        self.view_name = 'manage_home'

    @Trace(log)
    def goto_tab(self, tab_name, banner_title):
        self.click_named_element(tab_name)
        elem = self.find_named_element("NavBannerTitle")
        self.assert_equal(banner_title, elem.text,
                          "Expected banner title %s, got %s" % (banner_title, elem.text))


manage_home_view = ManageHomeView()
