from ePhone7.utils.get_softphone import get_softphone
from time import sleep
import lib.logging_esi as logging_esi
from ePhone7.config.configure import cfg

log = logging_esi.get_logger('esi.softphone_test')

phones = {}
logging_esi.console_handler.setLevel(logging_esi.TRACE)
users = sorted(cfg.site["DrsTestUsers"].keys())
for index in range(0, len(users), 2):
    caller_name = users[index]
    called_name = users[(index + 2) % len(users)]
    print "%s --> %s" % (caller_name, called_name)
    caller = get_softphone(caller_name, user_group="DrsTestUsers")
    called = get_softphone(called_name, user_group="DrsTestUsers")
    if caller.account_info.reg_status != 200:
        print "%s reg status = %s, exiting" % (caller_name, caller.account_info.reg_status)
        break
    if called.account_info.reg_status != 200:
        print "%s reg status = %s, exiting" % (called_name, called.account_info.reg_status)
        break
    called.set_incoming_response(200)
    caller.make_call(called.uri)
    sleep(5)
    caller.end_call()
    called.wait_for_call_status('idle', 15)
    caller.unregister()
    called.unregister()
    sleep(2)
# called.send_response_code(100)
# sleep(5)
# log.debug("2203 sending 180")
# called.send_response_code(180)
# sleep(5)
# log.debug("2203 sending 200")
# called.send_response_code(200)
# sleep(5)
# log.debug("2203 executing hold")
# called.hold()
# sleep(5)
# log.debug("2203 executing unhold")
# called.unhold()
# sleep(5)
# log.debug("2202 ending call")

