# wrapper for the python "logging" module
#
# Importing this module sets the logger class of the python "logging" module to EsiLogger.
# The EsiLogger class adds the "trace" level to logging.
#
# When this module is imported, EsiLogger is instantiated with the root name 'esi' and the instance
# sets up output to the console, and to the files esi_warn.log, esi_info.log, esi_trace.log and esi_debug.log.
#
# Then, when the importing program instantiates a new logger with the line:
#    log = logging_esi.get_logger(logname)
# where logname starts with "esi.", the methods log.warn, log.info, log.trace and log.debug create
# formatted output to the log files.
#
# The log levels used here correspond to the following symbolic names and values:
#
#    warn        logging.WARN       30
#    info        logging.INFO       20
#    trace       logging.TRACE      15
#    debug       logging.DEBUG      10
#
# Lower-level output files will include log output from higher levels.


from logging import getLoggerClass, addLevelName, setLoggerClass, NOTSET, DEBUG, INFO, WARN
from logging import Formatter, FileHandler, getLogger, StreamHandler
from contextlib import contextmanager
from time import sleep

msg_len_max = 33
msg_src_stack = []
msg_src = ''
root_name = 'esi'

TRACE = (DEBUG + INFO) / 2


class EsiLogger(getLoggerClass()):
    spaces = 0

    def __init__(self, name, level=NOTSET):
        super(EsiLogger, self).__init__(name, level)
        addLevelName(TRACE, 'TRACE')

    def trace(self, msg, *args, **kwargs):
        if self.isEnabledFor(TRACE):
            self._log(TRACE, msg, args, **kwargs)

setLoggerClass(EsiLogger)

@contextmanager
def msg_src_cm(src):
    push_msg_src(src)
    yield
    pop_msg_src()


def update_handler_formatters(f):
    for handler in _log.handlers:
        handler.setFormatter(f)


def push_msg_src(src):
    # save the previous msg_src
    msg_src_stack.append(msg_src)
    set_msg_src(src)


def pop_msg_src():
    if len(msg_src_stack) > 0:
        set_msg_src(msg_src_stack.pop())
    else:
        set_msg_src('')


def set_msg_src(src='', set_linefeed=False, show_lineno=True):
    global msg_len_max
    global msg_src
    if len(src) > msg_len_max:
        # print "src = '%s', len(src) = %d, msg_len_max = %d" % (src, len(src), msg_len_max)
        msg_len_max = len(src)
    msg_fmt = "%%-%ds" % (msg_len_max + 1)
    msg_src = src
    msg_src_formatted = msg_fmt % src
    # if show_lineno:
    #     lineno_fmt = '%(module)s'
    # else:
    lineno_fmt = ''
    format_str = '%%(asctime)s.%%(msecs)03d [%%(name)-25s] %%(levelname)-7s - [%s%s] %%(message)s' % \
                 (msg_src_formatted, lineno_fmt)
    formatter = Formatter(format_str, datefmt='%m/%d/%y %H:%M:%S')
    update_handler_formatters(formatter)
    if set_linefeed:
        # insert a linefeed to clean up the display in PyCharm
        print
        sleep(1)

_log = getLogger(root_name)
_log.setLevel(DEBUG)
# file logging for info, debug, trace and warn levels, each with its own output file
fh = FileHandler('log/%s_debug.log' % root_name, mode='w', encoding=None, delay=False)
fh.setLevel(DEBUG)
_log.addHandler(fh)
fh = FileHandler('log/%s_trace.log' % root_name, mode='w', encoding=None, delay=False)
fh.setLevel(TRACE)
_log.addHandler(fh)
fh = FileHandler('log/%s_info.log' % root_name, mode='w', encoding=None, delay=False)
fh.setLevel(INFO)
_log.addHandler(fh)
fh = FileHandler('log/%s_warn.log' % root_name, mode='w', encoding=None, delay=False)
fh.setLevel(WARN)
_log.addHandler(fh)
# console logging for info level
console_handler = StreamHandler()
console_handler.setLevel(INFO)
_log.addHandler(console_handler)
push_msg_src('logging_init')


def get_logger(name):
    return getLogger(name)


if __name__ == '__main__':
    log = get_logger('esi.mm')
    log.info("hello")
    push_msg_src('just a test')
    log.info("world")
    pop_msg_src()
    log.info("goodbye")
