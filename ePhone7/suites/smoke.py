import lib.common.logging_esi as logging_esi
logging_esi.console_handler.setLevel(logging_esi.INFO)
log = logging_esi.get_logger('esi.smoke')
with logging_esi.msg_src_cm('importing modules'):
    import unittest
    from lib.android.actions import Actions
    from ePhone7.utils.configure import cfg
    from ePhone7.views.base import base_view
    from ePhone7.views.contacts import contacts_view
    from ePhone7.views.history import history_view
    from ePhone7.views.voicemail import voicemail_view
    from ePhone7.views.keypad import keypad_view
    from ePhone7.views.user import user_view
    from ePhone7.views.prefs import prefs_view
    from lib.common.wrappers import TestCase

debug = True
no_favorites = True


def except_screenshot(type, value, traceback):
    Actions.get_screenshot_as_png('exception', cfg.test_screenshot_folder)


class SmokeTests(unittest.TestCase):

    @classmethod
    def tearDownClass(cls):
        base_view.actions.quit()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log, except_cb=except_screenshot)
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

    # @unittest.skipIf(debug, 'debug')
    @TestCase(log, except_cb=except_screenshot)
    def test_040_user_tabs(self):
        user_view.goto_tab('Contacts')
        user_view.goto_tab('History')
        user_view.goto_tab('Voicemail')
        user_view.goto_tab('Keypad')

    @unittest.skipIf(debug, 'debug')
    @TestCase(log, except_cb=except_screenshot)
    def test_050_active_contacts_tabs(self):
        user_view.goto_tab('Contacts')
        contacts_view.goto_tab('Personal')
        contacts_view.goto_tab('Coworkers')
        contacts_view.goto_tab('Favorites')
        contacts_view.goto_tab('Groups')

    @unittest.skipIf(debug, 'debug')
    @TestCase(log, except_cb=except_screenshot)
    def test_060_active_history_tabs(self):
        user_view.goto_tab('History')
        history_view.goto_tab('All')
        history_view.goto_tab('Missed')

    @unittest.skipIf(debug, 'debug')
    @TestCase(log, except_cb=except_screenshot)
    def test_070_active_voicemail_tabs(self):
        user_view.goto_tab('Voicemail')
        voicemail_view.goto_tab('New')
        voicemail_view.goto_tab('Saved')
        voicemail_view.goto_tab('Trash')

    @unittest.skipIf(debug, 'debug')
    @TestCase(log, except_cb=except_screenshot)
    def test_080_incoming_call_screen(self):
        user_view.wait_for_view()
        user_view.goto_prefs()
        prefs_view.set_auto_answer_off()
        prefs_view.exit_prefs()
        user_view.incoming_call_screen_test()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log, except_cb=except_screenshot)
    def test_090_incoming_auto_answer(self):
        user_view.wait_for_view()
        user_view.goto_prefs()
        prefs_view.set_auto_answer()
        prefs_view.exit_prefs()
        user_view.auto_answer_call_test()
        user_view.goto_prefs()
        prefs_view.set_auto_answer_off()
        prefs_view.exit_prefs()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log, except_cb=except_screenshot)
    def test_100_incoming_answer(self):
        user_view.wait_for_view()
        user_view.goto_prefs()
        prefs_view.set_auto_answer_off()
        prefs_view.exit_prefs()
        user_view.answer_call_test()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log, except_cb=except_screenshot)
    def test_110_incoming_ignore(self):
        user_view.wait_for_view()
        user_view.goto_prefs()
        prefs_view.set_auto_answer_off()
        prefs_view.exit_prefs()
        user_view.ignore_call_test()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log, except_cb=except_screenshot)
    def test_120_call_from_contacts(self):
        user_view.wait_for_view()
        user_view.goto_tab('Contacts')
        contacts_view.goto_tab('Coworkers')
        contact_number = cfg.site['Accounts'][cfg.site['DefaultSoftphoneUser']]['UserId']
        list_element = contacts_view.get_contact_list_element(contact_number)
        contacts_view.call_contact_from_list_element(list_element)

    @unittest.skipIf(debug or no_favorites, 'debug')
    @TestCase(log, except_cb=except_screenshot)
    def test_130_clear_favorites_list(self):
        user_view.wait_for_view()
        user_view.goto_tab('Contacts')
        contacts_view.goto_tab('Favorites')
        contacts_view.clear_favorites()

    @unittest.skipIf(debug or no_favorites, 'debug')
    @TestCase(log, except_cb=except_screenshot)
    def test_140_add_favorites(self):
        user_view.wait_for_view()
        user_view.goto_tab('Contacts')
        contacts_view.goto_tab('Coworkers')
        contacts_view.add_favorites_from_coworkers()

    @unittest.skipIf(debug or no_favorites, 'debug')
    @TestCase(log, except_cb=except_screenshot)
    def test_150_call_from_favorites(self):
        user_view.wait_for_view()
        user_view.goto_tab('Contacts')
        contacts_view.goto_tab('Favorites')
        contact_number = cfg.site['Accounts'][cfg.site['DefaultSoftphoneUser']]['UserId']
        list_element = contacts_view.get_contact_list_element(contact_number)
        contacts_view.call_contact_from_list_element(list_element)

    @unittest.skipIf(debug, 'debug')
    @TestCase(log, except_cb=except_screenshot)
    def test_160_call_from_history(self):
        user_view.wait_for_view()
        user_view.incoming_call_screen_test()
        user_view.goto_tab('History')
        history_view.goto_tab('All')
        history_view.call_contact_test()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log, except_cb=except_screenshot)
    def test_170_call_from_voicemail(self):
        user_view.goto_tab('Voicemail')
        voicemail_view.goto_tab('New')
        voicemail_view.clear_all_vm()
        voicemail_view.receive_voicemail()
        voicemail_view.open_first_vm()
        voicemail_view.call_first_vm_caller()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log, except_cb=except_screenshot)
    def test_180_call_from_keypad(self):
        user_view.goto_tab('Keypad')
        keypad_view.make_call()

    # run with test_200_delete_save_voicemail for better results
    @unittest.skipIf(debug, 'debug')
    @TestCase(log, except_cb=except_screenshot)
    def test_190_save_new_voicemail(self):
        self.save_new_voicemail()

    def save_new_voicemail(self):
        user_view.goto_tab('Voicemail')
        voicemail_view.goto_tab('Saved')
        voicemail_view.clear_all_vm()
        voicemail_view.goto_tab('New')
        voicemail_view.clear_all_vm()
        voicemail_view.receive_voicemail()
        voicemail_view.open_first_vm()
        voicemail_view.save_first_vm_vals()
        voicemail_view.save_voicemail_button()
        voicemail_view.goto_tab('Saved')
        voicemail_view.verify_first_vm()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log, except_cb=except_screenshot)
    def test_200_trash_saved_voicemail(self):
        user_view.goto_tab('Voicemail')
        voicemail_view.goto_tab('Saved')
        voicemail_view.clear_all_vm()
        voicemail_view.goto_tab('New')
        voicemail_view.clear_all_vm()
        voicemail_view.receive_voicemail()
        voicemail_view.open_first_vm()
        voicemail_view.save_first_vm_vals()
        voicemail_view.save_voicemail_button()
        voicemail_view.goto_tab('Saved')
        voicemail_view.verify_first_vm()
        voicemail_view.open_first_vm()
        voicemail_view.save_first_vm_vals()
        voicemail_view.delete_voicemail_button()
        voicemail_view.goto_tab('Trash')
        voicemail_view.verify_first_vm()

    # run with test_220_save_deleted_voicemail for better results
    @unittest.skipIf(debug, 'debug')
    @TestCase(log, except_cb=except_screenshot)
    def test_210_trash_new_voicemail(self):
        user_view.goto_tab('Voicemail')
        voicemail_view.goto_tab('New')
        voicemail_view.clear_all_vm()
        voicemail_view.receive_voicemail()
        voicemail_view.open_first_vm()
        voicemail_view.save_first_vm_vals()
        voicemail_view.delete_voicemail_button()
        voicemail_view.goto_tab('Trash')
        voicemail_view.verify_first_vm()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log, except_cb=except_screenshot)
    def test_220_save_deleted_voicemail(self):
        user_view.goto_tab('Voicemail')
        voicemail_view.goto_tab('Saved')
        voicemail_view.clear_all_vm()
        #
        # technically the commented lines should be run to make this work as a standalone test case,
        # but since trash is usually going to be full of messages from previous runs, it's a waste
        # of time - unless somehow the trash is empty when it is run standalone
        #
        # voicemail_view.goto_tab('New')
        # voicemail_view.clear_all_vm()
        # voicemail_view.receive_voicemail()
        # voicemail_view.open_first_vm()
        # voicemail_view.save_first_vm_vals()
        # voicemail_view.delete_voicemail_button()
        voicemail_view.goto_tab('Trash')
        # voicemail_view.verify_first_vm()
        voicemail_view.open_first_vm()
        voicemail_view.save_first_vm_vals()
        voicemail_view.save_voicemail_button()
        voicemail_view.goto_tab('Saved')
        voicemail_view.verify_first_vm()
        voicemail_view.clear_all_vm()

    @unittest.skipIf(debug, 'debug')
    @TestCase(log, except_cb=except_screenshot)
    def test_230_forward_new_voicemail(self):
        user_view.goto_tab('Voicemail')
        voicemail_view.goto_tab('New')
        voicemail_view.clear_all_vm()
        voicemail_view.receive_voicemail()
        voicemail_view.open_first_vm()
        voicemail_view.save_first_vm_vals()
        voicemail_view.forward_voicemail_button()
        voicemail_view.forward_voicemail()
        # need a way to verify the forward

    @unittest.skipIf(debug, 'debug')
    @TestCase(log, except_cb=except_screenshot)
    def test_240_forward_saved_voicemail(self):
        self.save_new_voicemail()
        user_view.goto_tab('Voicemail')
        voicemail_view.goto_tab('Saved')
        voicemail_view.clear_all_vm()
        voicemail_view.goto_tab('New')
        voicemail_view.clear_all_vm()
        voicemail_view.receive_voicemail()
        voicemail_view.open_first_vm()
        voicemail_view.save_first_vm_vals()
        voicemail_view.save_voicemail_button()
        voicemail_view.goto_tab('Saved')
        voicemail_view.open_first_vm()
        voicemail_view.forward_voicemail_button()
        voicemail_view.forward_voicemail()
        # need a way to verify the forward

    # #function disable for the moment
    # @unittest.skipIf(debug, 'debug')
    # @TestCase(log)
    # def test_250_share_voicemail(self):

    # @unittest.skipIf(debug, 'debug')
    # @TestCase(log, except_cb=except_screenshot)
    # def test_230_contact_search_by_number(self):
    #     pass
    #
    # @unittest.skipIf(debug, 'debug')
    # @TestCase(log, except_cb=except_screenshot)
    # def test_240_contact_search_by_name(self):
    #     pass
    #
    # @unittest.skipIf(debug, 'debug')
    # @TestCase(log, except_cb=except_screenshot)
    # def test_250_call_forward_busy(self):
    #     pass
    #
    # @unittest.skipIf(debug, 'debug')
    # @TestCase(log, except_cb=except_screenshot)
    # def test_260_call_forward_unanswered(self):
    #     pass
    #
    # @unittest.skipIf(debug, 'debug')
    # @TestCase(log, except_cb=except_screenshot)
    # def test_270_delete_google_account(self):
    #     pass
    #
    # @unittest.skipIf(debug, 'debug')
    # @TestCase(log, except_cb=except_screenshot)
    # def test_280_add_google_account(self):
    #     pass
