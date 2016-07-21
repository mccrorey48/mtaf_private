import argparse
from lib.common.configure import cfg

parser = argparse.ArgumentParser()
parser.add_argument("dir_name", type=str, choices=['ePhone7', 'ePhoneGo-android', 'ePhoneGo-iOS'],
                    help="specify name of product directory")
parser.add_argument("site_tag", type=str, choices=['mm', 'js', 'local'], help="specify site tag")
args = parser.parse_args()
cfg.set_site(args.dir_name, args.site_tag)

from lib.softphone.softphone import get_softphone
from time import sleep
import lib.common.logging_esi as logging_esi
from lib.common.configure import cfg

log = logging_esi.get_logger('esi.softphone_test')
logging_esi.console_handler.setLevel(logging_esi.TRACE)
softphone = get_softphone('Auto TesterC')
softphone2 = get_softphone('Auto TesterD')
r2d2_id = cfg.site['Accounts']['R2d2User']['UserId']
r2d2_domain = cfg.site['Accounts']['R2d2User']['DomainName']
s2_id = cfg.site['Accounts']['Auto TesterD']['UserId']
s2_domain = cfg.site['Accounts']['Auto TesterD']['DomainName']
softphone.make_call('sip:%s@%s' % (s2_id, s2_domain))
#softphone.wait_for_call_status('early', 20)
softphone.wait_for_call_status('start', 20)
# # softphone.set_monitor_on()
sleep(5)
# # softphone.dial_dtmf('2')
# # sleep(15)
# # softphone.set_monitor_off()
softphone.teardown_call()
# sleep(5)
# softphone2.make_call('sip:%s@%s' % (r2d2_id, r2d2_domain))
# softphone2.wait_for_call_status('early', 20)
# # # softphone.set_monitor_on()
# sleep(5)
# # # softphone.dial_dtmf('2')
# # # sleep(15)
# # # softphone.set_monitor_off()
# softphone2.teardown_call()
# # sleep(5)
