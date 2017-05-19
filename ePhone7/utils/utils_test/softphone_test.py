from ePhone7.utils.get_softphone import get_softphone
from time import sleep
import lib.logging_esi as logging_esi
from ePhone7.config.configure import cfg

log = logging_esi.get_logger('esi.softphone_test')
logging_esi.console_handler.setLevel(logging_esi.TRACE)
softphone_alt = get_softphone('R2d2AltUser')
softphone_alt.set_incoming_response(200)
softphone = get_softphone('Auto TesterC')
user_id = cfg.site['Users']['R2d2User']['UserId']
domain_name = cfg.site['Users']['R2d2User']['DomainName']
softphone.make_call('sip:%s@%s' % (user_id, domain_name))
sleep(10)
softphone.end_call()
