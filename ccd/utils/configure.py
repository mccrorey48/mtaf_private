import json
import os
from ccd.utils.db_utils import read_dbs


def stringify(thing):
    if type(thing) is unicode:
        return str(thing)
    elif type(thing) is dict:
        newdict = {}
        for key in thing:
            newdict[str(key)] = stringify(thing[key])
        return newdict
    elif type(thing) is list:
        return [stringify(item) for item in thing]
    else:
        return thing


class Cfg:
    cfg_folder_path = None
    test_screenshot_folder = None
    screenshot_folder = None
    xml_folder = None
    csv_folder = None
    colors_folder = None
    exec_dir = os.getcwd()
    caps = {}
    locators = {}
    colors = {}

    def set_site(self, svr_tag):
        site = read_dbs(['ccd_site'])[svr_tag]
        pass


cfg = Cfg()
