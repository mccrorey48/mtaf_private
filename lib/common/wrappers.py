from lib.common.user_exception import UserException as Ux, UserFailException as Fx, stat_prefix as sp
import lib.common.logging_esi as logging_esi
import re
import sys
import traceback
import inspect

log = logging_esi.get_logger('esi.wrappers')
log.spaces = 0
re_web_elem = re.compile('appium.webdriver.webelement.WebElement[^,]*, element="(\d+)"\)')


# decorator for test cases that puts the test method name in log messages
# that are generated within a test method, and catches Ux exceptions to put
# the message in a "fail" call that unittest will display
class TestCase(object):

    def __init__(self, logger=None, run_list=None, except_cb=None):
        self.run_list = run_list
        self.logger = logger
        self.except_cb = except_cb

    def __call__(self, f):
        def wrapped(*args, **kwargs):
            name = args[0]._testMethodName
            if self.run_list is not None and name not in self.run_list:
                args[0].skipTest('test in skip list')
            else:
                try:
                    with logging_esi.msg_src_cm(name):
                        return Trace(self.logger, self.except_cb)(f)(*args, **kwargs)
                except Ux as e:
                    args[0].fail(e.text)
        return wrapped


class Trace(object):

    def __init__(self, logger=None, except_cb=None):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        self.logger = logger
        self.except_cb = except_cb

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """

        def wrapped_f(*args, **kwargs):
            if self.logger is None:
                logger = log
            else:
                logger = self.logger
                logger.spaces = log.spaces
            called = "%s%s" % (f.func_name, repr(args))
            called = re_web_elem.sub(r'\1', called)
            if called[-2:] == ',)':
                called = called[:-2] + ')'
            logger.trace("%10s %s%s" % ('TRACE:', ' '*logger.spaces, called))
            if logging_esi.console_handler.level <= logging_esi.TRACE:
                logger.spaces += 1
                log.spaces += 1
            retval = None
            try:
                retval = f(*args, **kwargs)
            except Fx as e:
                logger.warn(('%%10s %%s%%-%ds FAIL - %%s' % (35 - logger.spaces))
                            % ('TRACE:', ' '*logger.spaces, f.func_name, "%s %s" % (sp(), e.get_msg())))
                raise Fx('calling %s' % f.func_name)
            except:
                (exc_type, value, tb) = sys.exc_info()
                if exc_type == Ux:
                    logger.warn(('%%10s %%s%%-%ds EXCEPTION:      %%s: %%s' % (35 - logger.spaces))
                                % ('TRACE:', ' '*logger.spaces, f.func_name, value.__class__.__name__, value))
                else:
                    logger.warn(('%%10s %%s%%-%ds EXCEPTION:      %%s: %%s [%%s]' % (35 - logger.spaces))
                                % ('TRACE:', ' '*logger.spaces, f.func_name, value.__class__.__name__,
                                   '%s line %s in %s attempting "%s"' % traceback.extract_tb(tb)[1], value))
                if self.except_cb:
                    try:
                        self.except_cb(exc_type, value, tb)
                    except:
                        pass
                raise Ux('calling %s from %s' % (f.func_name, "%s:%s" % tuple(inspect.stack()[1][1:3])), False)
            finally:
                if logging_esi.console_handler.level <= logging_esi.TRACE:
                    logger.spaces -= 1
                    log.spaces -= 1
                if retval is not None:
                    returned = re_web_elem.sub(r'\1', repr(retval))
                    if len(returned) > 160:
                        returned = returned[:160] + "..."
                    logger.trace('%10s %s%s returned %s' % ('TRACE:', ' '*logger.spaces, f.func_name, returned))
            return retval
        return wrapped_f
