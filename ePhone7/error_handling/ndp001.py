# bt001 
from mtaf.ADB import ADB
from mtaf.android_actions import AndroidActions
from ePhone7.views import *

android_actions = AndroidActions()
adb = ADB()


def reboot_phone():
    print 'open appium', android_actions.open_appium()
    print 'rebooting', adb.reboot_device()
    print 'close appium until reboot', android_actions.close_appium()
    print 'open appium', android_actions.open_appium()
    print 'startup', base_view.startup()
    return True


reboot_phone()
if android_actions.get_current_activity() == '.activities.AutoLoginActivity':
    print "Popup Screen"
    android_actions.element_with_text_is_present('Device Not Registered')
    print "Correct message Device Not Registered Screen"
else:
    print "Incorrect"
