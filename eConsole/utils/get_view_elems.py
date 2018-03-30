from eConsole.views import *
from eConsole.config.configure import cfg
from time import sleep
# from bs4 import BeautifulSoup
from mtaf import mtaf_logging
cfg.set_test_target("devdash")
log = mtaf_logging.get_logger('esi.get_view_elems')

base_view.open_browser()
base_view.get_url("http://devdash.esi-estech.com")
if login_view.becomes_present():
    login_view.input_username('select')
    login_view.input_password('select')
    login_view.click_login_button()
    if home_view.becomes_present():
        sleep(1)
        tabs = home_view.find_named_elements("NavTabs")
        for tab in tabs:
            print tab.text
base_view.close_browser()


