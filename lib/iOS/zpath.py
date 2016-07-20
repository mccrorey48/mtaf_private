import re
from common.helpers.user_exception import UserException as Ux

path_by_abbrev = {
    "": "",
    "bt": "android.widget.Button",
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



