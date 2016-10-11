import json
import os


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
    site = None
    exec_dir = os.getcwd()
    caps = {}
    locators = {}
    colors = {}

    def set_site(self, svr_tag):
        self.cfg_folder_path = os.path.join(self.exec_dir, 'ccd', 'config')
        self.site = stringify(json.load(open(os.path.join(self.cfg_folder_path, 'site_%s.json' % svr_tag))))

cfg = Cfg()
