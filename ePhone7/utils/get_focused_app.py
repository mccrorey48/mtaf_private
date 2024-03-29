from ePhone7.utils.spud_serial import SpudSerial
from ePhone7.config.configure import cfg
import lib.logging_esi as logging
from lib.user_exception import UserException as Ux
from lib.wrappers import Trace
log = logging.get_logger('esi.get_focused_app')


@Trace(log)
def get_focused_app():
    ss = SpudSerial(cfg.site['SerialDev'], pwd_check=False)
    action = {'cmd': 'dumpsys window windows\n',
              'timeout': 15,
              'expect': 'mFocusedApp.+Record\{.*\s(\S+)\s+\S+\}',
              'new_cwd': None}
    try:
        (reply, elapsed, groups) = ss.do_action(action)
        flushed = ss.flush(timeout=1)[0]
        for line in flushed.split('\n'):
            log.debug('flushed: %s' % line.encode('string_escape'))
        log.info('focused app: %s' % groups[1].encode('string_escape'))
        return groups[1]
    except Ux:
        return "Focused App Not Found"
