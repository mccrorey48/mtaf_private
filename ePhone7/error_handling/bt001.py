# bt001 Test when the bt server cannot be reachable (Stopping nginx)
from mtaf.ADB import ADB
from mtaf.android_actions import AndroidActions
from ePhone7.views import *
from mtaf.user_exception import UserException as Ux, UserTimeoutException as Tx, UserFailException as Fx
from mtaf import mtaf_logging

android_actions = AndroidActions()
adb = ADB()
# log = mtaf_logging.get_logger('error_handling.bt001')


def reboot_phone():
    print 'open appium', base_view.open_appium()
    print 'rebooting', adb.reboot_device()
    print 'close appium until reboot', base_view.close_appium_until_reboot()
    print 'startup', base_view.startup()
    return True


reboot_phone()
if android_actions.get_current_activity() == '.activities.AutoLoginActivity':
    print "Popup Screen"
    android_actions.element_with_text_is_present('Device Not Registered')
    print "Correct message Device Not Registered Screen"
elif android_actions.get_current_activity() == '.activities.MainViewActivity':
    print "Home Screen"
    if android_actions.element_with_text_is_present('Offline') and\
            android_actions.element_with_text_is_present('Not Registered'):
        print "Correct Message in Home Screen"
    elif android_actions.element_with_text_is_present('Online') and \
            android_actions.element_with_text_is_present('Jessica Sabugo'):
        print "InCorrect Message in Home Screen"

