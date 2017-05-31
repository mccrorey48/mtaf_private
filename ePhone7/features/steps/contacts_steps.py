from behave import *
from ePhone7.views import *
from ePhone7.config.configure import cfg
from lib.wrappers import fake


@step("[contacts] a check mark appears in the box")
def contacts__a_check_mark_appears_in_the_box(context):
    pass


@step("[contacts] a contact detail screen appears with a white star icon")
def contacts__a_contact_detail_screen_appears_with_a_white_star_icon(context):
    pass


@step("[contacts] a contact detail screen appears with a yellow star icon")
def contacts__a_contact_detail_screen_appears_with_a_yellow_star_icon(context):
    pass


@step("[contacts] a Create New Group popup appears")
def contacts__a_create_new_group_popup_appears(context):
    pass


@step("[contacts] a Google login screen appears")
def contacts__a_google_login_screen_appears(context):
    pass


@step("[contacts] Add and Delete buttons are not visible")
def contacts__add_and_delete_buttons_are_not_visible(context):
    pass


@step("[contacts] Add and Delete buttons are visible")
def contacts__add_and_delete_buttons_are_visible(context):
    pass


@step('[contacts] An "Add Multiple Favorites" confirmation dialog appears')
def contacts__an_add_multiple_favorites_confirmation_dialog_appears(context):
    pass


@step("[contacts] Any existing Favorite contacts have a yellow start icon")
def contacts__any_existing_favorite_contacts_have_a_yellow_start_icon(context):
    pass


@step("[contacts] Any other contacts have a white start icon")
def contacts__any_other_contacts_have_a_white_start_icon(context):
    pass


@step("[contacts] I close the contact detail screen")
def contacts__i_close_the_contact_detail_screen(context):
    pass


@step("[contacts] I enter a group name")
def contacts__i_enter_a_group_name(context):
    pass


@step("[contacts] I enter my Google user id and password")
def contacts__i_enter_my_google_user_id_and_password(context):
    pass


@step("[contacts] I go to the Personal tab")
@fake
def contacts__i_go_to_the_personal_tab(context):
    contacts_view.goto_tab('Personal')


@step("[contacts] I long-press a contact list item")
def contacts__i_longpress_a_contact_list_item(context):
    pass


@step("[contacts] I see the Personal, Coworkers, Favorites and Groups tabs")
@fake
def contacts__i_see_the_personal_coworkers_favorites_and_groups_tabs(context):
    assert contacts_view.element_is_present('Personal')
    assert contacts_view.element_is_present('Coworkers')
    assert contacts_view.element_is_present('Favorites')
    assert contacts_view.element_is_present('Groups')


@step("[contacts] I touch a check a box next to a contact")
def contacts__i_touch_a_check_a_box_next_to_a_contact(context):
    pass


@step('[contacts] I touch "OK"')
def contacts__i_touch_ok(context):
    pass


@step("[contacts] I touch the Add button")
def contacts__i_touch_the_add_button(context):
    pass


@step("[contacts] I touch the Coworkers tab")
@fake
def contacts__i_touch_the_coworkers_tab(context):
    contacts_view.goto_tab('Coworkers')


@step("[contacts] I touch the Create button")
def contacts__i_touch_the_create_button(context):
    pass


@step("[contacts] I touch the Delete button")
def contacts__i_touch_the_delete_button(context):
    pass


@step("[contacts] I touch the Done button")
def contacts__i_touch_the_done_button(context):
    pass


@step("[contacts] I touch the Favorites star icon on some contacts")
def contacts__i_touch_the_favorites_star_icon_on_some_contacts(context):
    pass


@step("[contacts] I touch the Favorites tab")
def contacts__i_touch_the_favorites_tab(context):
    pass


@step("[contacts] I touch the Groups tab")
def contacts__i_touch_the_groups_tab(context):
    pass


@step("[contacts] I touch the handset icon")
def contacts__i_touch_the_handset_icon(context):
    pass


@step("[contacts] I touch the name of a contact")
def contacts__i_touch_the_name_of_a_contact(context):
    pass


@step("[contacts] I touch the name of a contact that is not a Favorite")
def contacts__i_touch_the_name_of_a_contact_that_is_not_a_favorite(context):
    pass


@step("[contacts] I touch the name of a personal Group list")
def contacts__i_touch_the_name_of_a_personal_group_list(context):
    pass


@step("[contacts] I touch the name of a system Group list")
def contacts__i_touch_the_name_of_a_system_group_list(context):
    pass


@step('[contacts] I touch the "Personal" tab')
def contacts__i_touch_the_personal_tab(context):
    pass


@step('[contacts] I touch the "Sign in with Google" banner')
@fake
def contacts__i_touch_the_sign_in_with_google_banner(context):
    contacts_view.click_named_element('GoogleSignInBanner')


@step("[contacts] I touch the star icons so Favorites are yellow and others are white")
def contacts__i_touch_the_star_icons_so_favorites_are_yellow_and_others_are_white(context):
    pass


@step("[contacts] I touch the white star icon")
def contacts__i_touch_the_white_star_icon(context):
    pass


@step("[contacts] I touch the yellow star icon")
def contacts__i_touch_the_yellow_star_icon(context):
    pass


@step("[contacts] my Coworker contacts are displayed in a list with checkboxes")
def contacts__my_coworker_contacts_are_displayed_in_a_list_with_checkboxes(context):
    pass


@step("[contacts] my Coworker contacts are each listed with a handset icon")
def contacts__my_coworker_contacts_are_each_listed_with_a_handset_icon(context):
    pass


@step("[contacts] my Coworker contacts are shown on the display")
@fake
def contacts__my_coworker_contacts_are_shown_on_the_display(context):
    contacts_group = cfg.site['Users']['R2d2User']['CoworkerContacts']
    numbers = contacts_view.get_all_group_contacts(contacts_group)
    assert set(numbers) == set(contacts_group), "expected %s, got %s" % (contacts_group, numbers)


@step("[contacts] my Favorite contacts are shown on the display")
def contacts__my_favorite_contacts_are_shown_on_the_display(context):
    pass


@step("[contacts] my Google contacts are shown on the display")
def contacts__my_google_contacts_are_shown_on_the_display(context):
    pass


@step("[contacts] my Group Lists are shown on the display")
def contacts__my_group_lists_are_shown_on_the_display(context):
    pass


@step("[contacts] my Personal contacts are each listed with a handset icon")
def contacts__my_personal_contacts_are_each_listed_with_a_handset_icon(context):
    pass


@step("[contacts] my Personal contacts are shown on the display")
def contacts__my_personal_contacts_are_shown_on_the_display(context):
    pass


@step("[contacts] my phone calls the contact")
def contacts__my_phone_calls_the_contact(context):
    pass


@step("[contacts] my updated Favorite contacts are shown on the display")
def contacts__my_updated_favorite_contacts_are_shown_on_the_display(context):
    pass


@step("[contacts] the color toggles between yellow and white")
def contacts__the_color_toggles_between_yellow_and_white(context):
    pass


@step("[contacts] the contact is not shown on the contact list for the group")
def contacts__the_contact_is_not_shown_on_the_contact_list_for_the_group(context):
    pass


@step("[contacts] the contact is not shown on the display")
def contacts__the_contact_is_not_shown_on_the_display(context):
    pass


@step("[contacts] the contact is shown on the contact list for the group")
def contacts__the_contact_is_shown_on_the_contact_list_for_the_group(context):
    pass


@step("[contacts] the contact is shown on the display")
def contacts__the_contact_is_shown_on_the_display(context):
    pass


@step("[contacts] the contact list for the group is displayed")
def contacts__the_contact_list_for_the_group_is_displayed(context):
    pass


@step("[contacts] the contacts are shown with a Favorites star icon next to each one")
def contacts__the_contacts_are_shown_with_a_favorites_star_icon_next_to_each_one(context):
    pass


@step("[contacts] the Contacts view appears")
@fake
def contacts__the_contacts_view_appears(context):
    assert contacts_view.element_is_present('ContactsList')


@step("[contacts] the Group list contacts are displayed in a list with checkboxes")
def contacts__the_group_list_contacts_are_displayed_in_a_list_with_checkboxes(context):
    pass


@step("[contacts] the personal group list is shown on the display")
def contacts__the_personal_group_list_is_shown_on_the_display(context):
    pass


@step("[contacts] the previously added contact is not on the list with checkboxes")
def contacts__the_previously_added_contact_is_not_on_the_list_with_checkboxes(context):
    pass


@step("[contacts] the star turns white")
def contacts__the_star_turns_white(context):
    pass


@step("[contacts] the star turns yellow")
def contacts__the_star_turns_yellow(context):
    pass


