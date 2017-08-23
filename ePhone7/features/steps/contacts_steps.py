from behave import *
from ePhone7.views import *
from ePhone7.config.configure import cfg
from lib.wrappers import fake
from lib.user_exception import UserException as Ux
from ePhone7.utils.get_softphone import get_softphone
from time import sleep


@step("[contacts] a check mark appears in the box")
@fake
def contacts__a_check_mark_appears_in_the_box(context):
    pass


@step("[contacts] a contact detail screen appears with a white star icon")
@fake
def contacts__a_contact_detail_screen_appears_with_a_white_star_icon(context):
    assert contacts_view.contact_detail_view_visible(), "contact detail view is not visible"
    el = contacts_view.find_named_element("FavoriteIndicator")
    base_view.get_screenshot_as_png('contact_detail', cfg.test_screenshot_folder)
    color = contacts_view.get_element_color_and_count('contact_detail', el)
    expect_color = cfg.colors["ContactsView"]["favorite_off_color"]
    assert color == expect_color, "expected color %s, got %s" % (expect_color, color)


@step("[contacts] a contact detail screen appears with a yellow star icon")
@fake
def contacts__a_contact_detail_screen_appears_with_a_yellow_star_icon(context):
    pass


@step("[contacts] a Create New Group popup appears")
@fake
def contacts__a_create_new_group_popup_appears(context):
    pass


@step("[contacts] a Google login screen appears")
@fake
def contacts__a_google_login_screen_appears(context):
    pass


@step("[contacts] Add and Delete buttons are not visible")
@fake
def contacts__add_and_delete_buttons_are_not_visible(context):
    pass


@step("[contacts] Add and Delete buttons are visible")
@fake
def contacts__add_and_delete_buttons_are_visible(context):
    pass


@step('[contacts] An "Add Multiple Favorites" confirmation dialog appears')
@fake
def contacts__an_add_multiple_favorites_confirmation_dialog_appears(context):
    contacts_view.see_multi_edit_dialog()


@step("[contacts] Any existing Favorite contacts have a yellow star icon")
@fake
def contacts__any_existing_favorite_contacts_have_a_yellow_star_icon(context):
    pass


@step("[contacts] Any other contacts have a white star icon")
@fake
def contacts__any_other_contacts_have_a_white_star_icon(context):
    pass


@step("[contacts] I close the contact detail screen")
@fake
def contacts__i_close_the_contact_detail_screen(context):
    pass


@step("[contacts] I enter a group name")
@fake
def contacts__i_enter_a_group_name(context):
    pass


@step("[contacts] I enter my Google user id and password")
@fake
def contacts__i_enter_my_google_user_id_and_password(context):
    pass


@step("[contacts] I long-press a contact list item")
@fake
def contacts__i_longpress_a_contact_list_item(context):
    contacts_view.long_press_first_contact()


@step("[contacts] I see the Personal, Coworkers, Favorites and Groups tabs")
@fake
def contacts__i_see_the_personal_coworkers_favorites_and_groups_tabs(context):
    assert contacts_view.element_is_present('Personal')
    assert contacts_view.element_is_present('Coworkers')
    assert contacts_view.element_is_present('Favorites')
    assert contacts_view.element_is_present('Groups')


@step("[contacts] I touch a check a box next to a contact")
@fake
def contacts__i_touch_a_check_a_box_next_to_a_contact(context):
    pass


@step("[contacts] I touch the Favorites star icon on some contacts")
@fake
def contacts__i_touch_the_favorites_star_icon_on_some_contacts(context):
    pass


@step("[contacts] I touch the handset icon next to the contact I want to call")
@fake
def contacts__i_touch_the_handset_icon_next_to_the_contact_i_want_to_call(context):
    context.handset_icon.click()


@step("[contacts] I touch the name of a contact")
@fake
def contacts__i_touch_the_name_of_a_contact(context):
    pass


@step("[contacts] I touch the name of a Coworker contact that is not a Favorite")
@fake
def contacts__i_touch_the_name_of_a_coworker_contact_that_is_not_a_favorite(context):
    coworker_contacts = cfg.site["Users"]["R2d2User"]["CoworkerContacts"]
    favorite_contacts = cfg.site["Users"]["R2d2User"]["FavoriteContacts"]
    other_contacts = [contact for contact in coworker_contacts if contact not in favorite_contacts]
    context.new_favorite = other_contacts[0]
    contacts_view.touch_element_with_text(context.new_favorite)


@step("[contacts] I touch the name of a personal Group list")
@fake
def contacts__i_touch_the_name_of_a_personal_group_list(context):
    pass


@step("[contacts] I touch the name of a system Group list")
@fake
def contacts__i_touch_the_name_of_a_system_group_list(context):
    pass


@step("[contacts] I touch the star icon")
@fake
def contacts__i_touch_the_star_icon(context):
    contacts_view.click_named_element('FavoriteIndicator')


@step("[contacts] I touch the star icons so all are white")
@fake
def contacts__i_touch_the_star_icons_so_all_are_white(context):
    contacts_view.clear_all_favorites()


@step("[contacts] I touch the star icons so Favorites are yellow and others are white")
@fake
def contacts__i_touch_the_star_icons_so_favorites_are_yellow_and_others_are_white(context):
    contacts_view.set_all_favorites()


@step("[contacts] I touch the yellow star icon")
@fake
def contacts__i_touch_the_yellow_star_icon(context):
    pass


@step("[contacts] my Coworker contacts are displayed in a list with checkboxes")
@fake
def contacts__my_coworker_contacts_are_displayed_in_a_list_with_checkboxes(context):
    pass


@step("[contacts] my Coworker contacts are each shown with a Favorites star icon")
@fake
def contacts__my_coworker_contacts_are_each_shown_with_a_favorites_star_icon(context):
    # limit inspection to first 8 contacts because #9, if it exists, will be partly obscured
    contacts_view.scroll_to_top_of_list()
    names = contacts_view.find_named_elements('ContactName')[:8]
    stars = contacts_view.find_named_elements('CallButton')[:8]
    assert len(names) == len(stars), "Expected contact name count (%d) to equal star icon count (%d)" \
                                     % (len(names), len(stars))
    base_view.get_screenshot_as_png('multi_edit', cfg.test_screenshot_folder)
    for i in range(len(names)):
        color = base_view.get_element_color_and_count('multi_edit', stars[i])
        fail_msg = "No favorites icon found for contact name %s" % names[i].text
        assert (base_view.color_match(color, cfg.colors['ContactsView']['multi_favorite_on_color'])
                or base_view.color_match(color, cfg.colors['ContactsView']['multi_favorite_off_color'])), fail_msg


@step("[contacts] my Coworker contacts are each shown with a handset icon")
@fake
def contacts__my_coworker_contacts_are_each_shown_with_a_handset_icon(context):
    # limit inspection to first 8 contacts because #9, if it exists, will be partly obscured
    contacts_view.scroll_to_top_of_list()
    names = contacts_view.find_named_elements('ContactName')[:8]
    call_buttons = contacts_view.find_named_elements('CallButton')[:8]
    assert len(names) == len(call_buttons), "Expected contact name count (%d) to equal star icon count (%d)" \
                                            % (len(names), len(call_buttons))
    context.call_buttons = dict(zip(names, call_buttons))
    base_view.get_screenshot_as_png('multi_edit', cfg.test_screenshot_folder)
    for i in range(len(names)):
        color = base_view.get_element_color_and_count('multi_edit', call_buttons[i])
        fail_msg = "No handset icon found for contact name %s" % names[i].text
        assert (base_view.color_match(color, cfg.colors['ContactsView']['handset_online_color'])
                or base_view.color_match(color, cfg.colors['ContactsView']['handset_offline_color'])
                or base_view.color_match(color, cfg.colors['ContactsView']['handset_dnd_color'])
                or base_view.color_match(color, cfg.colors['ContactsView']['handset_empty_color'])
                or base_view.color_match(color, cfg.colors['ContactsView']['handset_unavailable_color'])), fail_msg


@step("[contacts] my Group Lists are shown on the display")
@fake
def contacts__my_group_lists_are_shown_on_the_display(context):
    pass


@step("[contacts] my {group_name} contacts are shown on the display")
@fake
def contacts__my_groupname_contacts_are_shown_on_the_display(context, group_name):
    valid_groups = ['Coworker', 'Favorite']
    if group_name not in valid_groups:
        raise Ux("expected group name in %s, got %s" % (valid_groups, group_name))
    contacts_group = cfg.site['Users']['R2d2User']['%sContacts' % group_name]
    numbers = contacts_view.get_all_group_contacts(contacts_group)
    assert set(numbers) == set(contacts_group), "expected %s, got %s" % (contacts_group, numbers)


@step("[contacts] my Personal contacts are each listed with a handset icon")
@fake
def contacts__my_personal_contacts_are_each_listed_with_a_handset_icon(context):
    pass


@step("[contacts] my phone calls the contact")
@fake
def contacts__my_phone_calls_the_contact(context):
    context.softphone.wait_for_call_status('call', 20)
    sleep(10)
    context.softphone.end_call()


@step("[contacts] no Coworker contacts are shown on the favorites display")
@fake
def contacts__no_coworker_contacts_are_shown_on_the_favorites_display(context):
    contacts_group = cfg.site['Users']['R2d2User']['CoworkerContacts']
    contacts = contacts_view.get_all_group_contacts(contacts_group)
    assert len(contacts) == 0, "Expected no coworker contacts on the Favorites list, got %s" % contacts


@step("[contacts] the color toggles between yellow and white")
@fake
def contacts__the_color_toggles_between_yellow_and_white(context):
    pass


@step("[contacts] the contact I want to call has a green handset icon")
@fake
def contacts__the_contact_i_want_to_call_has_a_green_handset_icon(context):
    contact_number = cfg.site['Users'][cfg.site['DefaultSoftphoneUser']]['UserId']
    context.softphone = get_softphone()
    context.softphone.set_incoming_response(200)
    list_element = contacts_view.get_contact_list_element(contact_number)
    context.handset_icon = contacts_view.find_handset_sub_element(list_element)
    contacts_view.wait_for_green_handset_icon(context.handset_icon)


@step("[contacts] the contact I want to call is online")
@fake
def contacts__the_contact_i_want_to_call_is_online(context):
    contact_number = cfg.site['Users'][cfg.site['DefaultSoftphoneUser']]['UserId']
    context.softphone = get_softphone()
    context.softphone.set_incoming_response(200)
    list_element = contacts_view.get_contact_list_element(contact_number)
    context.handset_icon = contacts_view.find_handset_sub_element(list_element)


@step("[contacts] the contact is not shown on the contact list for the group")
@fake
def contacts__the_contact_is_not_shown_on_the_contact_list_for_the_group(context):
    pass


@step("[contacts] the contact is not shown on the display")
@fake
def contacts__the_contact_is_not_shown_on_the_display(context):
    pass


@step("[contacts] the contact is shown on the contact list for the group")
@fake
def contacts__the_contact_is_shown_on_the_contact_list_for_the_group(context):
    pass


@step("[contacts] the contact list for the group is displayed")
@fake
def contacts__the_contact_list_for_the_group_is_displayed(context):
    pass


@step("[contacts] the Contacts view appears")
@fake
def contacts__the_contacts_view_appears(context):
    assert contacts_view.element_is_present('ContactsList')


@step("[contacts] the Group list contacts are displayed in a list with checkboxes")
@fake
def contacts__the_group_list_contacts_are_displayed_in_a_list_with_checkboxes(context):
    pass


@step("[contacts] the new favorite contact is shown on the display")
@fake
def contacts__the_new_favorite_contact_is_shown_on_the_display(context):
    contacts_view.element_with_text_is_present(context.new_favorite)


@step("[contacts] the personal group list is shown on the display")
@fake
def contacts__the_personal_group_list_is_shown_on_the_display(context):
    pass


@step("[contacts] the previously added contact is not on the list with checkboxes")
@fake
def contacts__the_previously_added_contact_is_not_on_the_list_with_checkboxes(context):
    pass


@step("[contacts] the star turns {color_name}")
@fake
def contacts__the_star_turns_colorname(context, color_name):
    cfg_color_names = {'white': 'favorite_off_color', 'yellow': 'favorite_on_color'}
    if color_name not in cfg_color_names:
        raise Ux('bad color name %s' % color_name)
    el = contacts_view.find_named_element("FavoriteIndicator")
    expect_color = cfg.colors["ContactsView"][cfg_color_names[color_name]]
    base_view.get_screenshot_as_png('contact_detail', cfg.test_screenshot_folder)
    actual_color = contacts_view.get_element_color_and_count('contact_detail', el)
    assert actual_color == expect_color, "expected color %s, got %s" % (expect_color, actual_color)


