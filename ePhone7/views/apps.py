from time import sleep

import lib.logging_esi as logging
from lib.wrappers import Trace

import lib.filters as filters
from ePhone7.views.base import BaseView

log = logging.get_logger('esi.apps_view')


class AppsView(BaseView):

    locators = {
        "AllVisible": {"by": "zpath", "value": "//gl/tv[1]"},
        "AppsExit": {"by": "zpath", "value": "//v/ll/fl/iv[2]"},
        "ContactsStorage": {"by": "zpath", "value": "//tv[contains(@text,'Contacts Storage')]"},
        "ePhone": {"by": "zpath", "value": "//tv[contains(@text,'ePhone')]"},
        "Tab": {"by": "zpath", "value": "//vp/v/tv"},
        "TabBar": {"by": "id", "value": "tabs"}
    }

    def __init__(self):
        super(AppsView, self).__init__()

    @Trace(log)
    def swipe_up(self):
        self.swipe(300, 750, 300, 100, 1000)
        sleep(1)

    # appium bug, swipe down doesn't work
    # def swipe_down(self):
    #     self.swipe(300, 100, 300, 750, 2000)
    #     sleep(1)

    @Trace(log)
    def goto_all_apps(self):
        elems = self.find_named_elements('Tab')
        self.assert_elements_count(elems, 2, 'app tabs')
        self.assert_element_text_ic(elems[0], 'downloaded', 'first tab')
        self.assert_element_text_ic(elems[1], 'running', 'second tab')
        # Swipe right twice, all apps view appears
        self.swipe(515, 250, 100, 250, 400)
        self.swipe(515, 250, 100, 250, 400)
        elems = self.find_named_elements('Tab')
        self.assert_elements_count(elems, 2, 'app tabs')
        self.assert_element_text_ic(elems[0], 'running', 'first tab')
        self.assert_element_text_ic(elems[1], 'all', 'second tab')

    @Trace(log)
    def goto_settings(self):
        self.click_named_element('AppsExit')

    @Trace(log)
    def goto_ephone_storage(self):
        # Scroll to and touch ePhone, ePhone App info view appears
        tries = 0
        elems = None
        while tries < 4:
            elems = self.find_named_elements('AllVisible',
                                             filters.get_filter('text_start', 'ePhone'))
            tries += 1
            if len(elems) > 0:
                break
            self.swipe_up()
        self.assert_elements_count(elems, 1, 'ePhone menu item')
        self.click_element(elems[0])

    @Trace(log)
    def goto_contacts_storage(self):
        # Scroll to and touch ePhone, ePhone App info view appears
        tries = 0
        elems = None
        while tries < 4:
            elems = self.find_named_elements('AllVisible',
                                             filters.get_filter('text_all', 'Contacts Storage'))
            tries += 1
            if len(elems) > 0:
                break
            self.swipe_up()
        self.assert_elements_count(elems, 1, 'Contacts Storage menu item')
        self.click_element(elems[0])

apps_view = AppsView()
