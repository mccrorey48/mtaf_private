import argparse
import os
from lib.softphone.simple_pj import Softphone
from lib.user_exception import UserTimeoutException as Tx
from ePhone7.utils.configure import cfg
from lib.softphone.simple_pj import media_state_text, call_state_text
from time import sleep

parser = argparse.ArgumentParser()
parser.add_argument("site_tag", type=str, choices=['mm', 'js', 'local'], help="specify site tag")
parser.add_argument('-c', '--cfg_host', help='name of mongodb server for test configuration, default "vqda"',
                    default='vqda')
args = parser.parse_args()
cfg.set_site(args.cfg_host, args.site_tag)

import lib.logging_esi as logging_esi
from ePhone7.utils.configure import cfg
log = logging_esi.get_logger('esi.softphone2_test')
logging_esi.console_handler.setLevel(logging_esi.INFO)


def on_incoming_call_answer(acct_info):
    _uri = acct_info.account.info().uri
    log.info('%s: on_incoming_call_cb (sending 200 OK)' % _uri)
    acct_info.call.answer(200)


def on_incoming_call_ring(acct_info):
    _uri = acct_info.account.info().uri
    log.info('%s: on_incoming_call_cb (sending 180)' % _uri)
    acct_info.call.answer(180)


def on_incoming_call_ignore(acct_info):
    _uri = acct_info.account.info().uri
    log.info('%s: on_incoming_call_cb (ignoring)' % _uri)


def on_state_cb(acct_info):
    _uri = acct_info.account.info().uri
    log.info('on_state_cb: uri=%s, state=%s, media_state=%s' % (_uri, call_state_text[acct_info.state],
                                                                media_state_text[acct_info.media_state]))

user_cfg = cfg.site['Users']['Auto TesterC']
uri = "sip:%s@%s" % (user_cfg['UserId'], user_cfg['DomainName'])
caller = Softphone(uri, user_cfg['Proxy'], user_cfg['Password'], dns_list=user_cfg['dns_list'])
caller.account_info.on_state_cb = on_state_cb
caller.account_info.on_incoming_call_cb = on_incoming_call_ring

user_cfg = cfg.site['Users']['Auto TesterD']
pbfile = os.path.join('wav', '%s.wav' % user_cfg['UserId'])
uri = "sip:%s@%s" % (user_cfg['UserId'], user_cfg['DomainName'])
called = Softphone(uri, user_cfg['Proxy'], user_cfg['Password'], null_snd=True,
                   dns_list=user_cfg['dns_list'], tcp=False, pbfile=pbfile)
called.account_info.on_state_cb = on_state_cb
called.account_info.on_incoming_call_cb = on_incoming_call_ring
caller.make_call(called.uri)
try:
    caller.wait_for_call_status('early', 20)
except Tx as e:
    log.warn(e.msg)
sleep(5)
called.account_info.call.answer(200)
try:
    caller.wait_for_call_status('call', 20)
except Tx as e:
    log.warn(e.msg)
sleep(5)
caller.end_call()
