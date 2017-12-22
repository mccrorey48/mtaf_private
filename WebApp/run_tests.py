import argparse

import lib.mtaf_logging as mtaf_logging

from lib.mtaf_result import MtafResult

log = mtaf_logging.get_logger('mtaf.run_tests')

parser = argparse.ArgumentParser()
parser.add_argument("--failfast", help="stop testing when a test case fails", action="store_true")
args = parser.parse_args()

with mtaf_logging.msg_src_cm('run_tests'):
    import unittest
    from WebApp.suites import unit_tests
    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(unit_tests.LoginTests))
    unittest.TextTestRunner(verbosity=0, resultclass=MtafResult, failfast=args.failfast).run(suite)
