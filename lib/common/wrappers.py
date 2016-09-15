from lib.common.user_exception import UserException as Ux, UserFailException as Fx, stat_prefix as sp
import lib.common.logging_esi as logging_esi
import sys
import traceback
import inspect
import appium
from time import time

log = logging_esi.get_logger('esi.wrappers')


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


# spaces = 0

class Trace(object):

    def __init__(self, logger=None, except_cb=None):
        """
        If there are decorator arguments, the function
        to be decorated is not passed to the constructor!
        """
        self.logger = logger
        self.except_cb = except_cb

    def prefix(self):
        indent = logging_esi.trace_indent
        return 'TRACE%d:%s' % (indent, ' '*indent)

    def __call__(self, f):
        """
        If there are decorator arguments, __call__() is only called
        once, as part of the decoration process! You can only give
        it a single argument, which is the function object.
        """

        def wrapped_f(*args, **kwargs):
            # global spaces
            if self.logger is None:
                logger = log
            else:
                logger = self.logger
            arg_reprs = []
            for arg in args:
                if type(arg) == appium.webdriver.webelement.WebElement:
                    arg_reprs.append('<%s>' % arg._id)
                else:
                    arg_reprs.append(repr(arg))
            called = "%s%s" % (f.func_name, '(%s)' % ','.join(arg_reprs))
            logger.trace("%10s %s" % (self.prefix(), called))
            logging_esi.trace_indent += 1
            retval = None
            elapsed_time = 0.0
            try:
                start_time = time()
                retval = f(*args, **kwargs)
                elapsed_time = time() - start_time
            except Fx as e:
                logger.warn(('%%10s %%s%%-%ds FAIL - %%s' % (35 - logging_esi.trace_indent))
                            % (self.prefix(), f.func_name, "%s %s" % (sp(), e.get_msg())))
                raise Fx('calling %s' % f.func_name)
            except:
                (exc_type, value, tb) = sys.exc_info()
                if exc_type == Ux:
                    logger.warn(('%%10s %%-%ds EXCEPTION:      %%s: %%s' % (35 - logging_esi.trace_indent))
                                % (self.prefix(), f.func_name, value.__class__.__name__, value))
                else:
                    logger.warn(('%%10s %%-%ds EXCEPTION:      %%s: %%s [%%s]' % (35 - logging_esi.trace_indent))
                                % (self.prefix(), f.func_name, value.__class__.__name__,
                                   '%s line %s in %s attempting "%s"' % traceback.extract_tb(tb)[1], value))
                if self.except_cb:
                    try:
                        self.except_cb(exc_type, value, tb)
                    except:
                        pass
                raise Ux('calling %s from %s' % (f.func_name, "%s:%s" % tuple(inspect.stack()[1][1:3])), False)
            finally:
                logging_esi.trace_indent -= 1
                val_reprs = []
                if retval is None:
                    logger.trace('%10s %s returned [%.3fs]' % (self.prefix(), f.func_name, elapsed_time))
                else:
                    if type(retval) == list:
                        for val in retval:
                            if type(val) == appium.webdriver.webelement.WebElement:
                                val_reprs.append('<%s>' % val._id)
                            else:
                                val_reprs.append(repr(val))
                        returned = '[%s]' % ','.join(val_reprs)
                    else:
                        if type(retval) == appium.webdriver.webelement.WebElement:
                            returned = '<%s>' % retval._id
                        else:
                            returned = repr(retval)
                    if len(returned) > 160:
                        returned = returned[:160] + "..."
                    logger.trace('%10s %s returned %s [%.3fs]' % (self.prefix(), f.func_name, returned, elapsed_time))
            return retval
        return wrapped_f
