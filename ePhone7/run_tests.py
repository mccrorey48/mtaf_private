import argparse
import time
from mtaf import mtaf_logging
from mtaf.esi_result import EsiResult

log = mtaf_logging.get_logger('esi.run_tests')


parser = argparse.ArgumentParser()
parser.add_argument('-f', '--failfast', help='stop testing when a test case fails', action='store_true')
parser.add_argument('-m', '--mock', help='use mock driver', action='store_true')
parser.add_argument('-l', '--log_host', help='name of mongodb server for logging')
parser.add_argument('--quiet', help='use -20db wave files', action='store_true')
args = parser.parse_args()

with logging_esi.msg_src_cm('run_tests'):
    import unittest
    from ePhone7.config.configure import cfg

    if args.log_host:
        log.set_db(args.log_host, 'results_ePhone7', time.strftime('%m_%d_%y-%H_%M_%S', time.localtime()))

    cfg.site['Mock'] = args.mock
    cfg.site['Quiet'] = args.quiet

    import ePhone7.suites.smoke as smoke

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(smoke.SmokeTests))
    unittest.TextTestRunner(verbosity=0, resultclass=EsiResult, failfast=args.failfast).run(suite)
