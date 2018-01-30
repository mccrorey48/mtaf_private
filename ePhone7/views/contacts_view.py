from mtaf import mtaf_logging
from mtaf.trace import Trace
from mtaf.user_exception import UserException as Ux
from mtaf.filters import get_filter

from ePhone7.config.configure import cfg
from ePhone7.lib.utils.get_softphone import get_softphone
from ePhone7.views.user_view import UserView

from time import time, sleep

log = mtaf_logging.get_logger('mtaf.contacts_view')


class ContactsView(UserView):

    locators = {
        "AddMultipleFavorites": {"by": "id", "value": "com.esi_estech.ditto:id/title_text",
                                 "text": "Add Multiple Favorites"},
        "ConfirmButton": {"by": "id", "value": "com.esi_estech.ditto:id/confirm_button"},
        "ContactCallIcon": {"by": "id", "value": "com.esi_estech.ditto:id/call_button"},
        "ContactClose": {"by": "id", "value": "com.esi_estech.ditto:id/bottom_sheet_title_clear_button"},
        "ContactName": {"by": "id", "value": "com.esi_estech.ditto:id/text1"},
        "ContactNumber": {"by": "id", "value": "com.esi_estech.ditto:id/text2"},
        "ContactParent": {"by": "id", "value": "com.esi_estech.ditto:id/contact_list_item_layout"},
        "ContactsList": {"by": "id", "value": "com.esi_estech.ditto:id/contactsList"},
        "Coworkers": {"by": "id", "value": "com.esi_estech.ditto:id/ephone_contacts", "text": "Coworkers"},
        "CorporateContactDetail": {"by": "id", "value": "com.esi_estech.ditto:id/corporate_details_sliding_layout"},
        "EmptyFavoritesList": {"by": "id", "value": "com.esi_estech.ditto:id/empty_view",
                               "text": "No Favorite Contacts Added"},
        "Favorites": {"by": "id", "value": "com.esi_estech.ditto:id/favorites", "text": "Favorites"},
        "FavoriteIndicator": {"by": "id", "value": "com.esi_estech.ditto:id/favorite_indicator"},
        "FirstContactName": {"by": "zpath", "value": "//rv/fl[1]/v/tv[1]"},
        "Groups": {"by": "id", "value": "com.esi_estech.ditto:id/contact_groups", "text": "Groups"},
        "CallButton": {"by": "id", "value": "com.esi_estech.ditto:id/call_button"},
        "Personal": {"by": "id", "value": "com.esi_estech.ditto:id/all_contacts", "text": "Personal"},
        "ScrollHandle": {"by": "id", "value": "com.esi_estech.ditto:id/scroll_handle"},
        "Tab": {"by": "zpath", "value": "//th/rl/fl/ll/ll"}
    }

    def __init__(self):
        super(ContactsView, self).__init__()
        self.tab_names = ('Personal', 'Coworkers', 'Favorites', 'Groups')
        self.png_file_base = 'contacts'
        self.displayed_elems = []
        self.displayed_numbers = []
        self.presence_element_names = ['ContactsList']

    @Trace(log)
    def call_contact_from_list_element(self, list_element):
        softphone = get_softphone()
        softphone.account_info.incoming_response = 200
        icon = self.find_named_sub_element(list_element, 'ContactCallIcon')
        self.wait_for_green_handset_icon(icon)
        self.click_element(icon)
        softphone.wait_for_call_status('call', 20)
        sleep(10)
        softphone.end_call()
        softphone.wait_for_call_status('idle', 20)

    def wait_for_green_handset_icon(self, icon):
        # wait for handset picture to turn green
        timeout = 120
        start_time = time()
        current_time = start_time
        current_color = None
        desired_color = cfg.colors['ContactsView']['handset_online_color'][:-1]
        while current_time - start_time < timeout:
            self.get_screenshot_as_png('call_from_contacts', cfg.test_screenshot_folder)
            current_color = self.get_element_color('call_from_contacts', icon)
            if current_color == desired_color:
                break
            current_time = time()
        else:
            raise Ux('handset icon color is not green (%s) within %s seconds, current color is %s' %
                     (desired_color, timeout, current_color))

    @Trace(log)
    def no_duplicate_numbers(self):
        # to defeat mysterious Appium tendency to retrieve bad element text list (with duplicates
        # of some elements and with others missing, although the list length is correct):
        # this doesn't seem to happen if you wait long enough before getting the elements, so repeat
        # until each element returned from find_named_elements has unique text
        self.displayed_elems = self.find_named_elements('ContactNumber')
        self.displayed_numbers = [elem.text for elem in self.displayed_elems]
        unique_numbers = []
        for number in self.displayed_numbers:
            log.debug('found contact number %s' % number)
            if number not in unique_numbers:
                unique_numbers.append(number)
        return len(unique_numbers) == len(self.displayed_numbers)

    @Trace(log)
    def wait_for_no_duplicate_numbers(self):
        failmsg_fmt = 'contact number list %s not unique'
        self.wait_for_condition_true(self.no_duplicate_numbers,
                                     lambda: failmsg_fmt % repr(self.displayed_numbers), timeout=30)

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
        parents = self.find_named_elements('ContactParent')
        for parent in parents:
            number = self.find_named_sub_element(parent, 'ContactNumber').text
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
        parents = self.find_named_elements('ContactParent')
        for parent in parents:
            number = self.find_named_sub_element(parent, 'ContactNumber').text
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
        prev_shown_numbers_len = 0
        shown_numbers = []
        match_numbers = []
        # get all contacts shown, adding the contact numbers to the "numbers" array
        # if they are in "contacts_group"; then scroll up and repeat
        # until scrolling fails to show new contacts
        while True:
            self.wait_for_no_duplicate_numbers()
            for number in self.displayed_numbers:
                if number not in shown_numbers:
                    shown_numbers.append(number)
                if number in contacts_group and number not in match_numbers:
                    log.debug('adding %s to contact number list' % number)
                    match_numbers.append(number)
            if len(shown_numbers) == prev_shown_numbers_len or len(match_numbers) == len(contacts_group):
                break
            prev_shown_numbers_len = len(shown_numbers)
            self.swipe_up()
        log.debug("%d elements found" % len(match_numbers))
        return match_numbers

    def get_all_fully_visible_contact_list_items(self):
        _list = self.find_named_element('ContactsList')
        parent_elems = self.find_named_elements('ContactParent')
        visible_items = []
        for elem in parent_elems:
            if elem.location["y"] < _list.location["y"]:
                continue
            if elem.location["y"] + elem.size["height"] > _list.location["y"] + _list.size["height"]:
                continue
            name = self.find_named_sub_element(elem, 'ContactName').text
            number = self.find_named_sub_element(elem, 'ContactNumber').text
            icon = self.find_named_sub_element(elem, 'CallButton')
            visible_items.append({'name': name, 'number': number, 'icon': icon})
        return visible_items

    @Trace(log)
    def clear_all_favorites(self):
        # when in multi-edit mode, scroll to the top of the list;
        # clear favorites icon for all contacts shown, then scroll up and repeat
        # until scrolling fails to show contacts not already in the list
        self.scroll_to_top_of_list()
        checked_numbers = []
        right_color = cfg.colors['ContactsView']['multi_favorite_off_color']
        wrong_color = cfg.colors['ContactsView']['multi_favorite_on_color']
        while True:
            displayed_items = self.get_all_fully_visible_contact_list_items()
            self.get_screenshot_as_png('multi_edit', cfg.test_screenshot_folder)
            prev_numbers_len = len(checked_numbers)
            for item in displayed_items:
                if item['number'] not in checked_numbers:
                    color = self.get_element_color_and_count(cfg.screenshot_folder, 'multi_edit', item['icon'])
                    if self.color_match(color, wrong_color):
                        item['icon'].click()
                        self.get_screenshot_as_png('multi_edit', cfg.test_screenshot_folder)
                        color = self.get_element_color_and_count(cfg.screenshot_folder, 'multi_edit', item['icon'])
                        if not self.color_match(color, right_color):
                            raise Ux("Expected color %s to equal %s" % (color, right_color))
                    log.debug('adding %s to checked number list' % item['number'])
                    checked_numbers.append(item['number'])
            if prev_numbers_len == len(checked_numbers):
                break
            self.swipe_up()
        log.debug("%d elements found" % len(checked_numbers))

    @Trace(log)
    def set_all_favorites(self):
        # when in multi-edit mode, scroll to the top of the list;
        # set favorites icon for all contacts shown that are in the user's favorites list,
        # then while not all favorites have been set, scroll up and repeat until all or set,
        # or until scrolling fails to show contacts not already in the list (which raises an exception)
        self.scroll_to_top_of_list()
        checked_numbers = []
        favorites = cfg.site['Users']['R2d2User']['FavoriteContacts'][:]
        while len(favorites):
            displayed_items = self.get_all_fully_visible_contact_list_items()
            self.get_screenshot_as_png('multi_edit', cfg.test_screenshot_folder)
            prev_numbers_len = len(checked_numbers)
            for item in displayed_items:
                if item['number'] not in checked_numbers:
                    if item['number'] in favorites:
                        right_color = cfg.colors['ContactsView']['multi_favorite_on_color']
                        wrong_color = cfg.colors['ContactsView']['multi_favorite_off_color']
                    else:
                        right_color = cfg.colors['ContactsView']['multi_favorite_off_color']
                        wrong_color = cfg.colors['ContactsView']['multi_favorite_on_color']
                    color = self.get_element_color_and_count(cfg.screenshot_folder, 'multi_edit', item['icon'])
                    if self.color_match(color, wrong_color):
                        item['icon'].click()
                        self.get_screenshot_as_png('multi_edit', cfg.test_screenshot_folder)
                        color = self.get_element_color_and_count(cfg.screenshot_folder, 'multi_edit', item['icon'])
                        if not self.color_match(color, right_color):
                            raise Ux("Expected color %s to equal %s" % (color, right_color))
                    if item['number'] in favorites:
                        favorites.remove(item['number'])
                    log.debug('adding %s to checked number list' % item['number'])
                    checked_numbers.append(item['number'])
            if prev_numbers_len == len(checked_numbers):
                break
            self.swipe_up()
        if len(favorites) > 0:
            raise Ux("Contacts %s from favorites list not found in Coworker Contacts" % favorites)
        log.debug("%d elements found" % len(checked_numbers))

    @Trace(log)
    def scroll_to_top_of_list(self):
        frame = self.find_named_element('ContactsList')
        parents = self.find_named_elements("ContactParent", get_filter("within_frame", frame=frame))
        elems = [self.find_named_sub_element(parent, "ContactName") for parent in parents]
        old_names = [el.text for el in elems]
        if len(old_names) < 7:
            return
        while True:
            self.short_press_scroll(elems[0], elems[-1])
            parents = self.find_named_elements("ContactParent", get_filter("within_frame", frame=frame))
            elems = [self.find_named_sub_element(parent, "ContactName") for parent in parents]
            new_name_count = 0
            for name in [el.text for el in elems]:
                if name not in old_names:
                    old_names.append(name)
                    new_name_count += 1
            if new_name_count == 0:
                break

    @Trace(log)
    def verify_contacts_list_test(self, contacts_group_name):
        self.scroll_to_top_of_list()
        contacts_group = cfg.site['Users']['R2d2User'][contacts_group_name]
        # wait for the contact list to appear
        self.find_named_element('FirstContactName', timeout=30)
        numbers = self.get_all_group_contacts(contacts_group)
        self.get_screenshot_as_png('contact_verify_numbers', cfg.test_screenshot_folder)
        err_msg = 'contact numbers %s not equal to group "%s"' % (repr(numbers), contacts_group)
        self.assertEqual(set(numbers), set(contacts_group), err_msg)

    @Trace(log)
    def clear_favorites_from_favorites_list(self):
        while True:
            elems = self.find_named_elements('ContactParent')
            if len(elems) == 0:
                break
            self.click_element(elems[0])
            self.click_named_element('FavoriteIndicator')
            sleep(5)

    def contact_detail_view_visible(self):
        try:
            self.find_named_element('CorporateContactDetail', timeout=5)
        except Ux:
            return False
        return True

    @Trace(log)
    def get_contact_detail_view(self):
        self.wait_for_condition_true(self.contact_detail_view_visible, lambda: 'no contact detail view')

    @Trace(log)
    def add_favorites_from_coworkers(self):
        new_favorites = cfg.site['Users']['R2d2User']['FavoriteContacts'][:]
        # get each contact element containing a name in the new_favorites list
        # and if it is not already a favorite, toggle the favorites selector
        for number in new_favorites:
            self.click_element(self.get_contact_list_element(number))
            # desired_color = cfg.colors['ContactsView']['handset_online_color'][:-1]
            filebase = 'contact_%s' % number
            self.get_screenshot_as_png(filebase, cfg.test_screenshot_folder)
            icon = self.find_named_element('FavoriteIndicator')
            current_color = self.get_element_color(filebase, icon)
            desired_color = cfg.colors['ContactsView']['multi_favorite_on_color'][:-1]
            if current_color != desired_color:
                self.click_element(icon)
            self.click_named_element('ContactClose')

    @Trace(log)
    def toggle_multi_edit(self):
        elems = self.find_named_elements("ContactName")
        if len(elems) == 0:
            raise Ux("No contact name elements found, cannot toggle multi-edit")
        self.long_press(elems[0])
        # if turning on multi-edit, there will be a dialog with Cancel and OK buttons
        if self.element_is_present("AddMultipleFavorites", timeout=5):
            self.click_named_element("ConfirmButton")

    @Trace(log)
    def long_press_first_contact(self):
        elems = self.find_named_elements("ContactName")
        if len(elems) == 0:
            raise Ux("No contact name elements found, cannot toggle multi-edit")
        self.long_press(elems[0])

    @Trace(log)
    def see_multi_edit_dialog(self):
        if not self.element_is_present("AddMultipleFavorites", timeout=5):
            raise Ux("Add Multiple Favorites dialog not present")

    @Trace(log)
    def confirm_multi_edit(self):
        self.click_named_element("ConfirmButton")

    @Trace(log)
    def find_handset_sub_element(self, list_element):
        return self.find_named_sub_element(list_element, 'ContactCallIcon')


contacts_view = ContactsView()
