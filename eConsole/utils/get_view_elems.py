from eConsole.views import *
from eConsole.config.configure import cfg
from time import sleep
# from bs4 import BeautifulSoup
from mtaf import mtaf_logging
import six
log = mtaf_logging.get_logger('mtaf.get_view_elems')

base_view.open_browser()
base_view.get_url("http://staging-econsole.esihs.net")
if login_view.becomes_present():
    login_view.input_username('1000@test1.test-eng.com')
    login_view.input_password('1000')
    login_view.click_login_button()
    if home_view.becomes_present():
        sleep(1)
        # tabs = home_view.find_named_elements("NavTabs")
        # tabs = home_view.find_named_elements("NavTabs")
        # for tab in tabs:
        #     six.print_(tab.text)
        pullout = base_view.ContactsPullout
        six.print_("offsetWidth: %s   offsetLeft: %s" % (pullout.get_attribute('offsetWidth'), pullout.get_attribute('offsetLeft')))
        base_view.click_named_element("ShowContacts")
        six.print_("offsetWidth: %s   offsetLeft: %s" % (pullout.get_attribute('offsetWidth'), pullout.get_attribute('offsetLeft')))
        accounts = cfg.site['accounts']
        contact_names = ["%s %s" % (accounts[uri]['name1'], accounts[uri]['name2']) for uri in accounts.keys()]
        for contact_name in sorted(contact_names):
            six.print_(contact_name)
        for contact_name in sorted(contact_names, reverse=True):
            six.print_(contact_name)


        # values = base_view.all.ContactsPulloutValues
        # for value in values:
        #     six.print_(value.text)
base_view.close_browser()


