import re

from lib.user_exception import UserException as Ux

path_by_abbrev = {
    "": "",
    "bt": "android.widget.Button",
    "el": "android.widget.ExpandableListView",
    "fl": "android.widget.FrameLayout",
    "gl": "android.widget.GridLayout",
    "gv": "android.widget.GridView",
    "h":  "hierarchy",
    "ib": "android.widget.ImageButton",
    "iv": "android.widget.ImageView",
    "ll": "android.widget.LinearLayout",
    "lv": "android.widget.ListView",
    "rl": "android.widget.RelativeLayout",
    "rv": "android.support.v7.widget.RecyclerView",
    "sv": "android.widget.ScrollView",
    "th": "android.widget.TabHost",
    "tl": "android.widget.TableLayout",
    "tr": "android.widget.TableRow",
    "tv": "android.widget.TextView",
    "tw": "android.widget.TabWidget",
    "v":  "android.view.View",
    "vp": "android.support.v4.view.ViewPager"
}

abbrev_by_path = dict((v, k) for k, v in path_by_abbrev.iteritems())


def get_path(abbrev):
    if abbrev in path_by_abbrev:
        return path_by_abbrev[abbrev]
    else:
        return abbrev


def get_abbrev(path):
    if path in abbrev_by_path:
        return abbrev_by_path[path]
    else:
        return path

re_elem_index = re.compile('([^\[\]]*)(\[[^\]]+\])?')


def expand_zpath(zpath):
    # short names will be expanded to their long name equivalents if the locator["by"] method is "zpath"
    token_list = zpath.split('/')
    term_list = []
    for token in token_list:
        re_match = re_elem_index.match(token)
        if not re_match:
            raise Ux('Program Error: expand_zpath(%s), token %s does not match re' % (zpath, token))
        bare_token = re_match.group(1)
        index_suffix = re_match.group(2)
        path_term = get_path(bare_token)
        if index_suffix is not None:
            path_term += index_suffix
        term_list.append(path_term)
    return '/'.join(term_list)


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


