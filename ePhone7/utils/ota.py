from ePhone7.views import *
from lib.wrappers import Trace
import lib.logging_esi as logger
log = logger.get_logger('esi.ota')
from lib.user_exception import UserException as Ux


@Trace(log)
def set_alpha_ota_server():
    dial_view.dial_name('Advanced Settings')
    dial_view.click_named_element('FuncKeyCall')
    assert user_view.element_is_present('AdvancedOptions'), "Expected Advanced Options view to appear but it did not"
    elems = user_view.find_named_elements('AdvancedItems')
    assert len(elems) > 1
    base_view.scroll(elems[-1], elems[0])
    if not user_view.element_is_present('TestOtaServerUrlText'):
        # one retry in case the scroll didn't work
        base_view.scroll(elems[-1], elems[0])
    use_ota_text = user_view.find_named_element('UseTestOtaServerText')
    text_ycenter = use_ota_text.location['y'] + (use_ota_text.size['height'] / 2)
    checkboxes = base_view.find_named_elements('AdvancedCheckbox')
    for cb in checkboxes:
        min_y = cb.location['y']
        max_y = min_y + cb.size['height']
        if min_y < text_ycenter < max_y:
            break
    else:
        raise Ux('"Use Test OTA Server" checkbox not found')
    if cb.get_attribute('checked') == 'false':
        cb.click()
    user_view.click_named_element('TestOtaServerUrlText')
    ota_url = user_view.find_named_element('TestOtaEditText')
    ota_url.clear()
    ota_url.set_text('http://52.36.62.239/aus/')

