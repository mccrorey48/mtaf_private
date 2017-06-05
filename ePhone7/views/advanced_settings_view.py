import lib.logging_esi as logging

from ePhone7.views.base_view import BaseView
from ePhone7.config.configure import cfg
from lib.wrappers import Trace
from time import sleep
from lib.user_exception import UserException as Ux

log = logging.get_logger('esi.settings_view')


class AdvancedSettingsView(BaseView):

    locators = {
        "AdvancedCheckbox": {"by": "id", "value": "com.esi_estech.ditto:id/checkbox"},
        "AdvancedItems": {"by": "id", "value": "android:id/title"},
        "AdvancedOptions": {"by": "zpath", "value": "//sp/rl/v[1]/fl/ll/fl/rv/tv[1]"},
        "AppsBar": {"by": "zpath", "value": "//lv/ll[6]"},
        "AppsText": {"parent_key": "AppsBar", "by": "id", "value": "title"},
        "CallRecordEnableText": {"by": "id", "value": "android:id/title", "text": "Call Record Enable"},
        "OtaAddressOk": {"by": "id", "value": "android:id/button1"},
        "TestOtaEditText": {"by": "id", "value": "android:id/edit"},
        "TestOtaServerUrlText": {"by": "id", "value": "android:id/title", "text": "Test OTA Server URL"},
        "UseTestOtaServerText": {"by": "id", "value": "android:id/title", "text": "Use Test OTA Server"},
    }

    def __init__(self):
        super(AdvancedSettingsView, self).__init__()
        BaseView.settings_view = self

    @Trace(log)
    def goto_apps(self):
        self.click_named_element('AppsBar')

    @Trace(log)
    def set_ota_server(self, ota_server):
        if not self.element_is_present('AdvancedOptions'):
            raise Ux("Expected Advanced Options view to appear but it did not")
        elems = self.find_named_elements('AdvancedItems')
        if len(elems) == 0:
            raise Ux('No "AvancedItems" elements found')
        self.long_press_scroll(elems[-1], elems[0])
        if not self.element_is_present('TestOtaServerUrlText'):
            # one retry in case the long_press_scroll didn't work
            self.long_press_scroll(elems[-1], elems[0])
        use_ota_text = self.find_named_element('UseTestOtaServerText')
        text_ycenter = use_ota_text.location['y'] + (use_ota_text.size['height'] / 2)
        checkboxes = self.find_named_elements('AdvancedCheckbox')
        for cb in checkboxes:
            min_y = cb.location['y']
            max_y = min_y + cb.size['height']
            if min_y < text_ycenter < max_y:
                break
        else:
            raise Ux('"Use Test OTA Server" checkbox not found')
        if cb.get_attribute('checked') == 'false':
            cb.click()
        self.click_named_element('TestOtaServerUrlText')
        ota_url = self.find_named_element('TestOtaEditText')
        ota_url.clear()
        if ota_server == 'alpha':
            ota_url.set_text(cfg.site["OtaAlphaUrl"])
        elif ota_server == 'beta':
            ota_url.set_text(cfg.site["OtaBetaUrl"])
        elif ota_server == 'prod':
            ota_url.set_text(cfg.site["OtaProdUrl"])
        else:
            raise Ux('ota_server must be "alpha", "beta" or "prod", got %s' % ota_server)
        self.click_named_element('OtaAddressOk')
        self.send_keycode_back()
        sleep(5)


advanced_settings_view = AdvancedSettingsView()
