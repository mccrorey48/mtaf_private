from mtaf.simple_pj import SoftphoneManager
from time import sleep
from mtaf import mtaf_logging
from mtaf.user_exception import UserException as Ux
from ePhone7.views import *
from ePhone7.config.configure import cfg
import six

log = mtaf_logging.get_logger('mtaf.softphone_test')

mtaf_logging.console_handler.setLevel(mtaf_logging.TRACE)

softphone_manager = SoftphoneManager()

e7_uri = 'sip:2016@test2.test-eng.com'


def call_e7_from_softphone(_sp, short_call=False):
    _sp.make_call(e7_uri)
    _sp.wait_for_call_status('call', timeout=30)
    try:
        if not short_call:
            # if not user_view.incoming_call_screen_is_present():
            #     raise Ux("incoming call screen not present when ePhone7 is being called")
            sleep(10)
    except Ux:
        raise
    finally:
        _sp.end_call()
        _sp.wait_for_call_status('idle', timeout=10)
    # sleep(5)


def call_softphone_from_e7(_sp):
    sleep(10)
    dial_view.dial_number(sp_user_id)
    dial_view.touch_dial_button()
    _sp.wait_for_call_status('early', timeout=30)
    sleep(10)
    active_call_view.touch_end_call_button()
    _sp.wait_for_call_status('idle', timeout=10)
    sleep(10)


def short_long_call_loop():
    try:
        sp = softphone_manager.get_softphone(uri, proxy, password, null_snd, dns_list, tcp)
        sp.set_incoming_response(200)
        if sp.account_info.reg_status != 200:
            raise Ux("%s reg status = %s, exiting" % sp.account_info.reg_status)
        base_view.open_appium()
        sleep(10)
        call_count = 0
        # while True:
        for i in range(18):
            # if not user_view.becomes_present():
            #     log.info("Restarting Appium")
            #     base_view.close_appium()
            #     sleep(10)
            #     base_view.open_appium()
            #     sleep(10)
            try:
                call_count += 1
                # user_view.goto_tab('Dial')
                # call_softphone_from_e7()
                # call_e7_from_softphone()
                if call_count % 6 == 0:
                    log.info("making normal call")
                    call_e7_from_softphone(sp)
                else:
                    log.info("making short call")
                    call_e7_from_softphone(sp, short_call=True)
            except Ux as e:
                log.info("got user exception: %s" % e)
    except KeyboardInterrupt:
        six.print_("\rgot keyboard interrupt")
    finally:
        user_view.close_appium()


if __name__ == "__main__":
    sp_user_name = cfg.site['DefaultSoftphoneUser']
    sp_user_cfg = cfg.site['Users'][sp_user_name]
    sp_user_id = sp_user_cfg['UserId']
    uri = "sip:%s@%s" % (sp_user_id, sp_user_cfg['DomainName'])
    proxy = sp_user_cfg['Proxy']
    # proxy = 'nms-01.hs.cs.lax01.esihs.net'
    password = sp_user_cfg['PhonePassword']
    null_snd = cfg.site['NullSound']
    dns_list = cfg.site['DnsList']
    tcp = cfg.site['UseTcp']
    call_e7_from_softphone(softphone_manager.get_softphone(uri, proxy, password, null_snd, dns_list, tcp))
