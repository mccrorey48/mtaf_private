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

    def __init__(self):
        self.cfg_folder_path = None
        self.test_screenshot_folder = None
        self.screenshot_folder = None
        self.xml_folder = None
        self.csv_folder = None
        self.colors_folder = None
        self.site = None
        self.exec_dir = os.getcwd()
        self.caps = {}
        self.colors = {}

    def set_site(self, site_tag):
        self.cfg_folder_path = os.path.join(self.exec_dir, 'ePhone7', 'config')
        self.caps = stringify(json.load(open(os.path.join(self.cfg_folder_path, 'caps.json'))))
        self.colors = stringify(json.load(open(os.path.join(self.cfg_folder_path, 'colors.json'))))
        self.site = stringify(json.load(open(os.path.join(self.cfg_folder_path, 'site_%s.json' % site_tag))))
        self.test_screenshot_folder = os.path.join(self.exec_dir, self.site['TestScreenshotsFolder'])
        self.screenshot_folder = os.path.join(self.exec_dir, self.site['ScreenshotsFolder'])
        self.xml_folder = os.path.join(self.exec_dir, self.site['XmlFolder'])
        self.csv_folder = os.path.join(self.exec_dir, self.site['CsvFolder'])
        self.colors_folder = os.path.join(self.exec_dir, self.site['ColorsFolder'])

cfg = Cfg()
