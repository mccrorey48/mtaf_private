import argparse
from time import sleep

import lib.logging_esi as logging_esi
from ePhone7.config.configure import cfg
from lib.softphone.simple_pj import Softphone

# process command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("site_tag", type=str, choices=['mm', 'mm_svlab'], help="specify site tag")
parser.add_argument('-c', '--cfg_host', help='name of mongodb server for test configuration, default "vqda"',
                    default='vqda')
args = parser.parse_args()
cfg.set_site(args.cfg_host, args.site_tag)

log = logging_esi.get_logger('esi.softphone2_test')
logging_esi.console_handler.setLevel(logging_esi.INFO)


# get account setup info from mongodb and create softphones
with logging_esi.msg_src_cm('creating softphones'):
    phones = []
    for user_tag in ['C', 'D', 'C']:
        user_name = 'Auto Tester' + user_tag
        user_cfg = cfg.site['Users'][user_name]
        uri = "sip:%s@%s" % (user_cfg['UserId'], user_cfg['DomainName'])
        phones.append(Softphone(uri, user_cfg['Proxy'], user_cfg['PhonePassword'], dns_list=cfg.site['DnsList'],
                                quiet=cfg.site['Quiet']))
    [p1, p2, p3] = phones


# make some calls:

def call_ring_answer(_caller, _called, auto_answer=True, holder=None, ender=p1):
    if auto_answer:
        _caller.make_call_to_softphone(_called.uri, 200)
        _caller.wait_for_call_status('call', warn_only=True)
    else:
        _caller.make_call_to_softphone(_called.uri, 180)
        _caller.wait_for_call_status('early', warn_only=True)
        sleep(5)
        _called.account_info.call.answer(200)
        _caller.wait_for_call_status('call', warn_only=True)
    sleep(10)
    if holder:
        holder.hold()
        sleep(5)
        holder.unhold()
    ender.end_call()
    _called.wait_for_call_status('idle', warn_only=True)
    sleep(1)


def call_hard_phone(_caller, dst_uri, duration):
    _caller.make_call(dst_uri)
    _caller.wait_for_call_status('call', warn_only=True)
    sleep(duration)
    _caller.end_call()
    sleep(1)

with logging_esi.msg_src_cm('test_0'):
    call_ring_answer(p1, p2, auto_answer=False, ender=p1)
# with logging_esi.msg_src_cm('test_1'):
#     call_ring_answer(p1, p2, ender=p1)
# with logging_esi.msg_src_cm('test_2'):
#     call_ring_answer(p1, p2, ender=p2)
# with logging_esi.msg_src_cm('test_3'):
#     call_ring_answer(p1, p2, holder=p1, ender=p1)
# with logging_esi.msg_src_cm('test_4'):
#     call_ring_answer(p1, p2, holder=p2, ender=p1)
# with logging_esi.msg_src_cm('test_5'):
#     call_ring_answer(p1, p2, holder=p1, ender=p2)
# with logging_esi.msg_src_cm('test_6'):
#     call_ring_answer(p1, p2, holder=p2, ender=p2)
# with logging_esi.msg_src_cm('test_7'):
#     call_hard_phone(p1, 'sip:1000@SVAutoCustomer', 10)
