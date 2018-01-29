from behave import *
from ePhone7.views import *
from mtaf.trace import fake


@step("[advanced] I {action} the Call Record Enable checkbox")
@fake
def advanced__i_action_the_call_record_enable_checkbox(context, action):
    cbs = advanced_settings_view.find_named_elements("AdvancedCheckbox")
    assert len(cbs) > 2, "Expected >2 AdvancedCheckbox elements, got %s" % len(cbs)
    if action.lower() == 'check':
        desired_value = 'true'
    else:
        desired_value = 'false'
    if cbs[1].get_attribute('checked') != desired_value:
        cbs[1].click()
        checked = cbs[1].get_attribute('checked')
        assert checked == desired_value


@step("[advanced] I scroll down to the Call Record Enable setting")
@fake
def advanced__i_scroll_down_to_the_call_record_enable_setting(context):
    elems = advanced_settings_view.find_named_elements('AdvancedItems')
    assert len(elems) > 1
    advanced_settings_view.long_press_scroll(elems[-1], elems[0])
    if not advanced_settings_view.element_is_present('CallRecordEnableText'):
        # one retry in case the scroll didn't work
        advanced_settings_view.long_press_scroll(elems[-1], elems[0])
        assert advanced_settings_view.element_is_present('CallRecordEnableText'), "Call Record Enable text not present"


@step("[advanced] the Advanced Options view appears")
@fake
def advanced__the_advanced_options_view_appears(context):
    assert advanced_settings_view.element_is_present('AdvancedOptions'), \
        "Expected Advanced Options view to appear but it did not"
