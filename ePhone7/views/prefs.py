from lib.android.actions import Actions
import lib.common.logging_esi as logging
from lib.common.wrappers import Trace
log = logging.get_logger('esi.prefs_view')


class PrefsView:

    @Trace(log)
    def __init__(self):
        self.actions = Actions(self)

    @Trace(log)
    def set_auto_answer_off(self):
        self.set_auto_answer(on=False)

    @Trace(log)
    def set_auto_answer(self, on=True):
        elem = self.actions.find_element_by_key('AutoAnswerSwitch')
        y = elem.location['y'] + (elem.size['height'] / 2)
        left = elem.location['x']
        right = elem.location['x'] + (elem.size['width'] / 2)
        if on:
            self.actions.swipe(left, y, right, y, 1000)
        else:
            self.actions.swipe(right, y, left, y, 1000)

    @Trace(log)
    def logout(self):
        self.actions.click_element_by_key('LogoutAccount')

    @Trace(log)
    def logout_cancel(self):
        self.actions.click_element_by_key('LogoutCancel')

    @Trace(log)
    def logout_confirm(self):
        self.actions.click_element_by_key('LogoutConfirm')

    @Trace(log)
    def exit_prefs(self):
        self.actions.click_element_by_key('Close')

    @Trace(log)
    def get_app_version(self):
        self.actions.click_element_by_key('About')
        about_popup = self.actions.find_element_by_key('AppVersion')
        about_text = about_popup.text
        self.actions.click_element_by_key('AboutOk')
        return about_text

prefs_view = PrefsView()
