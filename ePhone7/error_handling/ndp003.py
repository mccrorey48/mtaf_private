# ndp003 When the User Delete the Device
from device import device
from api import api
from mtaf import mtaf_logging
log = mtaf_logging.get_logger('mtaf.ndp003')
# android_actions = AndroidActions()
# adb = ADB()
# device = Device()

print('deleting device')
if api.delete_device():
    print('rebooting device')
    device.reboot()
    print('verifying error page')
    if device.verify_auto_login_page():
        print 'Test Passed'
    else:
        print 'Test Failed'

print('Restoring Data')
api.create_device()
device.retry()

