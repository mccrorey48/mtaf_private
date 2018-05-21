from mtaf import mtaf_logging
from ccd.utils.configure import cfg
from ccd.views.login import login_view
from ccd.views.reseller_home import reseller_home_view
import argparse
import six
parser = argparse.ArgumentParser()
parser.add_argument("svr_tag", choices=['alpha', 'test'], help="server tag, selects server to test")
parser.add_argument('-c', '--cfg_host', help='name of mongodb server for test configuration, default "vqda"',
                    default='vqda')
args = parser.parse_args()

cfg.set_site(args.cfg_host, args.svr_tag)

log = mtaf_logging.get_logger('mtaf.get_view_elems')

elems = login_view.actions.driver.find_elements_by_css_selector('*')
six.print_("login page id's")
for elem in elems:
    id = elem.get_attribute('id')
    if id:
        six.print_(id)

login_view.login_with_good_credentials()
elems = reseller_home_view.actions.driver.find_elements_by_css_selector('*')
six.print_("reseller_home page id's")
for elem in elems:
    id = elem.get_attribute('id')
    if id:
        six.print_(id)

reseller_home_view.logout()
login_view.actions.close_browser()

