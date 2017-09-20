from lib.softphone.simple_pj import SoftphoneManager
import time
from time import sleep
import lib.logging_esi as logging_esi
from lib.user_exception import UserException as Ux
from ePhone7.views import *
from ePhone7.config.configure import cfg

log = logging_esi.get_logger('esi.softphone_test')

logging_esi.console_handler.setLevel(logging_esi.TRACE)

softphone_manager = SoftphoneManager()

e7_uri = 'sip:2011@test2.test-eng.com'
sp_user_name = cfg.site['DefaultSoftphoneUser']
sp_user_cfg = cfg.site['Users'][sp_user_name]
sp_user_id = sp_user_cfg['UserId']
uri = "sip:%s@%s" % (sp_user_id, sp_user_cfg['DomainName'])
proxy = sp_user_cfg['Proxy']
password = sp_user_cfg['PhonePassword']
null_snd = cfg.site['NullSound']
dns_list = cfg.site['DnsList']
tcp = cfg.site['UseTcp']
sp = softphone_manager.get_softphone(uri, proxy, password, null_snd, dns_list, tcp)
sp.set_incoming_response(200)


def call_e7_from_softphone():
    sp.make_call(e7_uri)
    sleep(10)
    sp.end_call()
    sleep(20)


def call_softphone_from_e7():
    user_view.open_appium()
    sleep(10)
    # user_view.startup()
    user_view.goto_tab('Dial')
    dial_view.dial_number(sp_user_id)
    dial_view.touch_dial_button()
    sleep(10)
    active_call_view.touch_end_call_button()
    sp.wait_for_call_status('idle', timeout=10)
    sleep(5)
    user_view.close_appium()
    sleep(20)


# if softphone.account_info.reg_status != 200:
#     raise Ux("%s reg status = %s, exiting" % softphone.account_info.reg_status)
while True:
    try:
        call_e7_from_softphone()
        call_softphone_from_e7()
    except Ux as e:
        log.info("got user exception: %s" % e)
