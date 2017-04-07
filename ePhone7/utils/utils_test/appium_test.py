from ePhone7.utils.configure import cfg
from ePhone7.views import *
cfg.set_site('vqda1', 'mm')
base_view.open_appium('nolaunch')
print "current activity: %s" % base_view.driver.current_activity
base_view.close_appium()
pass

