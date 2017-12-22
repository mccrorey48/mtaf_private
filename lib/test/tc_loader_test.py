import unittest

from WebApp.config.configure import cfg

import WebApp.suites.unit_tests as unit_tests
suite = unittest.TestSuite()
suite.addTest(unittest.TestLoader().loadTestsFromTestCase(unit_tests.UnitTests))
names = unittest.TestLoader().getTestCaseNames(suite)
for name in names:
    print name
