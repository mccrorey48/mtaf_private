from behave import *
from mtaf import mtaf_logging
from ePhone7.views import *
from mtaf.trace import fake
from ePhone7.config.configure import cfg
from mtaf.user_exception import UserException as Ux

log = mtaf_logging.get_logger('mtaf.dial_steps')


@step("[dial] A list of contacts containing the partial number appears above the keypad")
@fake
def dial__a_list_of_contacts_containing_the_partial_number_appears_above_the_keypad(context):
    pass


@step("[dial] A list of Coworker contacts containing the partial name appears above the keypad")
@fake
def dial__a_list_of_coworker_contacts_containing_the_partial_name_appears_above_the_keypad(context):
    elem = dial_view.find_named_element("HideDialPad")
    elem.click
    dial_elems = dial_view.find_named_elements("DialPadContactName").text
    log.debug("records=", dial_elems)
    for i in dial_elems:
        if dial_elems[i] != cfg.site["Users"]["R2d2User"]["CoworkerContactsName"]:
            elem.click
            return True
        else:
            raise Ux('No Coworker element found ')
            # log.debug("coworkers = %s" % entry_elem.location['y'])
            return False


@step("[dial] A list of Personal contacts containing the partial name appears above the keypad")
@fake
def dial__a_list_of_personal_contacts_containing_the_partial_name_appears_above_the_keypad(context):
    pass


@step("[dial] I dial the {code_name} direct code")
@fake
def dial__i_dial_the_codename_direct_code(context, code_name):
    dial_view.dial_named_number(code_name)


@step("[dial] I enter a 10-digit phone number using the keypad")
@fake
def dial__i_enter_a_10digit_phone_number_using_the_keypad(context):
    context.active_screen_number = cfg.site["10DigitNumber"]
    dial_view.dial_number(context.active_screen_number)


@step("[dial] I enter a Coworker contact number using the keypad")
@fake
def dial__i_enter_a_coworker_contact_number_using_the_keypad(context):
    context.active_screen_number = cfg.site["Users"]["R2d2User"]["CoworkerContacts"][0]
    dial_view.dial_number(context.active_screen_number)


@step("[dial] I enter part of a Coworker contact number using the keypad")
@fake
def dial__i_enter_part_of_a_coworker_contact_number_using_the_keypad(context):
    dial_view.dial_number(cfg.site["Users"]["R2d2User"]["CoworkerContactsDialPadNumber"])
    # search "terA, terB and terC"


@step("[dial] I make a call to a coworker contact")
@fake
def dial__i_make_a_call_to_a_coworker_contact(context):
    context.softphone = user_view.configure_called_answer_ring()
    dial_view.dial_number(context.softphone.number)
    dial_view.touch_dial_button()
    context.softphone.wait_for_call_status('early', dial_view.call_status_wait)


@step("[dial] I see the keypad")
@fake
def dial__i_see_the_keypad(context):
    assert dial_view.DialPad is not None, "dial_view.DialPad element not present"


@step("[dial] I touch the Call button")
@fake
def dial__i_touch_the_call_button(context):
    dial_view.touch_dial_button()


@step("[dial] I touch the contact listing I want to call")
@fake
def dial__i_touch_the_contact_listing_i_want_to_call(context):
    pass


@step("[dial] Only the contact I touched is listed")
@fake
def dial__only_the_contact_i_touched_is_listed(context):
    pass


@step("[dial] the buttons are x pixels wide and y pixels high")
@fake
def dial__the_buttons_are_x_pixels_wide_and_y_pixels_high(context):
    pass


@step("[dial] the Dial view appears")
@fake
def dial__the_dial_view_appears(context):
    assert dial_view.DialPad is not None, "dial_view.DialPad element not present"
