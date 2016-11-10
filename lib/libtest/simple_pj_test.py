import time
import lib.softphone.simple_pj as pj
import lib.logging_esi as logging_esi

send_180 = True

log = logging_esi.get_logger('esi.simple_pj_test')
# set console log level
logging_esi.console_handler.setLevel(logging_esi.INFO)


def on_incoming_call_cb(acct):
    uri = acct.account.info().uri
    log.info('on_incoming_call_cb: uri=%s, answering with 200' % uri)
    acct.call.answer(200)


def on_state_cb(acct):
    state = pj.call_state_text[acct.state]
    media_state = pj.media_state_text[acct.media_state]
    uri = acct.account.info().uri
    log.info('on_state_cb: uri=%s, state=%s, media_state=%s' % (uri, state, media_state))

lib = pj.PjsuaLib()
log.debug('starting pjsua library')
with logging_esi.msg_src_cm('start pjsua'):
    lib.start(dns_list=['10.0.50.156', '10.0.50.157'])
log.debug('adding accounts')
with logging_esi.msg_src_cm('add accounts'):
    lib.add_account('2202', 'test2.test-eng.com', 'nr5.cpbx.esihs.net', 'vsvSIHpL')
    lib.add_account('2203', 'test2.test-eng.com', 'nr5.cpbx.esihs.net', 'TSDlprSD')
    caller = lib.accounts['sip:2202@test2.test-eng.com']
    caller.on_state_cb = on_state_cb
    called = lib.accounts['sip:2203@test2.test-eng.com']
    called.on_state_cb = on_state_cb
    called.on_incoming_call_cb = on_incoming_call_cb
log.debug('making a call from 2202 to 2203')
with logging_esi.msg_src_cm('make call'):
    caller.call = caller.account.make_call('sip:2203@test2.test-eng.com')
    caller.call.set_callback(pj.MyCallCallback(caller))
    for i in range(10):
        if called.call:
            if send_180:
                log.debug('called ringing (180)')
                called.call.answer(180)
                send_180 = False
            if i == 10:
                log.debug('called answering (200)')
                called.call.answer(200)
            if i == 15:
                log.debug('called hanging up')
                caller.call.hangup()
        time.sleep(1)
    log.debug('caller hanging up')
    caller.call.hangup()
log.debug('destroying pjsua library')
with logging_esi.msg_src_cm('destroy pjsua'):
    lib.destroy()

