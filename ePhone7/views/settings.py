from lib.common.wrappers import Trace
import lib.common.logging_esi as logging
from ePhone7.views.base import BaseView
log = logging.get_logger('esi.settings_view')


class SettingsView(BaseView):

    @Trace(log)
    def __init__(self):
        super(SettingsView, self).__init__()

    @Trace(log)
    def goto_apps(self):
        self.actions.click_element_by_key('AppsBar')

settings_view = SettingsView()