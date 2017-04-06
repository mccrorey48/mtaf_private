from time import sleep

import lib.logging_esi as logging

from ccd.views.base import BaseView
from lib.wrappers import Trace

log = logging.get_logger('esi.domain_view')


class DomainView(BaseView):

    locators = {
        "Auto": {"by": "partial link text", "value": "Auto"},
        "CallQueuesTab": {"by": "id", "value": "nav-callqueues"},
        "ConferencesTab": {"by": "id", "value": "nav-conferences"},
        "ConfirmYes": {"by": "xpath", "value": "/html/body/div[2]/div[2]/div/a[1]"},
        "HomeTab": {"by": "id", "value": "nav-home-manager"},
        "InventoryTab": {"by": "id", "value": "nav-inventory"},
        "Loc": {"by": "partial link text", "value": "Loc"},
        "Music": {"by": "partial link text", "value": "Music"},
        "NavBanner": {"by": "id", "value": "navigation-subbar"},
        "NavBannerTitle": {"by": "css selector", "value": ".navigation-title", "parent": "NavBanner"},
        "SettingsTab": {"by": "id", "value": "nav-settings"},
        "Time": {"by": "partial link text", "value": "Time"},
        "UsersTab": {"by": "id", "value": "nav-users"}
    }

    def __init__(self):
        super(DomainView, self).__init__()
        self.view_name = "domain"
        self.page_title = "Manager Portal - Home"

    @Trace(log)
    def goto_tab(self, tab_name, banner_title):
        self.click_named_element(tab_name)
        elem = self.find_named_element("NavBannerTitle")
        self.assert_element_text(elem, banner_title, "Banner Title")

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
        self.click_named_element('SettingsTab')
        link_elem = self.find_named_element('Auto')
        link_elem.click()

    @Trace(log)
    def goto_time_frames(self):
        sleep(1)
        self.click_named_element('SettingsTab')
        link_elem = self.find_named_element('Time')
        link_elem.click()

    @Trace(log)
    def goto_music_on_hold(self):
        sleep(1)
        self.click_named_element('SettingsTab')
        link_elem = self.find_named_element('Music')
        link_elem.click()

    @Trace(log)
    def goto_locations(self):
        sleep(1)
        self.click_named_element('SettingsTab')
        link_elem = self.find_named_element('Loc')
        link_elem.click()

domain_view = DomainView()
