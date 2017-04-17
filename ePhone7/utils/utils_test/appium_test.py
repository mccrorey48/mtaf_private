from ePhone7.utils.configure import cfg
from ePhone7.views import *
from time import sleep
cfg.set_site('vqda1', 'mm')

def reboot():
    print "rebooting..."
    user_view.click_named_element('PrefsButton')
    assert prefs_view.element_is_present('Preferences')
    prefs_view.hide_list_items()
    prefs_view.click_named_element('System')
    prefs_view.element_is_present('MenuItemNetworkText')
    prefs_view.click_named_element('MenuItemNetworkText')
    assert network_view.element_is_present('NetworkSettingsLabel')
    network_view.click_named_element('NetworkSaveAndReboot')
    assert network_view.element_is_present("VlanRebootAlert")
    base_view.close_appium()
    sleep(30)



base_view.startup()
for i in range(3):
    reboot()
    base_view.startup()
# for i in range(10000):
#     try:
#         print "%s: current activity: %s" % (i, base_view.driver.current_activity)
#     except WebDriverException:
#         print "%s: got WebDriverException" % i
#     sleep(1)
base_view.close_appium()

