from lib.android.actions import Actions
from lib.common.wrappers import Trace
import lib.common.logging_esi as logging
log = logging.get_logger('esi.settings_view')


class SettingsView:

    @Trace(log)
    def __init__(self):
        self.actions = Actions(self)

    @Trace(log)
    def goto_apps(self):
        self.actions.click_element_by_key('AppsBar')

settings_view = SettingsView()