from lib.softphone.softphone import get_softphone
from time import sleep
import lib.common.logging_esi as logging_esi
from lib.common.configure import cfg
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("site_tag", help="site tag, selects config/site_<tag>.json file")
parser.add_argument("--failfast", help="stop testing when a test case fails", action="store_true")
parser.add_argument("--mock", help="stop testing when a test case fails", action="store_true")
args = parser.parse_args()

cfg.set_site(args.site_tag)

log = logging_esi.get_logger('esi.softphone_test')
logging_esi.console_handler.setLevel(logging_esi.TRACE)
softphone = get_softphone()
r2d2_id = cfg.site['Accounts']['R2d2User']['UserId']
r2d2_domain = cfg.site['Accounts']['R2d2User']['DomainName']
softphone.make_call('sip:%s@%s' % (r2d2_id, r2d2_domain))
softphone.wait_for_call_status('early', 20)
# # softphone.set_monitor_on()
sleep(5)
# # softphone.dial_dtmf('2')
# # sleep(15)
# # softphone.set_monitor_off()
softphone.teardown_call()
# sleep(5)
