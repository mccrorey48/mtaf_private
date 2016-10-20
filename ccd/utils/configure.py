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
        self.exec_dir = os.getcwd()
        self.caps = {}
        self.locators = {}
        self.colors = {}
        self.site = {}

    def set_site(self, cfg_host, svr_tag):
        client = MongoClient(cfg_host)
        db = client['ccd_site']
        svr_collection = db[svr_tag]
        merge_collection(self.site, svr_collection)
        net_collection = db[self.site["Network"]]
        merge_collection(self.site, net_collection)
        default_collection = db['default']
        merge_collection(self.site, default_collection)


cfg = Cfg()
