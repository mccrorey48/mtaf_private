import re

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
            abbrev = tokens.pop(0)
            if abbrev in path_by_abbrev:
                new_zpath += path_by_abbrev[abbrev]
            else:
                new_zpath += abbrev
    return new_zpath


