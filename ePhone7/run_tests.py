import argparse
import time

import lib.common.logging_esi as logging_esi

from lib.esi_result import EsiResult

log = logging_esi.get_logger('esi.run_tests')


parser = argparse.ArgumentParser()
parser.add_argument("site_tag", choices=['mm', 'js', 'local', 'ds'], help="site tag, selects config/site_<tag>.json file")
parser.add_argument("--failfast", help="stop testing when a test case fails", action="store_true")
parser.add_argument("--mock", help="use mock driver", action="store_true")
parser.add_argument("--dbhost", help="name of mongodb server")
parser.add_argument("--quiet", help="use -20db wave files", action="store_true")
args = parser.parse_args()

with logging_esi.msg_src_cm('run_tests'):
    import unittest
    from ePhone7.utils.configure import cfg

    cfg.set_site(args.site_tag)

    if args.dbhost:
        log.set_db('localhost', 'results_ePhone7', time.strftime('%m_%d_%y-%H_%M_%S', time.localtime()))

    cfg.site['Mock'] = args.mock
    cfg.site['Quiet'] = args.quiet

    import ePhone7.suites.smoke as smoke

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(smoke.SmokeTests))
    unittest.TextTestRunner(verbosity=0, resultclass=EsiResult, failfast=args.failfast).run(suite)
