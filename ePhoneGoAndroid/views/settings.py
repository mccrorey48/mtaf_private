import lib.logging_esi as logging
from lib.user_exception import UserException as Ux

from ePhoneGoAndroid.views.base import BaseView
from lib.wrappers import Trace

log = logging.get_logger('esi.settings_view')


class SettingsView(BaseView):

    locators = {
        "ActionBarText": {"by": "xpath", "value": "//fl[1]/vg/tv", "text": "Settings"},
        "Storage": {"by": "id", "value": "com.android.settings:id/title", "text": "Storage"},
        "TitleAny": {"by": "id", "value": "com.android.settings:id/title"}
    }

    def __init__(self):
        super(SettingsView, self).__init__()

    def scroll_and_get_element(self, name):
        if self.element_is_present(name):
            return self.find_element(name)
        # scroll to top
        while True:
            elems = self.find_elements("TitleAny")
            before_titles = [elem.text for elem in elems]
            self.scroll(elems[0], elems[-1])
            elems = self.find_elements("TitleAny")
            after_titles = [elem.text for elem in elems]
            if before_titles == after_titles:
                break
        while True:
            elems = self.find_elements("TitleAny")
            before_titles = [elem.text for elem in elems]
            self.scroll(elems[-1], elems[0])
            elems = self.find_elements("TitleAny")
            after_titles = [elem.text for elem in elems]
            if self.element_is_present(name):
                return self.find_element(name)
            if before_titles == after_titles:
                raise Ux("Element %s not found" % name)


settings_view = SettingsView()
