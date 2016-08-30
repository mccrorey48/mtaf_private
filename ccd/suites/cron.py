import lib.common.logging_esi as logging_esi
logging_esi.console_handler.setLevel(logging_esi.INFO)
log = logging_esi.get_logger('esi.ccd_cron')
with logging_esi.msg_src_cm('importing modules'):
    import unittest
    from lib.chrome.actions import Actions
    from ccd.views.reseller_home import reseller_home_view
    from ccd.views.login import login_view
    from lib.common.wrappers import TestCase

run_list = [
    'test_010_login_get_version'
    ]


class CronTests(unittest.TestCase):

    @TestCase
    def test_010_login_check_version(self):
        login_view.login_with_good_credentials()
        reseller_home_view.wait_for_view()
        reseller_home_view.version_should_be_correct()
        reseller_home_view.logout()

    @TestCase
    def test_020_login_bad_password_should_fail(self):
        login_view.login_bad_password()

    @TestCase
    def test_030_login_no_password_should_fail(self):
        login_view.login_no_password()

    @TestCase
    def test_040_login_bad_username_should_fail(self):
        login_view.login_bad_username()

    @TestCase
    def test_040_login_no_username_should_fail(self):
        login_view.login_no_username()


    @classmethod
    def tearDownClass(cls):
        Actions.closeDriver()


