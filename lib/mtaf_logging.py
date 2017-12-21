# wrapper for the python "logging" module
#
# Importing this module sets the logger class of the python "logging" module to MtafLogger.
# The MtafLogger class adds the "trace" level to logging.
#
# When this module is imported, MtafLogger is instantiated with the root name 'mtaf' and the instance
# sets up output to the console, and to the files mtaf_warn.log, mtaf_info.log, mtaf_trace.log and mtaf_debug.log.
#
# Then, when the importing program instantiates a new logger with the line:
#    log = logging_mtaf.get_logger(logname)
# where logname starts with "mtaf.". The methods log.warn, log.info, log.trace and log.debug create
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
from time import sleep, strftime, localtime
import re
from lib.prune_logs import prune_logs

msg_len_max = 30
msg_src_stack = []
msg_src = ''
root_name = 'mtaf'

TRACE = (DEBUG + INFO) / 2

current_formatter = None
trace_indent = 0


class MtafLogger(getLoggerClass()):

    def __init__(self, name, level=NOTSET):
        super(MtafLogger, self).__init__(name, level)
        addLevelName(TRACE, 'TRACE')

    def trace(self, msg, *args, **kwargs):
        if self.isEnabledFor(TRACE):
            self._log(TRACE, msg, args, **kwargs)


setLoggerClass(MtafLogger)


@contextmanager
def msg_src_cm(src):
    push_msg_src(src)
    yield
    pop_msg_src()


def update_handler_formatters(f):
    global current_formatter
    for handler in _log.handlers:
        handler.setFormatter(f)
        current_formatter = f


def push_msg_src(src):
    # save the previous msg_src
    msg_src_stack.append(msg_src)
    set_msg_src(src)


def pop_msg_src():
    if len(msg_src_stack) > 0:
        set_msg_src(msg_src_stack.pop())
    else:
        set_msg_src('')


def set_msg_src(src='', set_linefeed=False):
    global msg_len_max
    global msg_src
    if len(src) > msg_len_max:
        msg_len_max = len(src)
    msg_fmt = "%%-%ds" % (msg_len_max + 1)
    msg_src = src
    msg_src_formatted = msg_fmt % src
    format_str = '%%(asctime)s.%%(msecs)03d [%%(name)-20s] %%(levelname)-5s - [%s] %%(message)s' % msg_src_formatted
    formatter = Formatter(format_str, datefmt='%m/%d/%y %H:%M:%S')
    update_handler_formatters(formatter)
    if set_linefeed:
        # insert a linefeed to clean up the display in PyCharm
        print
        sleep(1)


def get_logger(name):
    return getLogger(name)


re_common = re.compile(
    '(?P<date>\S+)\s+'
    + '(?P<time>\S+)\s+\['
    + '(?P<src>[^\s\]]+)[\s\]]+'
    + '(?P<level>\S+)[\s\-\]\[]+'
    + '(?P<tc>\S[^\]]+\S)\s*\]\s+'
    + '((?P<type>[A-Z ^:]+):\s+)?'
    + '(?P<tail>.*)'
)

re_tc = re.compile(
    '(?P<tc>\S+)\s+'
    + '(?P<status>\S+)\s*'
    + '([- ]+)?(?P<msg>.+)?'
)

re_trace = re.compile(
    '(?P<func>[^(\s]+)'
    + '((?P<arglist>\((?P<args>.*)\))?\s*|\s*)'
    + '((?P<event>returned|EXCEPTION)?:?\s+|)(?P<msg>.+)?'
)


def parse_msg_to_dict(msg):
    m = re_common.match(msg)
    if not m:
        print 'Unknown log message format:\n%s' % msg
        return None
    names = ['date', 'time', 'src', 'level', 'tc', 'type']
    # names = ['date', 'time', 'src', 'level', 'tc', 'type', 'tail']
    values = [m.group(name) for name in names]
    # # print "tail = " + m.group('tail')
    if m.group('type') == 'TEST CASE':
        mt = re_tc.match(m.group('tail'))
        if not mt:
            print 'Unknown log message tail format: "%s"' % m.group('tail')
            return None
        for name in ['tc', 'status', 'msg']:
            names.append(name)
            values.append(mt.group(name))
    elif m.group('type') == 'TRACE':
        mt = re_trace.match(m.group('tail'))
        if not mt:
            print 'Unknown log message tail format: "%s"' % m.group('tail')
            return None
        for name in ('func', 'args', 'event', 'msg'):
            names.append(name)
            if name == 'event' and mt.group('arglist') is not None:
                values.append('call')
            else:
                values.append(mt.group(name))
    else:
        names.append('msg')
        values.append(m.group('tail'))
    all_values = dict(zip(names, values))
    all_values['trace_indent'] = trace_indent
    # print '  ' + ', '.join(['%s: %s' % (name, all_values[name]) for name in names])
    return all_values


_log = getLogger(root_name)
_log.setLevel(DEBUG)
prune_logs('log/%s_debug_*.log' % root_name, 5)
prune_logs('log/*logcat_*.log', 5)
timestamp = strftime('%m_%d_%y-%H_%M_%S', localtime())
# file logging for info, debug, trace and warn levels, each with its own output file
base_warn_fname = 'log/%s_warn.log' % root_name
base_info_fname = 'log/%s_info.log' % root_name
base_trace_fname = 'log/%s_trace.log' % root_name
base_debug_fname = 'log/%s_debug.log' % root_name
extended_debug_fname = 'log/%s_debug_%s.log' % (root_name, timestamp)
fh = FileHandler(base_warn_fname, mode='w', encoding=None, delay=False)
fh.setLevel(WARN)
_log.addHandler(fh)
fh = FileHandler(base_info_fname, mode='w', encoding=None, delay=False)
fh.setLevel(INFO)
_log.addHandler(fh)
fh = FileHandler(base_trace_fname, mode='w', encoding=None, delay=False)
fh.setLevel(TRACE)
_log.addHandler(fh)
fh = FileHandler(base_debug_fname, mode='w', encoding=None, delay=False)
fh.setLevel(DEBUG)
_log.addHandler(fh)
fh = FileHandler(extended_debug_fname, mode='w', encoding=None, delay=False)
fh.setLevel(DEBUG)
_log.addHandler(fh)
# console logging for info level
console_handler = StreamHandler()
console_handler.setLevel(INFO)
_log.addHandler(console_handler)
push_msg_src('logging_init')
