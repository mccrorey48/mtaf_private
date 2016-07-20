import lib.common.logging_esi as logging
log = logging.get_logger('esi.mock')

# def loginfo(fn):
#     def wrapper(*args, **kwargs):
#         if len(args) > 1:
#             log.info('%s(%s)' % (fn.func_name, ', '.join(args[1:])))
#         else:
#             log.info('%s()' % (fn.func_name))
#         return fn(*args, **kwargs)
#     return wrapper

class MockElement:
    tag_name = 'mock element'
    text = 'mock element'
    location = {'x': 0, 'y': 0}
    size = {'height': 0, 'width': 0}

    def __init__(self):
        self.name = 'MockElement'

    def click(self):
        log.info('MockElement.click()')

    def get_attribute(self, attr):
        log.info('MockElement.get_attribute(%s)' % attr)
        return 'mock ' + attr + ' attribute'

    def hide_keyboard(self):
        log.info('MockElement.hide_keyboard()')

    def is_displayed(self):
        log.info('MockElement.is_displayed() returning True')
        return True

    def is_enabled(self):
        log.info('MockElement.is_enabled() returning True')
        return True

    def set_value(self, value):
        log.info('MockElement.set_value(%s)' % value)

    def set_text(self, value):
        log.info('MockElement.set_value(%s)' % value)

    def send_keys(self, value):
        log.info('MockElement.send_keys(%s)' % value)

    def find_element_by_xpath(self, xpath):
        return MockElement()

    def find_element_by_name(self, name):
        log.info('MockElement.find_element_by_name(%s)' % name)
        return MockElement()

    def find_element_by_classname(self, classname):
        log.info('MockElement.find_element_by_classname(%s)' % classname)
        return MockElement()

    def find_element_by_id(self, id):
        log.info('MockElement.find_element_by_id(%s)' % id)
        return MockElement()

    def find_elements_by_xpath(self, xpath):
        log.info('MockElement.find_elements_by_xpath(%s)' % xpath)
        return [MockElement(), MockElement()]

    def find_elements_by_name(self, name):
        log.info('MockElement.find_elements_by_name(%s)' % name)
        return [MockElement(), MockElement()]

    def find_elements_by_classname(self, classname):
        log.info('MockElement.find_elements_by_classname(%s)' % classname)
        return [MockElement(), MockElement()]

    def find_elements_by_id(self, id):
        log.info('MockElement.find_elements_by_id(%s)' % id)
        return [MockElement(), MockElement()]


class MockDriver:

    def __init__(self):
        pass

    def close_app(self):
        pass

    def quit(self):
        pass

    def execute_script(self, script, args):
        pass

    def find_element_by_xpath(self, xpath):
        log.info('find_element_by_xpath(%s)' % xpath)
        return MockElement()

    def find_element_by_name(self, name):
        log.info('find_element_by_xpath(%s)' % name)
        return MockElement()

    def find_element_by_classname(self, classname):
        log.info('find_element_by_xpath(%s)' % classname)
        return MockElement()

    def find_element_by_id(self, _id):
        log.info('find_element_by_xpath(%s)' % _id)
        return MockElement()

    def find_elements_by_xpath(self, xpath):
        log.info('find_element_by_xpath(%s)' % xpath)
        return [MockElement(), MockElement()]

    def find_elements_by_name(self, name):
        log.info('find_element_by_xpath(%s)' % name)
        return [MockElement(), MockElement()]

    def find_elements_by_classname(self, classname):
        log.info('find_element_by_xpath(%s)' % classname)
        return [MockElement(), MockElement()]

    def find_elements_by_id(self, _id):
        log.info('find_element_by_xpath(%s)' % _id)
        return [MockElement(), MockElement()]

    def scroll(self, origin_el, destination_el):
        log.info('scroll(%s, %s)' % (origin_el.text, destination_el.text))

    def swipe(self, x1, y1, x2, y2, duration):
        log.info('swipe(%s, %s, %s, %s, %s)' % (x1, y1, x2, y2, duration))
        return [MockElement(), MockElement()]

    def tap(self, loc, duration):
        log.info('tap(%s, %s, %s)' % (loc[0], loc[1], duration))

    def hide_keyboard(self):
        log.info('hide_keyboard()')

    def get_screenshot_as_file(self, filename):
        log.info('get_screenshot_as_file(%s)' % filename)
