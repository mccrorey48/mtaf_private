from time import time, sleep
import lib.softphone.simple_pj as pj
import lib.logging_esi as logging_esi
import random

log = logging_esi.get_logger('esi.simple_pj_test')
# set console log level
logging_esi.console_handler.setLevel(logging_esi.INFO)


def on_incoming_call_cb(acct_info):
    uri = acct_info.account.info().uri
    log.info('%s:  (ignoring)' % uri)
    # to auto-answer, send 200 OK
    # acct.call.answer(200)


def on_state_cb(acct_info):
    state = pj.call_state_text[acct_info.state]
    media_state = pj.media_state_text[acct_info.media_state]
    uri = acct_info.account.info().uri
    log.info('on_state_cb: uri=%s, state=%s, media_state=%s' % (uri, state, media_state))
    if acct_info.call == None:
        acct_info.dst_uri = None

lib = pj.PjsuaLib()


class Softphone:
    def __init__(self, number, domain, proxy, password):
        self.uri = 'sip:%s@%s' % (number, domain)
        self.account_info = lib.add_account(number, domain, proxy, password)
        self.dst_uri = None

    def set_on_state_cb(self, cb):
        self.account_info.on_state_cb = cb

    def set_on_incoming_call_cb(self, cb):
        self.account_info.on_incoming_call_cb = cb

    def make_call(self, dst_uri):
        log.debug("%s calling %s" % (self.uri, dst_uri))
        self.account_info.call = self.account_info.account.make_call(dst_uri)
        self.dst_uri = dst_uri
        self.account_info.call.set_callback(pj.MyCallCallback(self.account_info))

    def end_call(self):
        if self.account_info.call:
            log.debug("%s ending call to %s" % (self.uri, self.dst_uri))
            self.account_info.call.hangup()
        else:
            log.warn("end_call(): %s not in call" % self.uri)

    def leave_msg(self, length=None):
        if not self.account_info.call:
            log.warn("leave_msg(): %s not in call" % self.uri)
        sleep(10)
        self.account_info.call.dial_dtmf('2')
        if length is None:
            random.seed(time())
            length = random.randrange(10, 30, 1)
        sleep(length)

    def get_call(self):
        return self.account_info.call

    def get_uri(self):
        return self.uri

    def wait_for_call_status(self, desired_status, timeout=30):
        # possible desired_status values: 'call', 'idle', 'early', 'hold'
        start = time()
        while time() - start < timeout:
            if self.account_info.call_status == desired_status:
                return time() - start
            sleep(0.1)
            if self.account_info.call_status == 'call' and desired_status == 'early':
                self.teardown_call()
                log.warn('wait for call status "early" terminated call because status was "call"')
        else:
            log.warn('wait for call status "%s" timed out after %s seconds' % (desired_status, timeout))

    def teardown_call(self):
        if self.account_info.call:
            self.account_info.call.hangup()
            log.debug("%s hanging up" % self.uri)
            log.debug("calling wait_for_call_status(%s, 'end', 15)" % self.uri)
            self.wait_for_call_status('disconnected', 15)

    def dial_dtmf(self, dtmf_string):
        if self.account_info.call:
            for c in list(dtmf_string):
                log.debug('%s:send dtmf %s' % (self.uri, c))
                self.account_info.call.dial_dtmf(c)
                sleep(0.3)

log.debug('starting pjsua library')
with logging_esi.msg_src_cm('start pjsua'):
    lib.start(dns_list=['10.0.50.156', '10.0.50.157'])
log.debug('adding accounts')
with logging_esi.msg_src_cm('add accounts'):
    caller = Softphone('2202', 'test2.test-eng.com', 'nr5.cpbx.esihs.net', 'vsvSIHpL')
    called = Softphone('2203', 'test2.test-eng.com', 'nr5.cpbx.esihs.net', 'TSDlprSD')
    caller.set_on_state_cb(on_state_cb)
    called.set_on_state_cb(on_state_cb)
    caller.set_on_incoming_call_cb = on_incoming_call_cb
    called.set_on_incoming_call_cb = on_incoming_call_cb
log.debug('making a call from 2202 to 2203')
with logging_esi.msg_src_cm('make call'):
    caller.make_call(called.get_uri())
    for i in range(0, 20, 2):
        if called.get_call():
            if i < 10:
                log.debug('[%d] called ringing (180)' % i)
                called.get_call().answer(180)
            if i == 12:
                log.debug('[%d] called answering (200)' % i)
                called.get_call().answer(200)
            if i == 20:
                log.debug('[%d] called hanging up' % i)
                caller.get_call().hangup()
        sleep(2)
    log.debug('caller hanging up')
    caller.get_call().hangup()
log.debug('destroying pjsua library')
with logging_esi.msg_src_cm('destroy pjsua'):
    lib.destroy()

