import lib.common.logging_esi as logging
from lib.common.wrappers import Trace
from ccd.views.base import BaseView
from time import sleep

log = logging.get_logger('esi.domain_view')


class DomainView(BaseView):

    @Trace(log)
    def __init__(self):
        super(DomainView, self).__init__()
        self.view_name = "domain"
        self.page_title = "Manager Portal - Home"

    @Trace(log)
    def goto_tab(self, tab_name, banner_title):
        self.actions.click_element_by_key(tab_name)
        elem = self.actions.find_element_by_key("NavBannerTitle")
        self.actions.assert_element_text(elem, banner_title, "Banner Title")

    @Trace(log)
    def goto_home(self):
        self.goto_tab('HomeTab', 'Home')

    @Trace(log)
    def goto_users(self):
        self.goto_tab('UsersTab', 'Users')

    @Trace(log)
    def goto_conferences(self):
        self.goto_tab('ConferencesTab', 'Conferences')

    @Trace(log)
    def goto_call_queues(self):
        self.goto_tab('CallQueuesTab', 'Call Queues')

    @Trace(log)
    def goto_inventory(self):
        self.goto_tab('InventoryTab', 'Inventory')

    @Trace(log)
    def goto_auto_attendants(self):
        sleep(1)
        self.actions.click_element_by_key('SettingsTab')
        link_elem = self.actions.find_element_with_timeout("partial link text", 'Auto')
        link_elem.click()

    @Trace(log)
    def goto_time_frames(self):
        sleep(1)
        self.actions.click_element_by_key('SettingsTab')
        link_elem = self.actions.find_element_with_timeout("partial link text", 'Time')
        link_elem.click()

    @Trace(log)
    def goto_music_on_hold(self):
        sleep(1)
        self.actions.click_element_by_key('SettingsTab')
        link_elem = self.actions.find_element_with_timeout("partial link text", 'Music')
        link_elem.click()

    @Trace(log)
    def goto_locations(self):
        sleep(1)
        self.actions.click_element_by_key('SettingsTab')
        link_elem = self.actions.find_element_with_timeout("partial link text", 'Loc')
        link_elem.click()

domain_view = DomainView()
