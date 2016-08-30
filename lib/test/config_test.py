import argparse
import pprint

from ePhone7.utils.configure import cfg

parser = argparse.ArgumentParser()
parser.add_argument("dir_name", type=str, choices=['ePhone7', 'ePhoneGo-android', 'ePhoneGo-iOS'],
                    help="specify name of product directory")
parser.add_argument("site_tag", type=str, choices=['mm', 'js'], help="specify site tag")
args = parser.parse_args()

cfg.set_site(args.dir_name, args.site_tag)

d = {key: value for key, value in cfg.__dict__.items() if not key.startswith('__') and not callable(key)}
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(d)

