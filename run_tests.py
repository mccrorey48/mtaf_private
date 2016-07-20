import lib.common.logging_esi as logging_esi
from lib.common.esi_result import EsiResult
import argparse
log = logging_esi.get_logger('esi.run_tests')

parser = argparse.ArgumentParser()
parser.add_argument("dir_name", choices=['ePhone7', 'ePhonego-android', 'ePhoneGo-iOS'], help="dir name, selects mtaf subdirectory")
parser.add_argument("site_tag", choices=['mm', 'js', 'local'], help="site tag, selects config/site_<tag>.json file")
parser.add_argument("--failfast", help="stop testing when a test case fails", action="store_true")
parser.add_argument("--mock", help="stop testing when a test case fails", action="store_true")
args = parser.parse_args()

with logging_esi.msg_src_cm('run_tests'):
    import unittest
    from lib.common.configure import cfg

    cfg.set_site(args.dir_name, args.site_tag)

    if args.mock:
        cfg.site['Mock'] = True
        log.debug("Using Mock Driver")
    else:
        log.debug("Using Webdriver")

    import ePhone7.suites.smoke as smoke

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(smoke.SmokeTests))
    unittest.TextTestRunner(verbosity=0, resultclass=EsiResult, failfast=args.failfast).run(suite)
