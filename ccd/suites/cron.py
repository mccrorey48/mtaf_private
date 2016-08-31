import lib.common.logging_esi as logging_esi
logging_esi.console_handler.setLevel(logging_esi.INFO)
log = logging_esi.get_logger('esi.ccd_cron')
with logging_esi.msg_src_cm('importing modules'):
    import unittest
    from lib.chrome.actions import Actions
    from ccd.views.base import base_view
    from ccd.views.login import login_view
    from ccd.views.reseller import reseller_view
    from ccd.views.reseller_home import reseller_home_view
    from ccd.views.reseller_domains import reseller_domains_view
    from ccd.views.reseller_inventory import reseller_inventory_view
    from lib.common.wrappers import TestCase

run_list = [
    'test_001_login_check_version',
    'test_002_login_bad_password_should_fail',
    'test_003_login_no_password_should_fail',
    'test_004_login_bad_username_should_fail',
    'test_005_login_no_username_should_fail',
    'test_101_goto_home',
    'test_102_goto_domains',
    'test_103_goto_inventory'
    ]


class LoginTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        base_view.get_portal_url()

    @classmethod
    def tearDownClass(cls):
        Actions.closeDriver()

    @TestCase(log, run_list)
    def test_001_login_check_version(self):
        login_view.login_with_good_credentials()
        reseller_home_view.wait_for_view()
        reseller_home_view.version_should_be_correct()
        reseller_home_view.logout()
        login_view.wait_for_view()

    @TestCase(log, run_list)
    def test_002_login_bad_password_should_fail(self):
        login_view.login_bad_password()
        login_view.wait_for_password_alert()

    @TestCase(log, run_list)
    def test_003_login_no_password_should_fail(self):
        login_view.login_no_password()
        login_view.wait_for_password_alert()

    @TestCase(log, run_list)
    def test_004_login_bad_username_should_fail(self):
        login_view.login_bad_username()
        login_view.wait_for_password_alert()

    @TestCase(log, run_list)
    def test_004_login_no_username_should_fail(self):
        login_view.login_no_username()
        login_view.wait_for_password_alert()



class ResellerTests(unittest.TestCase):

    def setUp(self):
        login_view.login_with_good_credentials()
        reseller_home_view.wait_for_view()

    def tearDown(self):
        reseller_view.logout()

    def tearDownClass(self):
        Actions.closeDriver()

    @classmethod
    def setUp(cls):
        login_view.login_with_good_credentials()
        reseller_home_view.wait_for_view()

    @TestCase(log, run_list)
    def test_101_goto_home(self):
        reseller_view.goto_domains()
        reseller_domains_view.wait_for_view()
        reseller_view.goto_home()
        reseller_home_view.wait_for_view()
        reseller_view.goto_inventory()
        reseller_inventory_view.wait_for_view()
        reseller_view.goto_home()
        reseller_home_view.wait_for_view()

    @TestCase(log, run_list)
    def test_102_goto_domains(self):
        reseller_view.goto_home()
        reseller_home_view.wait_for_view()
        reseller_view.goto_domains()
        reseller_domains_view.wait_for_view()
        reseller_view.goto_inventory()
        reseller_inventory_view.wait_for_view()
        reseller_view.goto_domains()
        reseller_domains_view.wait_for_view()

    @TestCase(log, run_list)
    def test_103_goto_inventory(self):
        reseller_view.goto_home()
        reseller_home_view.wait_for_view()
        reseller_view.goto_inventory()
        reseller_inventory_view.wait_for_view()
        reseller_view.goto_inventory()
        reseller_inventory_view.wait_for_view()
        reseller_view.goto_inventory()
        reseller_inventory_view.wait_for_view()
