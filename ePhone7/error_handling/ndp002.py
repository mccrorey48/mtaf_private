# ndp002 Test when the user modify the device
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