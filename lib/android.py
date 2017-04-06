import re
import lib.logging_esi
from lib.wrappers import Trace


from lib.user_exception import UserException as Ux

path_by_abbrev = {
    "": "",
    "bt": "android.widget.Button",
    "cb": "android.widget.CheckBox",
    "el": "android.widget.ExpandableListView",
    "et": "android.widget.EditText",
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
    "sp": "android.support.v4.widget.SlidingPaneLayout",
    "sv": "android.widget.ScrollView",
    "th": "android.widget.TabHost",
    "tl": "android.widget.TableLayout",
    "tr": "android.widget.TableRow",
    "tv": "android.widget.TextView",
    "tw": "android.widget.TabWidget",
    "v":  "android.view.View",
    "vg": "android.view.ViewGroup",
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


mock_log = lib.logging_esi.get_logger('mock_element')


class MockElement:

    tag_name = 'mock element'
    text = 'mock element'
    location = {'x': 0, 'y': 0}
    size = {'height': 0, 'width': 0}

    def __init__(self):
        self.name = 'MockElement'

    @staticmethod
    @Trace(mock_log)
    def click():
        pass

    @staticmethod
    @Trace(mock_log)
    def get_attribute(attr):
        return 'mock ' + attr + ' attribute'

    @staticmethod
    @Trace(mock_log)
    def hide_keyboard():
        pass

    @staticmethod
    @Trace(mock_log)
    def is_displayed():
        return True

    @staticmethod
    @Trace(mock_log)
    def is_enabled():
        return True

    @staticmethod
    @Trace(mock_log)
    def set_value(value):
        pass

    @staticmethod
    @Trace(mock_log)
    def set_text(value):
        pass

    @staticmethod
    @Trace(mock_log)
    def send_keys(value):
        pass

    @staticmethod
    @Trace(mock_log)
    def find_element_by_xpath(xpath):
        return MockElement()

    @staticmethod
    @Trace(mock_log)
    def find_element_by_name(name):
        return MockElement()

    @staticmethod
    @Trace(mock_log)
    def find_element_by_classname(classname):
        return MockElement()

    @staticmethod
    @Trace(mock_log)
    def find_element_by_id(id):
        return MockElement()

    @staticmethod
    @Trace(mock_log)
    def find_elements_by_xpath(xpath):
        return [MockElement(), MockElement()]

    @staticmethod
    @Trace(mock_log)
    def find_elements_by_name(name):
        return [MockElement(), MockElement()]

    @staticmethod
    @Trace(mock_log)
    def find_elements_by_classname(classname):
        return [MockElement(), MockElement()]

    @staticmethod
    @Trace(mock_log)
    def find_elements_by_id(id):
        return [MockElement(), MockElement()]


class MockDriver:

    def __init__(self):
        pass

    @staticmethod
    @Trace(mock_log)
    def close_app():
        pass

    @staticmethod
    @Trace(mock_log)
    def quit():
        pass

    @staticmethod
    @Trace(mock_log)
    def execute_script(script, args):
        pass

    @staticmethod
    @Trace(mock_log)
    def find_element_by_xpath(xpath):
        return MockElement()

    @staticmethod
    @Trace(mock_log)
    def find_element_by_name(name):
        return MockElement()

    @staticmethod
    @Trace(mock_log)
    def find_element_by_classname(classname):
        return MockElement()

    @staticmethod
    @Trace(mock_log)
    def find_element_by_id(_id):
        return MockElement()

    @staticmethod
    @Trace(mock_log)
    def find_elements_by_xpath(xpath):
        return [MockElement(), MockElement()]

    @staticmethod
    @Trace(mock_log)
    def find_elements_by_name(name):
        return [MockElement(), MockElement()]

    @staticmethod
    @Trace(mock_log)
    def find_elements_by_classname(classname):
        return [MockElement(), MockElement()]

    @staticmethod
    @Trace(mock_log)
    def find_elements_by_id(_id):
        return [MockElement(), MockElement()]

    @staticmethod
    @Trace(mock_log)
    def scroll(origin_el, destination_el):
        pass

    @staticmethod
    @Trace(mock_log)
    def swipe(x1, y1, x2, y2, duration):
        return [MockElement(), MockElement()]

    @staticmethod
    @Trace(mock_log)
    def tap(loc, duration):
        pass

    @staticmethod
    @Trace(mock_log)
    def hide_keyboard():
        pass

    @staticmethod
    @Trace(mock_log)
    def get_screenshot_as_file(filename):
        pass


