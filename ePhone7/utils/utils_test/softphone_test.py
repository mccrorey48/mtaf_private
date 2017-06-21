from ePhone7.utils.get_softphone import get_softphone
from time import sleep
import lib.logging_esi as logging_esi
from ePhone7.config.configure import cfg

log = logging_esi.get_logger('esi.softphone_test')

logging_esi.console_handler.setLevel(logging_esi.TRACE)
called = get_softphone('Auto TesterD')
called.set_incoming_response(None)
caller = get_softphone('Auto TesterC')
log.debug("2202 making call")
caller.make_call(called.uri)
sleep(5)
log.debug("2203 sending 100")
called.send_response_code(100)
sleep(5)
log.debug("2203 sending 180")
called.send_response_code(180)
sleep(5)
log.debug("2203 sending 200")
called.send_response_code(200)
sleep(5)
log.debug("2203 executing hold")
called.hold()
sleep(5)
log.debug("2203 executing unhold")
called.unhold()
sleep(5)
log.debug("2202 ending call")
caller.end_call()

