from mtaf.ADB import ADB
from mtaf.android_actions import AndroidActions
from ePhone7.views import *

android_actions = AndroidActions()
adb = ADB()


print 'open appium'
base_view.open_appium()
if android_actions.get_current_activity() == '.activities.AutoLoginActivity':
    android_actions.element_with_text_is_present('Device Not Registered')
    print "Correct message Device Not Registered Screen"
elif android_actions.get_current_activity() == '.activities.MainViewActivity':
    print 'rebooting'
    adb.reboot_device()
    print 'close appium until reboot'
    base_view.close_appium_until_reboot()
    if android_actions.element_with_text_is_present('Not Registered'):
        print("Not Registered Home Screen")
    if android_actions.element_with_text_is_present('Offline'):
        print("Offline Home Screen")
    if android_actions.element_with_text_is_present('Online'):
        print("Online Home Screen")
    if android_actions.element_with_text_is_present('2012'):
        print("2012 Home Screen")
    if android_actions.element_with_text_is_present('Jessica Sabugo'):
        print("Jessica Sabugo")


def res():
    # print 'open appium'  # delete
    # base_view.open_appium()

    # if current_activity == '.activities.AutoLoginActivity':
    #     log.debug("current activity: %s", current_activity)
    #     if android_actions.element_with_text_is_present('Device Not Registered', timeout=1):
    #         log.debug("element with text 'Device Not Registered' is present")
    #         print "Device Not Registered Screen"  # delete
    #     else:
    #         log.debug("element with text 'Device Not Registered' is not present")
    # elif current_activity == '.activities.MainViewActivity':
    #     # if android_actions.element_with_text_is_present('Not Registered'):
    #     #     print("Not Registered Home Screen")
    #     # if android_actions.element_with_text_is_present('Offline'):
    #     #     print("Offline Home Screen")
    #     print "home Screen"
    # print 'rebooting'  # delete
    print 'reboot phone'  # delete
    adb.reboot_device()
    # sleep(5)
    print 'close appium until reboot'
    base_view.close_appium_until_reboot()
    current_activity = android_actions.get_current_activity()
    if current_activity == '.activities.AutoLoginActivity':
        # if android_actions.element_with_text_is_present('Not Registered'):
        #     print("Not Registered Home Screen")
        # if android_actions.element_with_text_is_present('Offline'):
        #     print("Offline Home Screen")
        print "home Screen"
    elif current_activity == '.util.crashreporting.EPhoneCrashReportDialog':
        android_actions.click_named_element('CrashOkButton')


res()
