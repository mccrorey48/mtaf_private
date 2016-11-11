import argparse
import os
from lib.softphone.softphone2 import Softphone, SoftphoneConfig
from ePhone7.utils.configure import cfg
from lib.softphone.simple_pj import media_state_text, call_state_text

parser = argparse.ArgumentParser()
parser.add_argument("site_tag", type=str, choices=['mm', 'js', 'local'], help="specify site tag")
parser.add_argument('-c', '--cfg_host', help='name of mongodb server for test configuration, default "vqda"',
                    default='vqda')
args = parser.parse_args()
cfg.set_site(args.cfg_host, args.site_tag)

from time import sleep
import lib.logging_esi as logging_esi
from ePhone7.utils.configure import cfg
log = logging_esi.get_logger('esi.softphone2_test')
logging_esi.console_handler.setLevel(logging_esi.TRACE)

cfg.set_site('vqda', 'alpha')


def on_incoming_call_cb(acct_info):
    uri = acct_info.account.info().uri
    log.info('%s: on_incoming_call_cb (ignoring)' % uri)


def on_state_cb(acct_info):
    uri = acct_info.account.info().uri
    log.info('on_state_cb: uri=%s, state=%s, media_state=%s' % (uri, call_state_text[acct_info.state],
                                                                media_state_text[acct_info.media_state]))

user_cfg = cfg.site['Users']['Auto TesterC']
uri = "sip:%s@%s" % (user_cfg['UserId'], user_cfg['DomainName'])
softphone_config = SoftphoneConfig(uri, user_cfg['Proxy'], user_cfg['Password'], dns_list=user_cfg['dns_list'])
caller = Softphone(softphone_config)

user_cfg = cfg.site['Users']['Auto TesterD']
pbfile = os.path.join('wav', '%s.wav' % user_cfg['UserId'])
uri = "sip:%s@%s" % (user_cfg['UserId'], user_cfg['DomainName'])
softphone_config = SoftphoneConfig(uri, user_cfg['Proxy'], user_cfg['Password'], null_snd=True,
                                   dns_list=user_cfg['dns_list'], tcp=False, pbfile=pbfile)
called = Softphone(softphone_config)
called.account_info.on_state_cb = on_state_cb
called.account_info.on_incoming_call_cb = on_incoming_call_cb
caller.make_call('sip:2201@test1.test-eng.com')
caller.wait_for_call_status('early', 20)
sleep(5)
caller.end_call()
