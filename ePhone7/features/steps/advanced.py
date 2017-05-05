from behave import *
from ePhone7.views import *
from time import sleep


@step("[advanced] I {action} the Call Record Enable checkbox")
def advanced__i_action_the_call_record_enable_checkbox(context, action):
    if 'fake' not in str(context._config.tags).split(','):
        cbs = base_view.find_named_elements("AdvancedCheckbox")
        assert len(cbs) > 2, "Expected >2 AdvancedCheckbox elements, got %s" % len(cbs)
        if action.lower() == 'check':
            desired_value = 'true'
        elif action.lower() == 'uncheck':
            desired_value = 'false'
        if cbs[1].get_attribute('checked') != desired_value:
            cbs[1].click()
            checked = cbs[1].get_attribute('checked')
            assert checked == desired_value


@step("[advanced] I scroll down to the Call Record Enable setting")
def advanced__i_scroll_down_to_the_call_record_enable_setting(context):
    if 'fake' not in str(context._config.tags).split(','):
        elems = user_view.find_named_elements('AdvancedItems')
        assert len(elems) > 1
        base_view.scroll(elems[-1], elems[0])
        if not base_view.element_is_present('CallRecordEnableText'):
            # one retry in case the scroll didn't work
            base_view.scroll(elems[-1], elems[0])
            assert base_view.element_is_present('CallRecordEnableText')


@step("[advanced] the Advanced Options view appears")
def advanced__the_advanced_options_view_appears(context):
    if 'fake' not in str(context._config.tags).split(','):
        assert user_view.element_is_present('AdvancedOptions'), "Expected Advanced Options view to appear but it did not"

