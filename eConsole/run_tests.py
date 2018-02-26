import argparse
import lib.logging_esi as logging

from lib.esi_result import EsiResult

log = logging.get_logger('mtaf.run_tests')

parser = argparse.ArgumentParser()
parser.add_argument("server_tag", choices=['alpha', 'test'], help="server tag, selects server to test")
parser.add_argument("--cfg_server", default='vqda', help="mongodb configuration server host name or IP (default 'vqda')")
parser.add_argument("--failfast", help="stop testing when a test case fails", action="store_true")
args = parser.parse_args()

with logging.msg_src_cm('run_tests'):
    import unittest
    from eConsole.config.configure import cfg

    cfg.set_test_target(args.cfg_server, args.server_tag)

    import eConsole.suites.cron as cron

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(cron.LoginTests))
    unittest.TextTestRunner(verbosity=0, resultclass=EsiResult, failfast=args.failfast).run(suite)
