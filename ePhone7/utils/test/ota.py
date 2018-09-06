from ePhone7.views import *
from mtaf.decorators import Trace
from mtaf import mtaf_logging
log = logger.get_logger('mtaf.ota')
from mtaf.user_exception import UserException as Ux


@Trace(log)
def set_alpha_ota_server():
    dial_view.goto_advanced_settings()
    assert advanced_settings_view.element_is_present('AdvancedOptions'), "Expected Advanced Options view to appear but it did not"
    elems = advanced_settings_view.find_named_elements('AdvancedItems')
    assert len(elems) > 1
    advanced_settings_view.long_press_scroll(elems[-1], elems[0])
    if not advanced_settings_view.element_is_present('TestOtaServerUrlText'):
        # one retry in case the long_press_scroll didn't work
        advanced_settings_view.long_press_scroll(elems[-1], elems[0])
    use_ota_text = advanced_settings_view.find_named_element('UseTestOtaServerText')
    text_ycenter = use_ota_text.location['y'] + (use_ota_text.size['height'] / 2)
    checkboxes = advanced_settings_view.find_named_elements('AdvancedCheckbox')
    for cb in checkboxes:
        min_y = cb.location['y']
        max_y = min_y + cb.size['height']
        if min_y < text_ycenter < max_y:
            break
    else:
        raise Ux('"Use Test OTA Server" checkbox not found')
    if cb.get_attribute('checked') == 'false':
        cb.click()
    advanced_settings_view.click_named_element('TestOtaServerUrlText')
    ota_url = advanced_settings_view.find_named_element('TestOtaEditText')
    ota_url.clear()
    ota_url.set_text('http://52.36.62.239/aus/')

