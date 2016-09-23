from time import sleep
import lib.common.filters as filters
from lib.common.wrappers import Trace
import lib.common.logging_esi as logging
from ePhone7.views.base import BaseView
log = logging.get_logger('esi.apps_view')


class AppsView(BaseView):

    @Trace(log)
    def __init__(self):
        super(AppsView, self).__init__()

    @Trace(log)
    def swipe_up(self):
        self.actions.swipe(300, 750, 300, 100, 1000)
        sleep(1)

    # appium bug, swipe down doesn't work
    # def swipe_down(self):
    #     self.actions.swipe(300, 100, 300, 750, 2000)
    #     sleep(1)

    @Trace(log)
    def goto_all_apps(self):
        elems = self.actions.find_elements_by_key('Tab')
        self.actions.assert_elements_count(elems, 2, 'app tabs')
        self.actions.assert_element_text_ic(elems[0], 'downloaded', 'first tab')
        self.actions.assert_element_text_ic(elems[1], 'running', 'second tab')
        # Swipe right twice, all apps view appears
        self.actions.swipe(515, 250, 100, 250, 400)
        self.actions.swipe(515, 250, 100, 250, 400)
        elems = self.actions.find_elements_by_key('Tab')
        self.actions.assert_elements_count(elems, 2, 'app tabs')
        self.actions.assert_element_text_ic(elems[0], 'running', 'first tab')
        self.actions.assert_element_text_ic(elems[1], 'all', 'second tab')

    @Trace(log)
    def goto_settings(self):
        self.actions.click_element_by_key('AppsExit')

    @Trace(log)
    def goto_ephone_storage(self):
        # Scroll to and touch ePhone, ePhone App info view appears
        tries = 0
        elems = None
        while tries < 4:
            elems = self.actions.find_elements_by_key('AllVisible',
                                                      filters.get_filter('text_start', 'ePhone'))
            tries += 1
            if len(elems) > 0:
                break
            self.swipe_up()
        self.actions.assert_elements_count(elems, 1, 'ePhone menu item')
        self.actions.click_element(elems[0])

    @Trace(log)
    def goto_contacts_storage(self):
        # Scroll to and touch ePhone, ePhone App info view appears
        tries = 0
        elems = None
        while tries < 4:
            elems = self.actions.find_elements_by_key('AllVisible',
                                                      filters.get_filter('text_all', 'Contacts Storage'))
            tries += 1
            if len(elems) > 0:
                break
            self.swipe_up()
        self.actions.assert_elements_count(elems, 1, 'Contacts Storage menu item')
        self.actions.click_element(elems[0])

apps_view = AppsView()
