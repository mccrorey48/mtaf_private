from ePhone7.utils.get_softphone import get_softphone
from time import sleep, time
import lib.logging_esi as logging_esi
from ePhone7.config.configure import cfg

log = logging_esi.get_logger('esi.softphone_test')

first_user = 60
max_user_count = 58
call_length = 600
recording_length = 60

# production_proxy_override = 'nms-21.hs.cs.jfk01.esihs.net'
# production_proxy_override = None

# if cfg.site_tag == 'mm':
#     proxy_override = production_proxy_override
# else:
proxy_override = None
phones = {}
logging_esi.console_handler.setLevel(logging_esi.TRACE)
# users = sorted(cfg.site["DrsTestUsers"].keys())
users = []
for i in range(first_user, first_user + max_user_count):
    users.append('DRS tester%03d' % i)
softphone_pairs = []
# for index in range(0, len(users), 2):
for index in range(0, max_user_count, 2):
    if index > len(users):
        break
    caller_name = users[index]
    called_name = users[(index + 1) % len(users)]
    log.warn("%s --> %s" % (caller_name, called_name))
    caller = get_softphone(caller_name, user_group="DrsTestUsers", reg_wait=False, proxy_override=proxy_override)
    called = get_softphone(called_name, user_group="DrsTestUsers", reg_wait=False, proxy_override=proxy_override)
    sleep(0.2)
    softphone_pairs.append({"caller": caller, "called": called})
sleep(10)
for pair in softphone_pairs:
    pair["called"].set_incoming_response(200)
    pair["caller"].make_call(pair["called"].uri)
    sleep(0.2)
call_time_left = call_length
rec_save_index = 0
while call_time_left > 0:
    sleep_time = min(recording_length, call_time_left)
    sleep(sleep_time)
    call_time_left -= sleep_time
    if call_time_left > 0:
        rec_save_index += 1
        for pair in softphone_pairs:
            pair['caller'].restart_recorder('rec_%s_%d.wav' % (pair['caller'].account_info.number, rec_save_index))
            pair['called'].restart_recorder('rec_%s_%d.wav' % (pair['caller'].account_info.number, rec_save_index))

for pair in softphone_pairs:
    log.warn("caller %s call time: %s" % (pair["caller"].account_info.uri,
                                          time() - pair["caller"].account_info.call_start_time))
    log.warn("called %s call time: %s" % (pair["called"].account_info.uri,
                                          time() - pair["called"].account_info.call_start_time))
    pair["caller"].end_call()
    pair["called"].wait_for_call_status('idle', 15)
for pair in softphone_pairs:
    pair["caller"].unregister()
    pair["called"].unregister()
    sleep(0.2)
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

