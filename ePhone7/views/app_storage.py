import lib.logging_esi as logging

from ePhone7.views.base import BaseView
from lib.wrappers import Trace

log = logging.get_logger('esi.app_storage_view')


class AppStorageView(BaseView):

    def __init__(self):
        super(AppStorageView, self).__init__()

    @Trace(log)
    def delete_data(self):
        # Touch Clear data, verification popup appears
        elems = self.find_elements('ClearData')
        if len(elems) == 0:
            log.info("AppStorageView Data Already Cleared")
        else:
            self.tap_element(elems[0])
            # Touch OK, verification popup closes, Clear data button disabled, Data is now 0.00B
            elem = self.find_element('Ok')
            self.tap_element(elem)
        elem = self.find_element('DataSize')
        self.assert_element_text(elem, '0.00B', "Data Size text")

    @Trace(log)
    def goto_apps(self):
        # Touch Settings icon at top left of screen, all apps view appears
        self.click_element_by_name('Apps')

app_storage_view = AppStorageView()
