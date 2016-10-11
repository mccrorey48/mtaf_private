import lib.logging_esi as logging

from ePhone7.views.base import BaseView
from lib.wrappers import Trace

log = logging.get_logger('esi.settings_view')


class SettingsView(BaseView):

    def __init__(self):
        super(SettingsView, self).__init__()

    @Trace(log)
    def goto_apps(self):
        self.click_element_by_key('AppsBar')

settings_view = SettingsView()