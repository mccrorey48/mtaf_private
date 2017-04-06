import lib.logging_esi as logging

from ePhone7.views.base import BaseView
from lib.wrappers import Trace

log = logging.get_logger('esi.settings_view')


class SettingsView(BaseView):

    locators = {
        "AppsBar": { "by": "zpath", "value": "//lv/ll[6]" },
        "AppsText": { "parent_key": "AppsBar", "by": "id", "value": "title" },
        "SettingsExit": { "by": "zpath", "value": "//v/ll/fl/iv[1]" } }

    def __init__(self):
        super(SettingsView, self).__init__()

    @Trace(log)
    def goto_apps(self):
        self.click_named_element('AppsBar')

settings_view = SettingsView()