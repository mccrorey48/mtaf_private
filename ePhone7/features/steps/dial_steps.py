from behave import *
from mtaf import mtaf_logging
from ePhone7.views import *
from ePhone7.config.configure import cfg
from mtaf.user_exception import UserException as Ux

log = mtaf_logging.get_logger('mtaf.dial_steps')


@step("[dial] A list of contacts containing the partial number appears above the keypad")
def dial__a_list_of_contacts_containing_the_partial_number_appears_above_the_keypad(context):
    pass


@step("[dial] A list of Coworker contacts containing the partial name appears above the keypad")
def dial__a_list_of_coworker_contacts_containing_the_partial_name_appears_above_the_keypad(context):
    dial_view.click_element(dial_view.find_named_element("HideDialPad"))
    elems = [elem.text for elem in dial_view.find_named_elements("DialPadContactName")]
    elems2 = [elem2['name'] for elem2 in cfg.site["Users"]["R2d2User"]["CoworkerContacts"]][0:3]
    assert elems == elems2, "expected %s, got %s" % (elems, elems2)


@step("[dial] A list of Coworker contacts containing the partial number appears above the keypad")
def dial__a_list_of_coworker_contacts_containing_the_partial_number_appears_above_the_keypad(context):
    dial_view.click_element(dial_view.find_named_element("HideDialPad"))
    elems = [elem.text for elem in dial_view.find_named_elements("DialPadContactNumber")]
    elems2 = [elem2['number'] for elem2 in cfg.site["Users"]["R2d2User"]["CoworkerContacts"]]
    assert elems == elems2, "expected %s, got %s" % (elems, elems2)


@step("[dial] A list of Personal contacts containing the partial name appears above the keypad")
def dial__a_list_of_personal_contacts_containing_the_partial_name_appears_above_the_keypad(context):
    pass


@step("[dial] A list of Personal contacts containing the partial number appears above the keypad")
def dial__a_list_of_personal_contacts_containing_the_partial_number_appears_above_the_keypad(context):
    pass


@step("[dial] I dial the {code_name} direct code")
def dial__i_dial_the_codename_direct_code(context, code_name):
    dial_view.dial_named_number(code_name)


@step("[dial] I enter a 10-digit phone number using the keypad")
def dial__i_enter_a_10digit_phone_number_using_the_keypad(context):
    context.caller_number = cfg.site["10DigitNumber"]
    dial_view.dial_number(context.caller_number)


@step("[dial] I enter a Coworker contact number using the keypad")
def dial__i_enter_a_coworker_contact_number_using_the_keypad(context):
    context.caller_number = cfg.site["Users"]["R2d2User"]["CoworkerContacts"][0]['number']
    dial_view.dial_number(context.caller_number)


@step("[dial] I enter part of a Coworker contact name using the keypad")
def dial__i_enter_part_of_a_coworker_contact_name_using_the_keypad(context):
    dial_view.dial_number(cfg.site["Users"]["R2d2User"]["CoworkerContactsDialPadName"])
    # search "terA, terB and terC"


@step("[dial] I enter part of a Coworker contact number using the keypad")
def dial__i_enter_part_of_a_coworker_contact_number_using_the_keypad(context):
    dial_view.dial_number(cfg.site["Users"]["R2d2User"]["CoworkerContactsDialPadNumber"])
    # search "220"


@step("[dial] I enter part of a Personal contact name using the keypad")
def dial__i_enter_part_of_a_personal_contact_name_using_the_keypad(context):
    pass


@step("[dial] I enter part of a Personal contact number using the keypad")
def dial__i_enter_part_of_a_personal_contact_number_using_the_keypad(context):
    pass


@step("[dial] I make a call to a coworker contact")
def dial__i_make_a_call_to_a_coworker_contact(context):
    context.softphone = user_view.configure_called_answer_ring()
    dial_view.dial_number(context.softphone.number)
    context.caller_number = context.softphone.number
    dial_view.touch_dial_button()
    context.softphone.wait_for_call_status('early', dial_view.call_status_wait)


@step("[dial] I see the keypad")
def dial__i_see_the_keypad(context):
    assert dial_view.DialPad is not None, "dial_view.DialPad element not present"


@step("[dial] I touch the Call button")
def dial__i_touch_the_call_button(context):
    dial_view.touch_dial_button()


@step("[dial] I touch the contact listing I want to call")
def dial__i_touch_the_contact_listing_i_want_to_call(context):
    dial_view.click_named_element("SearchResultItem1")


@step("[dial] Only the contact I touched is listed")
def dial__only_the_contact_i_touched_is_listed(context):
    context.caller_number = cfg.site["Users"]["R2d2User"]["CoworkerContacts"][0]['number']
    context.caller_name = cfg.site["Users"]["R2d2User"]["CoworkerContacts"][0]['name']
    assert (dial_view.find_named_element("DialPadContactName").text == context.caller_name and
            dial_view.find_named_element("DialPadContactNumber").text == context.caller_number and
            dial_view.find_named_element("DialedNumberTextView").text == context.caller_number),\
        "Contact display is not the correct"


@step("[dial] the buttons are x pixels wide and y pixels high")
def dial__the_buttons_are_x_pixels_wide_and_y_pixels_high(context):
    pass


@step("[dial] the Dial view appears")
def dial__the_dial_view_appears(context):
    assert dial_view.DialPad is not None, "dial_view.DialPad element not present"


