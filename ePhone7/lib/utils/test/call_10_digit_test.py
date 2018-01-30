from mtaf.simple_pj import SoftphoneManager
from time import sleep
from mtaf import mtaf_logging
from mtaf.user_exception import UserException as Ux, UserTimeoutException as Tx
from ePhone7.config.configure import cfg

log = mtaf_logging.get_logger('mtaf.softphone_test')

mtaf_logging.console_handler.setLevel(mtaf_logging.WARN)

softphone_manager = SoftphoneManager()

e7_uri = 'sip:9727559925@test2.test-eng.com'
sp_user_name = cfg.site['DefaultSoftphoneUser']
sp_user_cfg = cfg.site['Users'][sp_user_name]
sp_user_id = sp_user_cfg['UserId']
uri = "sip:%s@%s" % (sp_user_id, sp_user_cfg['DomainName'])
# proxy = sp_user_cfg['Proxy']
proxy = 'nms-01.hs.cs.lax01.esihs.net'
password = sp_user_cfg['PhonePassword']
null_snd = cfg.site['NullSound']
dns_list = cfg.site['DnsList']
tcp = cfg.site['UseTcp']

max_calls = 200


def call_e7_from_softphone(short_call=False, connect_timeout=15, call_duration=120):
    sp.make_call(e7_uri)
    try:
        secs = sp.wait_for_call_status('call', timeout=connect_timeout)
    except Tx:
        log.warn("call did not connect in %s seconds, ending call" % connect_timeout)
        sp.end_call()
    else:
        log.warn("call connected in %s seconds" % secs)
        try:
            secs = sp.wait_for_call_status('idle', timeout=call_duration)
        except Tx:
            sp.end_call()
            duration = call_duration
        else:
            duration = secs
        log.warn("call duration was %s seconds" % duration)
    sleep(5)


try:
    sp = softphone_manager.get_softphone(uri, proxy, password, null_snd, dns_list, tcp)
    sp.set_incoming_response(200)
    if sp.account_info.reg_status != 200:
        raise Ux("%s reg status = %s, exiting" % sp.account_info.reg_status)
    for i in range(max_calls):
        try:
            call_e7_from_softphone()
            sleep(5)
        except Ux as e:
            log.info("got user exception: %s" % e)
except KeyboardInterrupt:
    print "\rgot keyboard interrupt"

