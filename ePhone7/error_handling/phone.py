from mtaf.ADB import ADB
from ePhone7.views.base_view import *
from time import sleep
from mtaf import mtaf_logging
log = mtaf_logging.get_logger('mtaf.phone')

home_page_activity = '.activities.MainViewActivity'
auto_login_page_activity = '.activities.AutoLoginActivity'
crash_activity = '.util.crashreporting.EPhoneCrashReportDialog'


class Device(BaseView):
    driver = None
    adb = ADB()

    def __init__(self):
        super(Device, self).__init__()
        self.current_activity = ''

    def reboot(self):
        log.debug("rebooting phone")
        self.adb.reboot_device()
        sleep(10)
        log.debug("closing appium until reboot is completed")
        self.close_appium_until_reboot()

    def verify_auto_login_page(self):
        current_activity = self.get_current_activity()
        if current_activity == auto_login_page_activity:
            log.debug("current activity: %s", current_activity)
            if self.element_with_text_is_present('Device Registration Error', timeout=1):
                log.debug("element with text 'Device Not Registered Error' is present")
                return True
            else:
                log.info("element with text 'Device Registration Error' is not present")
                return False
        elif current_activity == home_page_activity:
            log.info("Error: home page is displayed")
        elif current_activity == crash_activity:
            self.click_named_element('CrashOkButton')  # pending
            log.info("Error: device crash")

    def retry(self):
        # android_actions.open_appium()
        if self.element_with_text_is_present('Retry', timeout=1):
            log.debug('Touching the Retry button')
            base_view.touch_element_with_text(text='Retry')


device = Device()
