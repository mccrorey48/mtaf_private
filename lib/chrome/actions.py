from PIL import Image
import os
from lib.selenium.selenium_actions import SeleniumActions
from time import time, sleep, strftime, localtime

import lib.common.logging_esi as logging
from lib.common.configure import cfg
from lib.common.remote import remote
from lib.android.zpath import expand_zpath
from lib.common.wrappers import Trace
from selenium.common.exceptions import WebDriverException
from lib.common.user_exception import UserException as Ux, UserFailException as Fx

log = logging.get_logger('esi.action')
test_screenshot_folder = cfg.test_screenshot_folder
keycodes = {'KEYCODE_%d' % k: k + 7 for k in range(10)}


class Actions(SeleniumActions):

    def __init__(self, leaf_view=None):
        SeleniumActions.__init__(self)
        self.leaf_view = leaf_view
        self.failureException = Fx

