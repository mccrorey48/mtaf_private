import lib.common.logging_esi as logging
import re
from lib.common.wrappers import Trace
from ePhone7.views.base import BaseView
from lib.common.user_exception import UserException as Ux
log = logging.get_logger('esi.prefs_view')

list_items = {
    'NeedHelp': ['eHelp', 'Walkthrough'],
    'Personal': ['Sign in with Google', 'Default Contacts Tab', 'Call Forwarding Options'],
    'Phone': ['Brightness', 'Screen Timeout', 'Ringtones', 'Volume Control', 'Auto-Answer Calls', 'Date/Time Options'],
    'System': ['Utilities', 'Network', 'Updates', 'About ePhone7']
}


class PrefsView(BaseView):

    @Trace(log)
    def __init__(self):
        super(PrefsView, self).__init__()

    def hide_list_items(self):
        titles_shown = [el.text for el in self.actions.find_elements_by_key('ListItemTitle')]
        if len(titles_shown) == 0:
            return
        for header in list_items.keys():
            if list_items[header][0] in titles_shown:
                self.actions.click_element_by_key(header)
            titles_shown = [el.text for el in self.actions.find_elements_by_key('ListItemTitle')]
            if len(titles_shown) == 0:
                return
            if list_items[header][0] in titles_shown:
                raise Ux ('unable to hide list items for header %s' % header)



    @Trace(log)
    def set_auto_answer_off(self):
        self.set_auto_answer(on=False)

    @Trace(log)
    def set_auto_answer(self, on=True):
        self.hide_list_items()
        self.actions.click_element_by_key('Phone')
        elem = self.actions.find_element_by_key('AutoAnswerSwitch')
        y = elem.location['y'] + (elem.size['height'] / 2)
        left = elem.location['x']
        right = elem.location['x'] + (elem.size['width'] / 2)
        if on:
            self.actions.swipe(left, y, right, y, 1000)
        else:
            self.actions.swipe(right, y, left, y, 1000)
        self.actions.click_element_by_key('Phone')

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
        self.hide_list_items()
        self.actions.click_element_by_key('System')
        self.actions.click_element_by_key('About')
        about_popup = self.actions.find_element_by_key('AppVersion')
        source = about_popup.text
        self.actions.click_element_by_key('AboutOk')
        self.actions.click_element_by_key('System')
        m = re.match('App Version : (\S*)', source.encode('utf8'))
        if m is None:
            return "Unknown Version"
        version = re.sub('\.', '_', m.group(1))
        # make the xml and csv directories for this version (or if it already exists, ignore the resulting exception)
        return version

    @Trace(log)
    def verify_view(self):
        return len(self.actions.find_elements_by_key('MenuCategories')) > 0


prefs_view = PrefsView()
