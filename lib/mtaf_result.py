import unittest

import lib.logging_esi as logging_esi

log = logging_esi.get_logger('esi.result')


class MtafResult(unittest.TextTestResult):

    def __init__(self, *args, **kwargs):
        unittest.TextTestResult.__init__(self, *args, **kwargs)
        logging_esi.set_msg_src(self.__class__.__name__)

    def startTest(self, test):
        super(MtafResult, self).startTest(test)
        with logging_esi.msg_src_cm(test.id().split('.')[-1]):
            log.info("TEST CASE: %-35s start" % test.id().split('.')[-1])

    def addSuccess(self, test):
        super(MtafResult, self).addSuccess(test)
        with logging_esi.msg_src_cm(test.id().split('.')[-1]):
            log.info("TEST CASE: %-35s PASS", test.id().split('.')[-1])

    def addSkip(self, test, reason):
        super(MtafResult, self).addSkip(test, reason)
        with logging_esi.msg_src_cm(test.id().split('.')[-1]):
            log.info("TEST CASE: %-35s skipped", test.id().split('.')[-1])

    def addFailure(self, test, err):
        super(MtafResult, self).addFailure(test, err)
        with logging_esi.msg_src_cm(test.id().split('.')[-1]):
            log.error("TEST CASE: %-35s FAIL - %s" % (test.id().split('.')[-1], err[1]))

    def addError(self, test, err):
        super(MtafResult, self).addFailure(test, err)
        with logging_esi.msg_src_cm(test.id().split('.')[-1]):
            log.error("TEST CASE: %-35s ERROR - %s" % (test.id().split('.')[-1], err[1]))

    # def stopTestRun(self):
    #     pass
