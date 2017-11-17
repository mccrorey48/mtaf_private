import re
import lib.logging_esi
from lib.wrappers import Trace
from datetime import datetime, timedelta


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

re_tokens = re.compile(r'\b[a-z]{1,3}\b')


def expand_zpath(zpath):
    other = re_tokens.split(zpath)
    tokens = re_tokens.findall(zpath)
    new_zpath = ''
    while len(other) or len(tokens):
        if len(other):
            new_zpath += other.pop(0)
        if len(tokens):
            new_zpath += get_path(tokens.pop(0))
    return new_zpath


def get_age_range_minutes(display_age, delta_minutes=2):
    # analyze the displayed vm age and return a min and max age (in minutes)
    # that would match the age of the timestamp in the vm metadata "dateRecorded" field
    # min_age = 0
    # max_age = 0
    if display_age == 'in 0 minutes':
        min_age = 0
        max_age = 0
    elif display_age.endswith(' minutes ago') or display_age == '1 minute ago':
        age = int(display_age.split()[0])
        min_age = age
        max_age = age
    elif display_age.endswith(' hours ago') or display_age == '1 hour ago':
        age = int(display_age.split()[0]) * 60
        min_age = age
        max_age = age + 59
    elif display_age == 'Yesterday':
        now = datetime.now()
        midnight = datetime(now.year, now.month, now.day)
        oldest = midnight - timedelta(days=1)
        newest = midnight - timedelta(minutes=1)
        min_age = int((now - newest).total_seconds())/60
        max_age = int((now - oldest).total_seconds())/60
    elif display_age.endswith(' days ago'):
        days = int(display_age.split()[0])
        now = datetime.now()
        midnight = datetime(now.year, now.month, now.day)
        oldest = midnight - timedelta(days=days)
        newest = midnight - timedelta(days=days - 1, minutes=1)
        min_age = int((now - newest).total_seconds())/60
        max_age = int((now - oldest).total_seconds())/60
    else:
        date = datetime.strptime(display_age, '%b %d, %Y')
        now = datetime.now()
        midnight = datetime(now.year, now.month, now.day)
        days = (now - date).days
        oldest = midnight - timedelta(days=days)
        newest = midnight - timedelta(days=days - 1, minutes=1)
        min_age = int((now - newest).total_seconds())/60
        max_age = int((now - oldest).total_seconds())/60
    return max(min_age - delta_minutes, 0), max_age + delta_minutes


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
