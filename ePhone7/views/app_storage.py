from lib.android.actions import Actions
from lib.common.wrappers import Trace
import lib.common.logging_esi as logging
log = logging.get_logger('esi.app_storage_view')


class AppStorageView:

    @Trace(log)
    def __init__(self):
        self.actions = Actions(self)

    @Trace(log)
    def delete_data(self):
        # Touch Clear data, verification popup appears
        elems = self.actions.find_elements_by_key('ClearData')
        if len(elems) == 0:
            log.info("AppStorageView Data Already Cleared")
        else:
            self.actions.tap_element(elems[0])
            # Touch OK, verification popup closes, Clear data button disabled, Data is now 0.00B
            elem = self.actions.find_element_by_key('Ok')
            self.actions.tap_element(elem)
        elem = self.actions.find_element_by_key('DataSize')
        self.actions.assert_element_text(elem, '0.00B', "Data Size text")

    @Trace(log)
    def goto_apps(self):
        # Touch Settings icon at top left of screen, all apps view appears
        self.actions.click_element_by_key('Apps')

app_storage_view = AppStorageView()
