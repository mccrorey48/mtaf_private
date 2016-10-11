import argparse

from ccd.utils.configure import cfg
from lib.user_exception import UserException as Ux

parser = argparse.ArgumentParser()
parser.add_argument("product_dir", type=str, choices=['ePhone7', 'ccd'], help="product directory")
# parser.add_argument("site_tag", type=str, choices=['mm', 'js', 'ds', 'local'], help="site tag")
parser.add_argument("site_tag", type=str, choices=['test', 'alpha'], help="site tag")
args = parser.parse_args()

cfg.set_site(args.site_tag)
cfg.site['Mock'] = True

from ccd.views import *

try:
    # print cfg.get_locator('DomainQuickLaunch', reseller_home_view)
    print reseller_home_view.get_locator('DomainQuickLaunch')
    print reseller_home_view.get_locator('TestDomainMessage')
except Ux as e:
    print "User Exception: %s" % e.msg
# d = {key: value for key, value in cfg.__dict__.items() if not key.startswith('__') and not callable(key)}
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(d)

