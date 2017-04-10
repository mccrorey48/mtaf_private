from ePhone7.utils.configure import cfg
from ePhone7.views import *
from time import sleep
from selenium.common.exceptions import WebDriverException
cfg.set_site('vqda1', 'mm')

def reboot():
    print "rebooting..."
    user_view.click_named_element('PrefsButton')
    assert prefs_view.element_is_present('Preferences')
    prefs_view.hide_list_items()
    prefs_view.click_named_element('System')
    prefs_view.element_is_present('MenuItemNetworkText')
    prefs_view.click_named_element('MenuItemNetworkText')
    assert prefs_view.element_is_present('NetworkSettingsLabel')
    prefs_view.click_named_element('NetworkSaveAndReboot')
    assert prefs_view.element_is_present("VlanRebootAlert")
    i = 1
    while True:
        try:
            if base_view.driver.current_activity != '.activities.MainViewActivity':
                break
        except WebDriverException:
            print "%s: got WebDriverException" % i
        print "waiting for MainViewActivity to stop"
        i += 1
        sleep(1)


def startup():
    while True:
        try:
            current_activity = base_view.driver.current_activity
            print "startup: current_activity = " + current_activity
            if current_activity == '.activites.MainViewActivity':
                if base_view.element_is_present('RegRetryButton'):
                    print "startup: RegRetryButton present"
                    base_view.click_named_element('RegRetryButton')
                    sleep(5)
                else:
                    break
            elif current_activity == 'util.crashreporting.EphoneCrashReportDialog':
                base_view.click_named_element('CrashOkButton')
                sleep(5)
        except WebDriverException:
            print "startup: got WebDriverException"
            sleep(5)

base_view.open_appium('nolaunch')
startup()
# for i in range(10):
    # reboot()
    # startup()
# for i in range(10000):
#     try:
#         print "%s: current activity: %s" % (i, base_view.driver.current_activity)
#     except WebDriverException:
#         print "%s: got WebDriverException" % i
#     sleep(1)
base_view.close_appium()

