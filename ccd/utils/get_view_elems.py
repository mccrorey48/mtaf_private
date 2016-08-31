import argparse
parser = argparse.ArgumentParser()
parser.add_argument("svr_tag", choices=['alpha', 'test'], help="server tag, selects server to test")
args = parser.parse_args()

from ccd.utils.configure import cfg
cfg.set_site(args.svr_tag)

import lib.common.logging_esi as logging_esi
log = logging_esi.get_logger('esi.get_view_elems')

from ccd.views.login import login_view
elems = login_view.actions.driver.find_elements_by_css_selector('*')
print "login page id's"
for elem in elems:
    id = elem.get_attribute('id')
    if id:
        print id

from ccd.views.reseller_home import reseller_home_view
login_view.login_with_good_credentials()
elems = reseller_home_view.actions.driver.find_elements_by_css_selector('*')
print "reseller_home page id's"
for elem in elems:
    id = elem.get_attribute('id')
    if id:
        print id


