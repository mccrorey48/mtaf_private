import re

import lib.logging_esi as logging
from lib.wrappers import Trace

from ePhone7.views.base import BaseView
from lib.user_exception import UserException as Ux

log = logging.get_logger('esi.prefs_view')

list_items = {
    'NeedHelp': ['eHelp', 'Walkthrough'],
    'Personal': ['Sign in with Google', 'Default Contacts Tab', 'Call Forwarding Options'],
    'Phone': ['Brightness', 'Screen Timeout', 'Ringtones', 'Volume Control', 'Auto-Answer Calls', 'Date/Time Options'],
    'System': ['Utilities', 'Network', 'Updates', 'About ePhone7']
}


class PrefsView(BaseView):
    locators = {
        "About": {"by": "zpath", "value": "//el/ll[4]/tv"},
        "AboutOk": {"by": "id", "value": "android:id/button1"},
        "AboutEphone7": {"by": "zpath", "value": "//lv/ll[13]/tv", "text": "About ePhone7"},
        "AppVersion": {"by": "id", "value": "com.esi_estech.ditto:id/app_version"},
        "AutoAnswerSwitch": {"by": "id", "value": "com.esi_estech.ditto:id/settings_list_auto_answer_switch"},
        "CallForwardingOptions": {"by": "zpath", "value": "//el/ll[3]/tv", "text": "Call Forwarding Options"},
        "Close": {"by": "id", "value": "com.esi_estech.ditto:id/close_button"},
        "DisplayBrightness": {"by": "zpath", "value": "//lv/ll[8]/tv", "text": "Display Brightness"},
        "DisplaySleepTimer": {"by": "zpath", "value": "//lv/ll[9]/tv", "text": "Display Sleep Timer"},
        "eHelp": {"by": "zpath", "value": "//lv/ll[4]/tv", "text": "eHelp"},
        "ListItemTitle": {"by": "id", "value": "com.esi_estech.ditto:id/settings_list_item_title"},
        "LogoutAccount": {"by": "zpath", "value": "//lv/ll[12]/tv", "text": "Logout Account"},
        "LogoutCancel": {"by": "id", "value": "com.esi_estech.ditto:id/cancel_button"},
        "LogoutConfirm": {"by": "id", "value": "com.esi_estech.ditto:id/confirm_button"},
        "MenuCategories": {"by": "id", "value": "com.esi_estech.ditto:id/settings_header_label"},
        "MenuItems": {"by": "xpath", "value": "//el/ll"},
        "NeedHelp": {"by": "zpath", "value": "//el/rl[1]/tv[1]", "text": "Need Help?"},
        "Personal": {"by": "zpath", "value": "//el/rl[2]/tv[1]", "text": "Personal"},
        "Phone": {"by": "zpath", "value": "//el/rl[3]/tv[1]", "text": "Phone"},
        "PhoneUpdates": {"by": "zpath", "value": "//lv/ll[10]/tv", "text": "Phone Updates"},
        "Preferences": {"by": "id", "value": "com.esi_estech.ditto:id/settings_list"},
        "Ringtones": {"by": "zpath", "value": "//lv/ll[7]/tv", "text": "Ringtones"},
        "SignInWithGoogle": {"by": "zpath", "value": "//lv/ll[2]/tv", "text": "Sign in with Google"},
        "System": {"by": "zpath", "value": "//el/rl[4]/tv[1]", "text": "System"},
        "VolumeSettings": {"by": "zpath", "value": "//lv/ll[6]/tv", "text": "Volume Settings"}
    }

    def __init__(self):
        super(PrefsView, self).__init__()

    def hide_list_items(self):
        titles_shown = [el.text for el in self.find_elements('ListItemTitle')]
        if len(titles_shown) == 0:
            return
        for header in list_items.keys():
            if list_items[header][0] in titles_shown:
                self.click_element_by_name(header)
            titles_shown = [el.text for el in self.find_elements('ListItemTitle')]
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
        self.click_element_by_name('Phone')
        elem = self.find_element('AutoAnswerSwitch')
        y = elem.location['y'] + (elem.size['height'] / 2)
        left = elem.location['x']
        right = elem.location['x'] + (elem.size['width'] / 2)
        if on:
            self.swipe(left, y, right, y, 1000)
        else:
            self.swipe(right, y, left, y, 1000)
        self.click_element_by_name('Phone')

    @Trace(log)
    def logout(self):
        self.click_element_by_name('LogoutAccount')

    @Trace(log)
    def logout_cancel(self):
        self.click_element_by_name('LogoutCancel')

    @Trace(log)
    def logout_confirm(self):
        self.click_element_by_name('LogoutConfirm')

    @Trace(log)
    def exit_prefs(self):
        self.click_element_by_name('Close')

    @Trace(log)
    def get_app_version(self):
        self.hide_list_items()
        self.click_element_by_name('System')
        self.click_element_by_name('About')
        about_popup = self.find_element('AppVersion')
        source = about_popup.text
        self.click_element_by_name('AboutOk')
        self.click_element_by_name('System')
        m = re.match('App Version : (\S*)', source.encode('utf8'))
        if m is None:
            return "Unknown Version"
        version = re.sub('\.', '_', m.group(1))
        # make the xml and csv directories for this version (or if it already exists, ignore the resulting exception)
        return version

    @Trace(log)
    def verify_view(self):
        return len(self.find_elements('MenuCategories')) > 0


prefs_view = PrefsView()
