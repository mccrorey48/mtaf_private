import os
from pymongo import MongoClient
from lib.mongo import merge_collection


class Cfg:

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

    def set_site(self, cfg_server, site_tag):
        client = MongoClient(cfg_server)
        db = client['ego_android_site']
        site_collection = db[site_tag]
        merge_collection(self.site, site_collection)
        db = client['ego_android_caps']
        for name in db.collection_names(False):
            self.caps[name] = {}
            merge_collection(self.caps[name], db[name])
        db = client['ego_android_colors']
        for name in db.collection_names(False):
            self.colors[name] = {}
            merge_collection(self.colors[name], db[name])
            self.test_screenshot_folder = os.path.join(self.exec_dir, self.site['TestScreenshotsFolder'])
            self.screenshot_folder = os.path.join(self.exec_dir, self.site['ScreenshotsFolder'])
            self.xml_folder = os.path.join(self.exec_dir, self.site['XmlFolder'])
            self.csv_folder = os.path.join(self.exec_dir, self.site['CsvFolder'])
            self.colors_folder = os.path.join(self.exec_dir, self.site['ColorsFolder'])

cfg = Cfg()
