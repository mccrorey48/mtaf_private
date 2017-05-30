import os
from pymongo import MongoClient
from lib.mongo import merge_collection
from lib.user_exception import UserException as Ux


class Cfg(object):

    def __init__(self):
        self.cfg_folder_path = None
        self.test_screenshot_folder = None
        self.screenshot_folder = None
        self.xml_folder = None
        self.csv_folder = None
        self.colors_folder = None
        self.site = {}
        self.exec_dir = os.getcwd()
        self.caps = {}
        self.colors = {}
        self.site_tag = os.getenv('MTAF_SITE')
        if not self.site_tag:
            raise Ux('MTAF_SITE must be defined in the run-time environment')
        server = os.getenv('MTAF_DB_HOST')
        if not server:
            raise Ux('MTAF_DB_HOST must be defined in the run-time environment')
        self.set_site(server, self.site_tag)

    def set_site(self, cfg_server, site_tag):
        client = MongoClient(cfg_server)
        db = client['e7_site']
        merge_collection(self.site, db[site_tag])
        merge_collection(self.site, db["default"])
        db = client['e7_caps']
        for name in db.collection_names(False):
            self.caps[name] = {}
            merge_collection(self.caps[name], db[name])
        db = client['e7_colors']
        for name in db.collection_names(False):
            self.colors[name] = {}
            merge_collection(self.colors[name], db[name])
            self.test_screenshot_folder = os.path.join(self.exec_dir, self.site['TestScreenshotsFolder'])
            self.screenshot_folder = os.path.join(self.exec_dir, self.site['ScreenshotsFolder'])
            self.xml_folder = os.path.join(self.exec_dir, self.site['XmlFolder'])
            self.csv_folder = os.path.join(self.exec_dir, self.site['CsvFolder'])
            self.colors_folder = os.path.join(self.exec_dir, self.site['ColorsFolder'])

cfg = Cfg()

if __name__ == '__main__':
    import json
    json_repr = json.dumps(cfg.__dict__, sort_keys=True, indent=4, separators=(',', ': '))
    with open('cfg_site.json', 'w') as f:
        f.write(json_repr)
