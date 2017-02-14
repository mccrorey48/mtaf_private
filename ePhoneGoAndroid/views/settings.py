import lib.logging_esi as logging

from ePhoneGoAndroid.views.base import BaseView
from lib.wrappers import Trace

log = logging.get_logger('esi.settings_view')


class SettingsView(BaseView):

    locators = {
        "ActionBarText": {"by": "xpath", "value": "//fl[1]/vg/tv", "text": "Settings"},
        "Storage": {"by": "id", "value": "com.android.settings:id/title", "text": "Storage"}
    }

    def __init__(self):
        super(SettingsView, self).__init__()

    def scroll_and_get_element(self, name):
        if self.element_is_present(name):
            return self.find_element(name)


settings_view = SettingsView()
