import lib.common.logging_esi as logging_esi
logging_esi.console_handler.setLevel(logging_esi.INFO)
log = logging_esi.get_logger('esi.cron')
with logging_esi.msg_src_cm('importing modules'):
    import unittest
    from ccd.views.base import base_view
    from ccd.views.login import login_view
    from ccd.views.reseller import reseller_view
    from ccd.views.reseller_home import reseller_home_view
    from ccd.views.reseller_domains import reseller_domains_view
    from ccd.views.reseller_inventory import reseller_inventory_view
    from lib.common.wrappers import TestCase

debug = True

class LoginTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        base_view.open_browser()
        base_view.get_portal_url()

    @classmethod
    def tearDownClass(cls):
        base_view.close_browser()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_001_login_check_version(self):
        login_view.login_with_good_credentials()
        reseller_home_view.wait_for_page_title()
        reseller_home_view.version_should_be_correct()
        reseller_home_view.logout()
        login_view.wait_for_page_title()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_002_login_bad_password(self):
        login_view.login_bad_password()
        login_view.wait_for_password_alert()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_003_login_no_password(self):
        login_view.login_no_password()
        login_view.wait_for_password_alert()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_004_login_bad_username(self):
        login_view.login_bad_username()
        login_view.wait_for_password_alert()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_005_login_no_username(self):
        login_view.login_no_username()
        login_view.wait_for_password_alert()


class ResellerTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        base_view.open_browser()

    @classmethod
    def tearDownClass(cls):
        base_view.close_browser()

    def setUp(self):
        base_view.get_portal_url()
        login_view.login_with_good_credentials()
        reseller_home_view.wait_for_page_title()

    def tearDown(self):
        reseller_view.logout()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_101_goto_home(self):
        reseller_view.goto_domains()
        reseller_domains_view.wait_for_page_title()
        reseller_view.goto_home()
        reseller_home_view.wait_for_page_title()
        reseller_view.goto_inventory()
        reseller_inventory_view.wait_for_page_title()
        reseller_view.goto_home()
        reseller_home_view.wait_for_page_title()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_102_goto_domains(self):
        reseller_view.goto_home()
        reseller_home_view.wait_for_page_title()
        reseller_view.goto_domains()
        reseller_domains_view.wait_for_page_title()
        reseller_view.goto_inventory()
        reseller_inventory_view.wait_for_page_title()
        reseller_view.goto_domains()
        reseller_domains_view.wait_for_page_title()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_103_goto_inventory(self):
        reseller_view.goto_home()
        reseller_home_view.wait_for_page_title()
        reseller_view.goto_inventory()
        reseller_inventory_view.wait_for_page_title()
        reseller_view.goto_inventory()
        reseller_inventory_view.wait_for_page_title()
        reseller_view.goto_inventory()
        reseller_inventory_view.wait_for_page_title()

    # @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_104_goto_test_domain_quick(self):
        reseller_view.goto_home()
        reseller_home_view.wait_for_page_title()
        reseller_home_view.goto_test_domain_quick()
        pass

    # @unittest.skip('debug')
    @TestCase(log)
    def test_105_goto_test_domain_select(self):
        reseller_view.goto_domains()
        reseller_domains_view.wait_for_page_title()
        reseller_domains_view.goto_test_domain_select()

    # @unittest.skip('debug')
    @TestCase(log)
    def test_106_goto_test_domain_filter(self):
        reseller_view.goto_domains()
        reseller_domains_view.wait_for_page_title()
        reseller_domains_view.goto_test_domain_filter()


class DomainTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        base_view.open_browser()

    @classmethod
    def tearDownClass(cls):
        base_view.close_browser()

    def setUp(self):
        base_view.get_portal_url()
        login_view.login_with_good_credentials()
        reseller_home_view.wait_for_page_title()

    def tearDown(self):
        reseller_view.logout()

    @unittest.skip('debug')
    @TestCase(log)
    def test_101_goto_domain(self):
        reseller_view.goto_domains()
        reseller_domains_view.wait_for_page_title()
        reseller_view.goto_home()
        reseller_home_view.wait_for_page_title()
        reseller_view.goto_inventory()
        reseller_inventory_view.wait_for_page_title()
        reseller_view.goto_home()
        reseller_home_view.wait_for_page_title()

