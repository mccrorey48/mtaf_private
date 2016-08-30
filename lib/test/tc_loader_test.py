import argparse
import unittest

parser = argparse.ArgumentParser()
parser.add_argument("dir_name", choices=['ePhone7', 'ePhonego-android', 'ePhoneGo-iOS'], help="dir name, selects mtaf subdirectory")
parser.add_argument("site_tag", choices=['mm', 'js', 'local'], help="site tag, selects config/site_<tag>.json file")
args = parser.parse_args()

from ePhone7.utils.configure import cfg

cfg.set_site(args.dir_name, args.site_tag)

# suite = unittest.TestSuite()
# suite.addTest(unittest.TestLoader().loadTestsFromTestCase(smoke.SmokeTests))
import ePhone7.suites.smoke as smoke
suite = unittest.TestSuite()
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(smoke.SmokeTests))
names = unittest.TestLoader().getTestCaseNames(suite)
for name in names:
    print name
