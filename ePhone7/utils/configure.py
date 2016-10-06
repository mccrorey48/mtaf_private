import json
import os
import inspect
from lib.common.user_exception import UserException as Ux
from lib.android.zpath import expand_zpath


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

    def set_site(self, site_tag):
        self.cfg_folder_path = os.path.join(self.exec_dir, 'ePhone7', 'config')
        self.caps = stringify(json.load(open(os.path.join(self.cfg_folder_path, 'caps.json'))))
        self.locators = stringify(json.load(open(os.path.join(self.cfg_folder_path, 'locators.json'))))
        self.colors = stringify(json.load(open(os.path.join(self.cfg_folder_path, 'colors.json'))))
        self.site = stringify(json.load(open(os.path.join(self.cfg_folder_path, 'site_%s.json' % site_tag))))
        self.test_screenshot_folder = os.path.join(self.exec_dir, self.site['TestScreenshotsFolder'])
        self.screenshot_folder = os.path.join(self.exec_dir, self.site['ScreenshotsFolder'])
        self.xml_folder = os.path.join(self.exec_dir, self.site['XmlFolder'])
        self.csv_folder = os.path.join(self.exec_dir, self.site['CsvFolder'])
        self.colors_folder = os.path.join(self.exec_dir, self.site['ColorsFolder'])

    def get_locator(self, locator_name, actions_instantiator):
        view_chain = [c.__name__ for c in inspect.getmro(actions_instantiator.__class__)]
        for view_name in view_chain:
            if view_name in self.locators and locator_name in self.locators[view_name]:
                locator = self.locators[view_name][locator_name]
                locator_copy = {}
                for key in locator.keys():
                    locator_copy[key] = locator[key]
                if locator_copy["by"] == "zpath":
                    locator_copy["by"] = "xpath"
                    locator_copy["value"] = expand_zpath(locator["value"])
                return locator_copy
        raise Ux('locator with name %s is not in views: %s' % (locator_name, ','.join(view_chain)))

cfg = Cfg()
