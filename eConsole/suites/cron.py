import lib.logging_esi as logging
logging.console_handler.setLevel(logging.INFO)
log = logging.get_logger('esi.cron')
with logging.msg_src_cm('importing modules'):
    import unittest
    from eConsole.views import *
    from lib.wrappers import TestCase

debug = False
browser = 'chrome'


class LoginTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        base_view.open_browser(browser)
        base_view.get_portal_url()

    @classmethod
    def tearDownClass(cls):
        base_view.close_browser()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_001_login_check_version(self):
        login_view.input_username('select')
        login_view.input_password('select')
        login_view.click_login_button()

