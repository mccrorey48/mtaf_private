import json
import os
import inspect
from lib.common.user_exception import UserException as Ux


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
        all_locators = json.load(open(os.path.join(self.cfg_folder_path, 'locators.json')))
        locators = all_locators['default']
        if self.site['Version'] in all_locators:
            version_locators = all_locators[self.site['Version']]
            for key in version_locators:
                locators[key] = version_locators[key]
        self.locators = stringify(locators)

    def get_locator(self, key, actions_instantiator):
        view_chain = [c.__name__ for c in inspect.getmro(actions_instantiator.__class__)]
        for view_name in view_chain:
            if view_name in self.locators and key in self.locators[view_name]:
                return self.locators[view_name][key]
        raise Ux('locator for key %s is not in views: %s' % (key, ','.join(view_chain)))

cfg = Cfg()
