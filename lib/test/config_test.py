import argparse
# import pprint
# import json
from lib.common.user_exception import UserException as Ux
from ePhone7.utils.configure import cfg

parser = argparse.ArgumentParser()
parser.add_argument("product_dir", type=str, choices=['ePhone7', 'ccd'], help="product directory")
parser.add_argument("site_tag", type=str, choices=['mm', 'js', 'ds', 'local'], help="site tag")
args = parser.parse_args()

cfg.set_site(args.site_tag)
cfg.site['Mock'] = True

from ePhone7.views.prefs import prefs_view

try:
    print cfg.get_locator('About', prefs_view)
except Ux as e:
    print "User Exception: %s" % e.msg
# d = {key: value for key, value in cfg.__dict__.items() if not key.startswith('__') and not callable(key)}
# pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(d)

