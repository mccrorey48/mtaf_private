from ePhone7.views.user import UserView
from lib.android.actions import Actions
import lib.common.logging_esi as logging
from lib.common.user_exception import UserException as Ux
from lib.common.configure import cfg
from lib.common.wrappers import Trace
from lib.softphone.softphone import get_softphone
from time import time, sleep
log = logging.get_logger('esi.contacts_view')


class ContactsView(UserView):

    @Trace(log)
    def __init__(self):
        UserView.__init__(self)
        self.actions = Actions(self)
        self.tab_names = ('Personal', 'Coworkers', 'Favorites', 'Groups')
        self.png_file_base = 'contacts'
        self.displayed_elems = []
        self.displayed_numbers = []

    @Trace(log)
    def call_contact_from_list_element(self, list_element):
        softphone = get_softphone()
        icon = self.actions.find_sub_element_by_key(list_element, 'ContactCallIcon')
        # wait for handset picture to turn green
        timeout = 20
        start_time = time()
        current_time = start_time
        desired_color = cfg.colors['ContactsView']['handset_online_color'][:-1]
        while current_time - start_time < timeout:
            self.actions.get_screenshot_as_png('call_from_contacts', cfg.test_screenshot_folder)
            current_color = self.actions.get_element_color('call_from_contacts', icon)
            if current_color == desired_color:
                break
            current_time = time()
        else:
            log.warn('handset icon color is not green (%s) within %s seconds, current color is %s' %
                         (desired_color, timeout, current_color))
        icon.click()
        softphone.wait_for_call_status('start', 20)
        sleep(10)
        self.actions.click_element_by_key('EndActiveCall')
        softphone.wait_for_call_status('end', 20)

    @Trace(log)
    def no_duplicate_numbers(self):
        # to defeat mysterious Appium tendency to retrieve bad element text list (with duplicates
        # of some elements and with others missing, although the list length is correct):
        # this doesn't seem to happen if you wait long enough before getting the elements, so repeat
        # until each element returned from find_elements_by_key has unique text
        self.displayed_elems = self.actions.find_elements_by_key('ContactNumber')
        self.displayed_numbers = [elem.text for elem in self.displayed_elems]
        unique_numbers = []
        for number in self.displayed_numbers:
            log.debug('found contact number %s' % number)
            if number not in unique_numbers:
                unique_numbers.append(number)
        return len(unique_numbers) == len(self.displayed_numbers)

    @Trace(log)
    def wait_for_no_duplicate_numbers(self):
        failmsg_fmt = 'failed to get unique contact number list, last list was %s'
        self.actions.wait_for_condition_true(self.no_duplicate_numbers,
                                             lambda: failmsg_fmt % repr(self.displayed_numbers), 30)

    @Trace(log)
    def get_contact_list_element(self, contact_number):
        # start at the top of the contact list
        self.scroll_to_top_of_list()
        # get the desired contact on the screen by scrolling if necessary
        prev_numbers_len = 0
        numbers = []
        while True:
            self.wait_for_no_duplicate_numbers()
            # if the contact_number is on the display, break the while loop and don't scroll anymore
            if contact_number in self.displayed_numbers:
                break
            # otherwise add to the list of numbers already seen
            for number in self.displayed_numbers:
                if number not in numbers:
                    numbers.append(number)
            # if len(numbers) is unchanged, all numbers have been checked
            # and the desired number was not found
            if len(numbers) == prev_numbers_len:
                raise Ux('contact number %s not found[1]' % contact_number)
            prev_numbers_len = len(numbers)
            self.swipe_up()

        # get the parent elements from the screen and find the one that contains contact_number
        parents = self.actions.find_elements_by_key('ContactParent')
        for parent in parents:
            number = self.actions.find_sub_element_by_key(parent, 'ContactNumber').text
            log.debug('<%s> subelement ContactNumber text = %s' % (parent.id, number))
            if number == contact_number:
                break
        else:
            # it was on the screen before, it should be a subelement of one of the parent elememts;
            # so if not, what happened? erratic Appium behavior happened
            raise Ux('contact number %s not found[2]' % contact_number)

        # just in case the handset icon is partly obscured by the top or bottom borders of the list,
        # move it to the center
        self.swipe_elem_to_center(parent)

        # repeat getting the parent elements and finding the one with the right subelement
        # now that we're pretty sure it's near the center of the screen
        self.wait_for_no_duplicate_numbers()
        parents = self.actions.find_elements_by_key('ContactParent')
        for parent in parents:
            number = self.actions.find_sub_element_by_key(parent, 'ContactNumber').text
            log.debug('<%s> subelement ContactNumber text = %s' % (parent.id, number))
            if number == contact_number:
                break
        else:
            raise Ux('contact number %s not found[3]' % contact_number)

        # this should be the droid parent we are looking for
        return parent

    @Trace(log)
    def get_all_group_contacts(self, contacts_group):
        self.scroll_to_top_of_list()
        prev_numbers_len = 0
        numbers = []
        # get all contacts shown, then scroll up and repeat
        # until scrolling fails to show contacts not already in the list
        while True:
            self.wait_for_no_duplicate_numbers()
            for number in self.displayed_numbers:
                if number in contacts_group and number not in numbers:
                    log.debug('adding %s to contact number list' % number)
                    numbers.append(number)
            if len(numbers) == prev_numbers_len or len(numbers) == len(contacts_group):
                break
            prev_numbers_len = len(numbers)
            self.swipe_up()
        log.debug("%d elements found" % len(numbers))
        return numbers

    @Trace(log)
    def scroll_to_top_of_list(self):
        self.actions.tap(560, 210, duration=1000)
        sleep(2)

    @Trace(log)
    def verify_contacts_list_test(self, contacts_group_name):
        self.scroll_to_top_of_list()
        contacts_group = cfg.site['Accounts']['R2d2User'][contacts_group_name]
        # wait for the contact list to appear
        self.actions.find_element_by_key('FirstContactName', timeout=30)
        numbers = self.get_all_group_contacts(contacts_group)
        self.actions.get_screenshot_as_png('contact_verify_numbers', cfg.test_screenshot_folder)
        err_msg = 'contact numbers %s not equal to group "%s"' % (repr(numbers), contacts_group)
        self.actions.assertEqual(set(numbers), set(contacts_group), err_msg)

    @Trace(log)
    def clear_favorites(self):
        while True:
            elems = self.actions.find_elements_by_key('ContactParent')
            if len(elems) == 0:
                break
            elems[0].click()
            self.actions.find_element_by_key('FavoriteIndicator').click()
            sleep(5)

    def contact_detail_view_visible(self):
        try:
            self.actions.find_element_by_key('FavoriteIndicator', timeout=5)
        except Ux:
            return False
        return True

    @Trace(log)
    def get_contact_detail_view(self):
        self.actions.wait_for_condition_true(self.contact_detail_view_visible,
                                             lambda: 'contact detail view failed to become visible')

    @Trace(log)
    def add_favorites_from_coworkers(self):
        new_favorites = cfg.site['Accounts']['R2d2User']['FavoriteContacts'][:]
        # get each contact element containing a name in the new_favorites list
        # and if it is not already a favorite, toggle the favorites selector
        for number in new_favorites:
            self.get_contact_list_element(number).click()
            # desired_color = cfg.colors['ContactsView']['handset_online_color'][:-1]
            filebase = 'contact_%s' %  number
            self.actions.get_screenshot_as_png(filebase, cfg.test_screenshot_folder)
            icon = self.actions.find_element_by_key('FavoriteIndicator')
            current_color = self.actions.get_element_color(filebase, icon)
            desired_color = cfg.colors['ContactsView']['favorite_on_color'][:-1]
            if current_color != desired_color:
                icon.click()
            self.actions.find_element_by_key('ContactClose').click()


contacts_view = ContactsView()
