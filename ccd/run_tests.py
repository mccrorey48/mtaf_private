import argparse
import time

from mtaf import mtaf_logging

from mtaf.test_result import TestResult

log = mtaf_logging.get_logger('mtaf.run_tests')

# log.set_db('localhost', 'results_ccd', time.strftime('%m_%d_%y-%H_%M_%S', time.localtime()))

parser = argparse.ArgumentParser()
parser.add_argument("server_tag", choices=['alpha', 'test'], help="server tag, selects server to test")
parser.add_argument("--cfg_server", default='vqda', help="mongodb configuration server host name or IP (default 'vqda')")
parser.add_argument("--failfast", help="stop testing when a test case fails", action="store_true")
args = parser.parse_args()

with mtaf_logging.msg_src_cm('run_tests'):
    import unittest
    from ccd.utils.configure import cfg

    cfg.set_site(args.cfg_server, args.server_tag)

    import ccd.suites.cron as cron

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(cron.LoginTests))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(cron.ResellerTests))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(cron.DomainTests))
    unittest.TextTestRunner(verbosity=0, resultclass=TestResult, failfast=args.failfast).run(suite)
