import lib.mtaf_logging as mtaf_logging
import unittest
from WebApp.views import *
from lib.trace import TestCase
from WebApp.config.configure import cfg
mtaf_logging.console_handler.setLevel(mtaf_logging.INFO)
log = mtaf_logging.get_logger('mtaf.unit_test')

debug = False
browser = 'chrome'


class LoginTests(unittest.TestCase):

    def setUp(self):
        base_view.open_browser(browser)
        base_view.get_url(cfg.site['app_url'])
        start_view.wait_for_page_title()
        start_view.goto_login()
        login_view.wait_for_page_title()

    def tearDown(self):
        base_view.close_browser()

    # @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_001_login_check_version(self):
        login_view.login_with_good_credentials()
        user_home_view.wait_for_page_title()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_002_login_bad_password(self):
        login_view.login_bad_password()
        login_view.wait_for_invalid_login_alert()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_003_login_no_password(self):
        login_view.login_no_password()
        login_view.wait_for_invalid_login_alert()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_004_login_bad_username(self):
        login_view.login_bad_username()
        login_view.wait_for_invalid_login_alert()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_005_login_no_username(self):
        login_view.login_no_username()
        login_view.wait_for_invalid_login_alert()



