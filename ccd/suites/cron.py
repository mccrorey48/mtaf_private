from mtaf import mtaf_logging
mtaf_logging.console_handler.setLevel(mtaf_logging.INFO)
log = mtaf_logging.get_logger('mtaf.cron')
with mtaf_logging.msg_src_cm('importing modules'):
    import unittest
    from ccd.views import *
    from mtaf.decorators import TestCase

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
        login_view.login_with_good_credentials()
        reseller_home_view.wait_for_page_title()
        reseller_home_view.version_should_be_correct()
        reseller_home_view.logout()
        login_view.wait_for_page_title()

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


class ResellerTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        base_view.open_browser(browser)
        base_view.get_portal_url()

    @classmethod
    def tearDownClass(cls):
        base_view.close_browser()

    def setUp(self):
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

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_104_goto_test_domain_quick(self):
        reseller_view.goto_home()
        reseller_home_view.wait_for_page_title()
        reseller_home_view.goto_test_domain_quick()
        reseller_home_view.test_domain_message_is_displayed()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_105_goto_test_domain_select(self):
        reseller_view.goto_domains()
        reseller_domains_view.wait_for_page_title()
        reseller_domains_view.goto_test_domain_select()
        reseller_home_view.test_domain_message_is_displayed()

    @unittest.skip('broken')
    @TestCase(log)
    def test_106_goto_test_domain_filter(self):
        reseller_view.goto_domains()
        reseller_domains_view.wait_for_page_title()
        reseller_domains_view.goto_test_domain_filter()
        reseller_home_view.test_domain_message_is_displayed()


class DomainTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        base_view.open_browser(browser)

    @classmethod
    def tearDownClass(cls):
        base_view.close_browser()

    def setUp(self):
        base_view.get_portal_url()
        login_view.login_with_good_credentials()
        reseller_home_view.wait_for_page_title()
        reseller_home_view.goto_test_domain_quick()
        reseller_home_view.test_domain_message_is_displayed()
        domain_home_view.wait_for_page_title()

    def tearDown(self):
        reseller_view.logout()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_201_goto_home(self):
        domain_view.goto_inventory()
        domain_inventory_view.wait_for_page_title()
        domain_inventory_view.goto_home()
        domain_home_view.wait_for_page_title()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_202_goto_users(self):
        domain_home_view.goto_users()
        domain_users_view.wait_for_page_title()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_203_goto_conferences(self):
        domain_home_view.goto_conferences()
        domain_conferences_view.wait_for_page_title()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_204_goto_call_queues(self):
        domain_home_view.goto_call_queues()
        domain_call_queues_view.wait_for_page_title()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_205_goto_inventory(self):
        domain_home_view.goto_inventory()
        domain_inventory_view.wait_for_page_title()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_206_goto_auto_attendants(self):
        domain_home_view.goto_auto_attendants()
        domain_auto_attendants_view.wait_for_page_title()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_207_goto_time_frames(self):
        domain_home_view.goto_time_frames()
        domain_time_frames_view.wait_for_page_title()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_208_goto_music_on_hold(self):
        domain_home_view.goto_music_on_hold()
        domain_music_on_hold_view.wait_for_page_title()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log)
    def test_209_goto_locations(self):
        domain_home_view.goto_locations()
        domain_locations_view.wait_for_page_title()
