import lib.common.logging_esi as logging_esi
logging_esi.console_handler.setLevel(logging_esi.INFO)
log = logging_esi.get_logger('esi.smoke')
with logging_esi.msg_src_cm('importing modules'):
    import unittest
    from lib.android.actions import Actions
    from lib.common.remote import remote
    from lib.common.configure import cfg
    from selenium.common.exceptions import WebDriverException
    from ePhone7.views.contacts import contacts_view
    from ePhone7.views.history import history_view
    from ePhone7.views.voicemail import voicemail_view
    from ePhone7.views.keypad import keypad_view
    from ePhone7.views.user import user_view
    from ePhone7.views.prefs import prefs_view
    from ePhone7.views.login import login_view
    from ePhone7.views.settings import settings_view
    from ePhone7.views.apps import apps_view
    from ePhone7.views.ephone_storage import ephone_storage_view
    from ePhone7.views.contacts_storage import contacts_storage_view
    from ePhone7.views.tnc import tnc_view
    from lib.common.wrappers import TestCase

run_list = []
# run_list.append('test_030_contact_lists')
# run_list.append('test_040_user_tabs')
# run_list.append('test_050_active_contacts_tabs')
# run_list.append('test_060_active_history_tabs')
# run_list.append('test_070_active_voicemail_tabs')
# run_list.append('test_080_incoming_call_screen')
# run_list.append('test_090_incoming_auto_answer')
# run_list.append('test_100_incoming_answer')
# run_list.append('test_110_incoming_ignore')
# run_list.append('test_120_call_from_contacts')
# run_list.append('test_130_clear_favorites_list')
# run_list.append('test_140_add_favorites')
# run_list.append('test_150_call_from_favorites')
# run_list.append('test_160_call_from_history')
# run_list.append('test_170_call_from_voicemail')
# run_list.append('test_180_call_from_keypad')
run_list.append('test_190_save_voicemail')
run_list.append('test_200_trash_saved_voicemail')
run_list.append('test_210_trash_new_voicemail')
run_list.append('test_220_save_deleted_voicemail')


def except_screenshot(type, value, traceback):
    Actions.get_screenshot_as_png('exception', cfg.test_screenshot_folder)


class SmokeTests(unittest.TestCase):

    actions = Actions()

    @classmethod
    def setUpClass(cls):
        with logging_esi.msg_src_cm('setUpClass'):
            if not cfg.site['Mock']:
                try:
                    # r2d2 bug, app crashes when you are logging in and enter password
                    # so log in manually, and call goto_main_activity with assume_logged_in=True
                    # so it won't run the state machine that logs in
                    cls.goto_main_activity(assume_logged_in=True)
                    cls.classInitialized = True
                except WebDriverException as e:
                    log.info('WebDriverException in setUpClass: ' + e.msg)
                    cls.classInitialized = False

    @classmethod
    def logged_in_start(cls):
        remote.update_remote('main')

    @classmethod
    def goto_main_activity(cls, assume_logged_in=False):
        # webdriver.Remote() normally requires desired_caps with the correct
        # current activity specified or it won't connect to the Appium server.
        #
        # At the start, or when the current activity changes and needs to be
        # verified, we use (default) 'nolaunch' option so we can connect and find
        # the current activity
        #
        # once we know the current activity we run
        # remote.update_remote(<activity name>) to reconnect

        if not assume_logged_in:
            state = 'start'
            while state != 'logged_in':
                remote.update_remote('nolaunch')
                activity_tag = remote.get_current_activity(state)
                log.info("state: %s, activity_tag: %s" % (state, activity_tag))
                remote.update_remote(activity_tag)
                if activity_tag == 'main':
                    state = 'logged_in'
                elif activity_tag == 'login':
                    login_view.login()
                    state = 'test_for_tnc'
                elif activity_tag == 'tnc':
                    tnc_view.accept_tnc()
                    state = 'tnc_accepted'
            cls.actions.assertEqual(state, 'logged_in', 'Program Error: incorrect state')
        remote.update_remote('main')

        #
        # this version of the state machine was used in setUpClass() to log in if
        # necessary, then do a hard-logout/login/accept-tnc to make sure the
        # contact list reloaded for the logged-in user.
        #
        # since r2d2 now has a better logout procedure that clears user data,
        # the hard logout (still the only way to get a tnc screen) has been
        # moved to a test case
        #
        # state = 'start'
        # while state != 'hard_logged_out':
        #     remote.update_remote('nolaunch')
        #     activity_tag = remote.get_current_activity(state)
        #     log.info("state: %s, activity_tag: %s" % (state, activity_tag))
        #     remote.update_remote(activity_tag)
        #     if state == 'start':
        #         if activity_tag == 'login':
        #             login_view.login()
        #             state = 'logged_in'
        #         elif activity_tag == 'tnc':
        #             tnc_view.accept_tnc()
        #             state = 'tnc_accepted'
        #         elif activity_tag == 'main':
        #             cls.hard_logout()
        #             state = 'hard_logged_out'
        #     elif state == 'logged_in':
        #         if activity_tag == 'tnc':
        #             tnc_view.accept_tnc()
        #             state = 'tnc_accepted'
        #         elif activity_tag == 'main':
        #             cls.hard_logout()
        #             state = 'hard_logged_out'
        #     elif state == 'tnc_accepted':
        #         cls.hard_logout()
        #         state = 'hard_logged_out'
        # cls.actions.assertEqual(state, 'hard_logged_out', 'Program Error: incorrect state')
        # remote.update_remote('login')
        # login_view.login()
        # remote.update_remote('tnc')
        # tnc_view.accept_tnc()
        # remote.update_remote('main')

    @classmethod
    def soft_logout(cls):
        user_view.goto_prefs()
        prefs_view.logout()
        prefs_view.logout_confirm()
        remote.update_remote('login')

    @classmethod
    def hard_logout(cls):
        contacts_view.goto_settings()
        settings_view.goto_apps()
        apps_view.goto_all_apps()
        apps_view.goto_ephone_storage()
        ephone_storage_view.delete_data()
        ephone_storage_view.goto_apps()
        apps_view.goto_settings()
        settings_view.goto_apps()
        apps_view.goto_all_apps()
        apps_view.goto_contacts_storage()
        contacts_storage_view.delete_data()
        contacts_storage_view.goto_apps()
        apps_view.goto_settings()
        remote.update_remote('login')

    @classmethod
    def tearDownClass(cls):
        cls.actions.quit()

    def setUp(self):
        if not cfg.site['Mock']:
            self.assertTrue(self.classInitialized, 'setUpClass() failed, %s not run' % self._testMethodName)

    # # r2d2 bug, app crashes when you are logging in and enter password
    # @TestCase(log, run_list)
    # def test_010_soft_logout_login(self):
    #     self.soft_logout()
    #     login_view.login()
    #     remote.update_remote('main')
    #
    # @TestCase(log, run_list)
    # def test_015_hard_logout_login(self):
    #     self.hard_logout()
    #     login_view.login()
    #     remote.update_remote('tnc')
    #     tnc_view.accept_tnc()
    #     remote.update_remote('main')
    #
    # @TestCase(log, run_list)
    # def test_020_show_registered(self):
    #     pass
    #
    # the verify_contacts_list("FavoriteContacts") call fails because r2d2 does not
    # yet display the favorites for the account

    #
    #        030 - 095 tested with 0.16.2 6/7/16
    #
    @TestCase(log, run_list, except_screenshot)
    def test_030_contact_lists(self):
        # works for coworker contacts, need to define requirements and setup for others
        user_view.goto_tab('Contacts')
        # contacts_view.goto_tab('Personal')
        # contacts_view.verify_contacts_list('AllContacts')
        contacts_view.goto_tab('Coworkers')
        contacts_view.verify_contacts_list_test('CoworkerContacts')
        # contacts_view.goto_tab('Groups')
        # contacts_view.verify_contacts_list('GroupsContacts')
        # contacts_view.goto_tab('Favorites')
        # contacts_view.verify_contacts_list('FavoriteContacts')

    # # there is currently (2/1/2016) a bug in r2d2 that keeps this from passing
    # # if contacts_view.goto_all() is executed
    # # (clicking the tab when already on the "All" view leaves it in the correct
    # # view, but the "Coworkers" tab is given the "active" color
    @TestCase(log, run_list, except_screenshot)
    def test_040_user_tabs(self):
        user_view.goto_tab('Contacts')
        user_view.goto_tab('History')
        user_view.goto_tab('Voicemail')
        user_view.goto_tab('Keypad')

    @TestCase(log, run_list, except_screenshot)
    def test_050_active_contacts_tabs(self):
        user_view.goto_tab('Contacts')
        contacts_view.goto_tab('Personal')
        contacts_view.goto_tab('Coworkers')
        contacts_view.goto_tab('Favorites')
        contacts_view.goto_tab('Groups')

    @TestCase(log, run_list, except_screenshot)
    def test_060_active_history_tabs(self):
        user_view.goto_tab('History')
        history_view.goto_tab('All')
        history_view.goto_tab('Missed')

    @TestCase(log, run_list, except_screenshot)
    def test_070_active_voicemail_tabs(self):
        user_view.goto_tab('Voicemail')
        voicemail_view.goto_tab('New')
        voicemail_view.goto_tab('Saved')
        voicemail_view.goto_tab('Trash')

    @TestCase(log, run_list, except_screenshot)
    def test_080_incoming_call_screen(self):
        user_view.wait_for_view()
        user_view.goto_prefs()
        prefs_view.set_auto_answer_off()
        prefs_view.exit_prefs()
        user_view.incoming_call_screen_test()

    @TestCase(log, run_list, except_screenshot)
    def test_090_incoming_auto_answer(self):
        user_view.wait_for_view()
        user_view.goto_prefs()
        prefs_view.set_auto_answer()
        prefs_view.exit_prefs()
        user_view.auto_answer_call_test()
        user_view.goto_prefs()
        prefs_view.set_auto_answer_off()
        prefs_view.exit_prefs()

    @TestCase(log, run_list, except_screenshot)
    def test_100_incoming_answer(self):
        user_view.wait_for_view()
        user_view.goto_prefs()
        prefs_view.set_auto_answer_off()
        prefs_view.exit_prefs()
        user_view.answer_call_test()

    @TestCase(log, run_list, except_screenshot)
    def test_110_incoming_ignore(self):
        user_view.wait_for_view()
        user_view.goto_prefs()
        prefs_view.set_auto_answer_off()
        prefs_view.exit_prefs()
        user_view.ignore_call_test()

    @TestCase(log, run_list, except_screenshot)
    def test_120_call_from_contacts(self):
        user_view.wait_for_view()
        user_view.goto_tab('Contacts')
        contacts_view.goto_tab('Coworkers')
        contact_number = cfg.site['Accounts']['SoftphoneUser']['UserId']
        list_element = contacts_view.get_contact_list_element(contact_number)
        contacts_view.call_contact_from_list_element(list_element)

    @TestCase(log, run_list, except_screenshot)
    def test_130_clear_favorites_list(self):
        user_view.wait_for_view()
        user_view.goto_tab('Contacts')
        contacts_view.goto_tab('Favorites')
        contacts_view.clear_favorites()

    @TestCase(log, run_list, except_screenshot)
    def test_140_add_favorites(self):
        user_view.wait_for_view()
        user_view.goto_tab('Contacts')
        contacts_view.goto_tab('Coworkers')
        contacts_view.add_favorites_from_coworkers()

    @TestCase(log, run_list, except_screenshot)
    def test_150_call_from_favorites(self):
        user_view.wait_for_view()
        user_view.goto_tab('Contacts')
        contacts_view.goto_tab('Favorites')
        contact_number = cfg.site['Accounts']['SoftphoneUser']['UserId']
        list_element = contacts_view.get_contact_list_element(contact_number)
        contacts_view.call_contact_from_list_element(list_element)

    @TestCase(log, run_list, except_screenshot)
    def test_160_call_from_history(self):
        user_view.wait_for_view()
        user_view.incoming_call_screen_test()
        user_view.goto_tab('History')
        history_view.goto_tab('All')
        history_view.call_contact_test()

    @TestCase(log, run_list, except_screenshot)
    def test_170_call_from_voicemail(self):
        user_view.goto_tab('Voicemail')
        voicemail_view.goto_tab('New')
        voicemail_view.clear_all_vm()
        voicemail_view.receive_voicemail()
        voicemail_view.get_first_vm()
        voicemail_view.call_first_vm_caller()

    @TestCase(log, run_list, except_screenshot)
    def test_180_call_from_keypad(self):
        user_view.goto_tab('Keypad')
        keypad_view.make_call()

    # run with test_200_delete_save_voicemail for better results
    @TestCase(log, run_list, except_screenshot)
    def test_190_save_voicemail(self):
        user_view.goto_tab('Voicemail')
        voicemail_view.goto_tab('New')
        voicemail_view.clear_all_vm()
        voicemail_view.receive_voicemail()
        voicemail_view.get_first_vm_parent().click()
        voicemail_view.save_first_vm_vals()
        voicemail_view.save_voicemail()
        voicemail_view.goto_tab('Saved')
        voicemail_view.verify_first_vm()

    @TestCase(log, run_list, except_screenshot)
    def test_200_trash_saved_voicemail(self):
        user_view.goto_tab('Voicemail')
        voicemail_view.goto_tab('Saved')
        voicemail_view.get_first_vm_parent().click()
        voicemail_view.save_first_vm_vals()
        voicemail_view.delete_voicemail()
        voicemail_view.goto_tab('Trash')
        voicemail_view.verify_first_vm()

    # run with test_220_save_deleted_voicemail for better results
    @TestCase(log, run_list, except_screenshot)
    def test_210_trash_new_voicemail(self):
        user_view.goto_tab('Voicemail')
        voicemail_view.goto_tab('New')
        voicemail_view.clear_all_vm()
        voicemail_view.receive_voicemail()
        voicemail_view.get_first_vm_parent().click()
        voicemail_view.save_first_vm_vals()
        voicemail_view.delete_voicemail()
        voicemail_view.goto_tab('Trash')
        voicemail_view.verify_first_vm()

    @TestCase(log, run_list, except_screenshot)
    def test_220_save_deleted_voicemail(self):
        user_view.goto_tab('Voicemail')
        voicemail_view.goto_tab('Trash')
        voicemail_view.get_first_vm_parent().click()
        voicemail_view.save_first_vm_vals()
        voicemail_view.save_voicemail()
        voicemail_view.goto_tab('Saved')
        voicemail_view.verify_first_vm()
        voicemail_view.clear_all_vm()

    # @TestCase(log, run_list, except_screenshot)
    # def test_230_contact_search_by_number(self):
    #     pass
    #
    # @TestCase(log, run_list, except_screenshot)
    # def test_240_contact_search_by_name(self):
    #     pass
    #
    # @TestCase(log, run_list, except_screenshot)
    # def test_250_call_forward_busy(self):
    #     pass
    #
    # @TestCase(log, run_list, except_screenshot)
    # def test_260_call_forward_unanswered(self):
    #     pass
    #
    # @TestCase(log, run_list, except_screenshot)
    # def test_270_delete_google_account(self):
    #     pass
    #
    # @TestCase(log, run_list, except_screenshot)
    # def test_280_add_google_account(self):
    #     pass
