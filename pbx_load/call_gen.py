from lib.softphone.simple_pj import SoftphoneManager
from csv import DictReader
from time import sleep, time
import os
from ePhone7.config.configure import cfg

# MAX_USERS = 116
MAX_USERS = 30
# CALL_LENGTH = 120
# MAX_USERS = 4
CALL_LENGTH = 10

softphone_manager = SoftphoneManager()
null_snd = True
tcp = False

cfgs = {}
i = 0
#
# asterisk pbx
#
dns_list = ["10.0.50.156", "10.0.50.157"]
for i in range(MAX_USERS):
    username = 'DRS tester%02d' % i
    user_cfg = cfg.site['DrsTestUsers'][username]
    cfgs[username] = [
        "sip:%s@%s" % (user_cfg['UserId'], user_cfg['DomainName']),
        user_cfg['Proxy'],
        user_cfg['PhonePassword'],
        null_snd,
        dns_list,
        tcp
    ]
# proxy = '192.64.95.85'
# domain = '192.64.95.85'
# with open(os.path.join('pbx_load', 'users.csv')) as f:
#     users = DictReader(f)
#     for i, user in enumerate(users):
#         if i == MAX_USERS:
#             break
#         cfgs[user['username']] = [
#             "sip:%s@%s" % (user['username'], domain),
#             proxy,
#             user['registerpassword'],
#             null_snd,
#             dns_list,
#             tcp,
#             ]
# #
# production drs-test users
# proxy = 'nr5.cpbx.esihs.net'
# csv_file = 'pro_users_concurrent_csv'
# lab drs-test users
# proxy = 'svlab.esihs.net'
# csv_file = 'lab_users_concurrent.csv'
# dns_list = ["10.0.50.156", "10.0.50.157"]
# with open(os.path.join('pbx_load', csv_file)) as f:
#     users = DictReader(f)
#     for i, user in enumerate(users):
#         if i == MAX_USERS:
#             break
#         cfgs[user['name']] = [
#             "sip:%s@%s" % (user['name'], user['domain']),
#             proxy,
#             user['password'],
#             null_snd,
#             dns_list,
#             tcp,
#         ]

MAX_USERS = i + 1

MAX_CALLS = int(MAX_USERS / 2)

print MAX_CALLS, "calls,", MAX_USERS, "users"

softphones = {}

users = sorted(cfgs.keys())

for user in users:
    # print cfgs[user]
    softphones[user] = softphone_manager.get_softphone(*cfgs[user])
    sleep(0.5)

sleep(5)

import lib.logging_esi as logging_esi

log = logging_esi.get_logger('esi.call_gen')
logging_esi.console_handler.setLevel(logging_esi.TRACE)


softphone_pairs = []
for index in range(MAX_CALLS):
    caller_name = users[index * 2]
    called_name = users[((index * 2) + 1) % len(users)]
    log.info("%s calling %s" % (caller_name, called_name))
    softphone_pairs.append({"caller": softphones[caller_name], "called": softphones[called_name]})
for pair in softphone_pairs:
    pair["called"].set_incoming_response(200)
    pair["caller"].make_call(pair["called"].uri)
    pair["caller"].wait_for_call_status('call', timeout=10)
    pair["called"].wait_for_call_status('call', timeout=10)
sleep(CALL_LENGTH)
for pair in softphone_pairs:
    if pair["caller"].account_info.call_start_time is None:
        log.warn("caller %s call did not complete" % pair["caller"].account_info.uri)
    else:
        log.warn("caller %s call time: %s" % (pair["caller"].account_info.uri,
                                              time() - pair["caller"].account_info.call_start_time))
    if pair["caller"].account_info.call_start_time is None:
        log.warn("called %s call did not complete" % pair["called"].account_info.uri)
    else:
        log.warn("called %s call time: %s" % (pair["called"].account_info.uri,
                                          time() - pair["called"].account_info.call_start_time))
    pair["caller"].end_call()
    pair["called"].wait_for_call_status('idle', 15)
for user in users:
    softphones[user].unregister()
sleep(5)
