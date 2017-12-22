import lib.mtaf_logging as mtaf_logging
from lib.user_exception import UserException as Ux
from lib.trace import Trace, SkipTrace
log = mtaf_logging.get_logger('mtaf.trace_test')
mtaf_logging.console_handler.setLevel(mtaf_logging.INFO)
# Trace = SkipTrace


@Trace(log)
def f1(*args):
    return f2(args[0])


@Trace(log)
def f2(arg):
    if arg == 'a':
        return f3(arg)
    return f4(arg)


@Trace(log)
def f3(arg):
    raise Ux('f3 user exception here, arg=%s' % arg)


@Trace(log)
def f4(arg):
    l = []
    log.debug('causing a list index out of range error')
    return l[arg]


run_list = ['test_1_trace_f3']


f3('a')

