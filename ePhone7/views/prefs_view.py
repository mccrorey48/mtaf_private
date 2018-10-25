import re

from mtaf import mtaf_logging
from mtaf.decorators import Trace
from mtaf.user_exception import UserException as Ux

from ePhone7.views.base_view import BaseView
from time import sleep

log = mtaf_logging.get_logger('mtaf.prefs_view')

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
        "ActiveCallScreen": {"by": "id", "value": "com.esi_estech.ditto:id/title", "text": "Active Call Screen"},
        "ActiveCallDialpad": {"by": "id", "value": "com.esi_estech.ditto:id/title", "text": "Active Call Dialpad"},
        "AppVersion": {"by": "id", "value": "com.esi_estech.ditto:id/app_version"},
        "AutoAnswerSwitch": {"by": "id", "value": "com.esi_estech.ditto:id/settings_list_auto_answer_switch"},
        "CallForwardingOptions": {"by": "zpath", "value": "//el/ll[3]/tv", "text": "Call Forwarding Options"},
        "CallHistory": {"by": "id", "value": "com.esi_estech.ditto:id/title", "text": "Call History"},
        "CloseButton": {"by": "id", "value": "com.esi_estech.ditto:id/close_button"},
        "Collapse": {"by": "id", "value": "com.esi_estech.ditto:id/group_indicator_text", "text": "Collapse"},
        "ContactManagement": {"by": "id", "value": "com.esi_estech.ditto:id/title", "text": "Contact Management"},
        "DialpadScreen": {"by": "id", "value": "com.esi_estech.ditto:id/title", "text": "Dialpad Screen"},
        "DisplayBrightness": {"by": "zpath", "value": "//lv/ll[8]/tv", "text": "Display Brightness"},
        "DisplaySleepTimer": {"by": "zpath", "value": "//lv/ll[9]/tv", "text": "Display Sleep Timer"},
        "eHelp": {"by": "zpath", "value": "//el/ll[1]/tv", "text": "eHelp"},
        "eHelpEmailSent": {"by": "id", "value": "com.esi_estech.ditto:id/content_text"},
        "ListItemTitle": {"by": "id", "value": "com.esi_estech.ditto:id/settings_list_item_title"},
        "LogoutAccount": {"by": "zpath", "value": "//lv/ll[12]/tv", "text": "Logout Account"},
        "LogoutCancel": {"by": "id", "value": "com.esi_estech.ditto:id/cancel_button"},
        "LogoutConfirm": {"by": "id", "value": "com.esi_estech.ditto:id/confirm_button"},
        "MenuCategories": {"by": "id", "value": "com.esi_estech.ditto:id/settings_header_label"},
        "MenuItems": {"by": "zpath", "value": "//el/ll"},
        "MenuItemNetworkText": {"by": "zpath", "value": "//el/ll/tv", "text": "Network"},
        "MenuItemTexts": {"by": "zpath", "value": "//el/ll/tv"},
        "NeedHelp": {"by": "zpath", "value": "//el/rl[1]/tv[1]", "text": "Need Help?"},
        "Personal": {"by": "zpath", "value": "//el/rl[2]/tv[1]", "text": "Personal"},
        "Phone": {"by": "zpath", "value": "//el/rl[3]/tv[1]", "text": "Phone"},
        "Preferences": {"by": "id", "value": "com.esi_estech.ditto:id/settings_list"},
        "PreferencesScreen": {"by": "id", "value": "com.esi_estech.ditto:id/title", "text": "Preferences Screen"},
        "PrefsLabel": {"by": "id", "value": "com.esi_estech.ditto:id/preferences_label"},
        "RebootEPhone7": {"by": "uia_text", "value": "Reboot ePhone7"},
        "Ringtones": {"by": "zpath", "value": "//lv/ll[7]/tv", "text": "Ringtones"},
        "SignInWithGoogle": {"by": "zpath", "value": "//lv/ll[2]/tv", "text": "Sign in with Google"},
        "System": {"by": "zpath", "value": "//el/rl[4]/tv[1]", "text": "System"},
        "SystemUpdate": {"by": "id", "value": "com.esi_estech.ditto:id/aosp_update_row"},
        "SystemVersion": {"by": "id", "value": "com.esi_estech.ditto:id/system_version"},
        "UpgradeButton": {"by": "id", "value": "com.fsl.android.ota:id/upgrade_button"},
        "Utilities": {"by": "uia_text", "value": "Utilities"},
        "VisualVoicemail": {"by": "id", "value": "com.esi_estech.ditto:id/title", "text": "Visual Voicemail"},
        "VolumeSettings": {"by": "zpath", "value": "//lv/ll[6]/tv", "text": "Volume Settings"},
        "VoicemailPlayback": {"by": "id", "value": "com.esi_estech.ditto:id/title", "text": "Voicemail Playback"},
        "Walkthrough": {"by": "zpath", "value": "//ll[4]/tv", "text": "Walkthrough"},
        "WelcometoePhone7" : {"by": "id", "value": "com.esi_estech.ditto:id/title", "text": "Welcome to ePhone7!"},
        "WiredHeadsetSwitch": {"by": "id", "value": "com.esi_estech.ditto:id/headset_enabled_switch"}
    }

    def __init__(self):
        super(PrefsView, self).__init__()
        BaseView.prefs_view = self
        self.presence_element_names = ['Preferences', 'PrefsLabel']

    def hide_list_items(self):
        titles_shown = [el.text for el in self.find_named_elements('ListItemTitle')]
        if len(titles_shown) == 0:
            return
        for header in list_items.keys():
            if list_items[header][0] in titles_shown:
                self.click_named_element(header)
            titles_shown = [el.text for el in self.find_named_elements('ListItemTitle')]
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
        self.click_named_element('Phone')
        elem = self.find_named_element('AutoAnswerSwitch')
        y = elem.location['y'] + (elem.size['height'] / 2)
        left = elem.location['x']
        right = elem.location['x'] + (elem.size['width'] / 2)
        if on:
            self.swipe(left, y, right, y, 1000)
        else:
            self.swipe(right, y, left, y, 1000)
        self.click_named_element('Phone')

    @Trace(log)
    def swipefromrighttoleft(self):
        self.swipe(300, 300, 50, 300, 500)
        sleep(2)


    @Trace(log)
    def logout(self):
        self.click_named_element('LogoutAccount')

    @Trace(log)
    def logout_cancel(self):
        self.click_named_element('LogoutCancel')

    @Trace(log)
    def logout_confirm(self):
        self.click_named_element('LogoutConfirm')

    @Trace(log)
    def exit_prefs(self):
        self.click_named_element('CloseButton')

    @Trace(log)
    def get_app_version(self):
        self.hide_list_items()
        self.click_named_element('System')
        self.click_named_element('About')
        about_popup = self.find_named_element('AppVersion')
        source = about_popup.text
        self.click_named_element('AboutOk')
        self.click_named_element('System')
        m = re.match('App Version : (\S*)', source.encode('utf8'))
        if m is None:
            return "Unknown Version"
        version = re.sub('\.', '_', m.group(1))
        return version

    @Trace(log)
    def verify_view(self):
        return len(self.find_named_elements('MenuCategories')) > 0


prefs_view = PrefsView()
