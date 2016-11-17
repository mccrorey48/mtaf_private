import re
import threading
import random
from lib.wrappers import Trace
from lib.user_exception import UserException as Ux, UserTimeoutException as Tx
import pjsua as pj
from lib.softphone.wav_audio import create_wav_file
import lib.logging_esi as logging_esi
from time import time, sleep

log = logging_esi.get_logger('esi.simple_pj')
# set console log level
logging_esi.console_handler.setLevel(logging_esi.INFO)

account_infos = {}

media_state_text = {
    pj.MediaState.NULL: 'NULL',
    pj.MediaState.ACTIVE: 'ACTIVE',
    pj.MediaState.LOCAL_HOLD: 'LOCAL HOLD',
    pj.MediaState.REMOTE_HOLD: 'REMOTE HOLD',
    pj.MediaState.ERROR: 'ERROR'
}

call_state_text = {
    pj.CallState.NULL: "NULL",
    pj.CallState.CALLING: "CALLING",
    pj.CallState.INCOMING: "INCOMING",
    pj.CallState.EARLY: "EARLY",
    pj.CallState.CONNECTING: "CONNECTING",
    pj.CallState.CONFIRMED: "CONFIRMED",
    pj.CallState.DISCONNECTED: "DISCONNECTED"
}


# callback to be used by the pjsip/pjsua C libraries for logging
def pjl_log_cb(level, _str, _len):
    sip_match = re.match('.*(Request|Response)', _str)
    lines = ["log_cb(%d): %s" % (level, line) for line in _str.splitlines()]
    if level == 1:
        for line in lines:
            log.warn(line)
    elif level == 2:
        for line in lines:
            log.info(line)
    elif sip_match:
        log.trace(lines[0])
        for line in lines:
            log.debug(line)
    else:
        for line in lines:
            log.debug(line)


class Softphone:

    lib = None
    pbfile = None
    dst_uri = None
    rec_id = None
    rec_slot = None

    @Trace(log)
    def __init__(self, uri, proxy, password, null_snd=True, dns_list=None, tcp=False,
                 pbfile=None, rec=True, quiet=True):
        self.uri = uri
        self.pbfile = pbfile
        if not self.lib:
            Softphone.lib = PjsuaLib()
            self.lib.start(null_snd=null_snd, dns_list=dns_list, tcp=tcp)
        if self.pbfile:
            create_wav_file(self.pbfile, quiet)
        m = re.match('sip:([^@]+)@(.+)', self.uri)
        if m:
            self.lib.add_account(m.group(1), m.group(2), proxy, password)
            self.account_info = account_infos[self.uri]

    @Trace(log)
    def wait_for_call_status(self, desired_status, timeout=20, warn_only=False):
        # possible desired_status values: 'call', 'idle', 'early', 'hold'
        start = time()
        while time() - start < timeout:
            log.debug("%s: call status is %s" % (self.uri, self.account_info.call_status))
            if self.account_info.call_status == desired_status:
                return time() - start
            sleep(0.1)
            if self.account_info.call_status == 'call' and desired_status == 'early':
                self.teardown_call()
                raise Ux('wait for call status "early" terminated call because status was "call"')
        else:
            if warn_only:
                log.warn('wait for call status "%s" timed out after %s seconds' % (desired_status, timeout))
            else:
                raise Tx('wait for call status "%s" timed out after %s seconds' % (desired_status, timeout))

    @Trace(log)
    def make_call(self, dst_uri, dst_response=None):
        self.dst_uri = dst_uri
        account_infos[dst_uri].incoming_response = dst_response
        if self.account_info.reg_status != 200:
            raise Ux("Can't set up call, registration status (src) %s" % self.account_info.reg_status)
        log.debug("%s calling %s" % (self.uri, self.dst_uri))
        self.account_info.call = self.account_info.account.make_call(self.dst_uri)
        self.account_info.call.set_callback(MyCallCallback(self.account_info))

    @Trace(log)
    def end_call(self, timeout=10):
        if not self.account_info.call:
            raise Ux("end_call(): %s not in call" % self.uri)
        log.debug("%s ending call to %s" % (self.uri, self.dst_uri))
        self.account_info.call.hangup()
        self.wait_for_call_status('idle', timeout)

    @Trace(log)
    def hold(self, timeout=10):
        if not self.account_info.call:
            raise Ux("end_call(): %s not in call" % self.uri)
        log.debug("%s ending call to %s" % (self.uri, self.dst_uri))
        self.account_info.call.hold()
        self.wait_for_call_status('hold', timeout)

    @Trace(log)
    def unhold(self, timeout=10):
        if not self.account_info.call:
            raise Ux("end_call(): %s not in call" % self.uri)
        log.debug("%s ending call to %s" % (self.uri, self.dst_uri))
        self.account_info.call.unhold()
        self.wait_for_call_status('call', timeout)

    @Trace(log)
    def send_response_code(self, code):
        if not self.account_info.call:
            raise Ux("leave_msg(): %s not in call" % self.uri)
        self.account_info.call.answer(code)

    @Trace(log)
    def leave_msg(self, length=None):
        if not self.account_info.call:
            raise Ux("leave_msg(): %s not in call" % self.uri)
        sleep(10)
        self.account_info.call.dial_dtmf('2')
        if length is None:
            random.seed(time())
            length = random.randrange(10, 30, 1)
        sleep(length)

    @Trace(log)
    def dial_dtmf(self, dtmf_string):
        if self.account_info.call:
            for c in list(dtmf_string):
                log.debug('%s:send dtmf %s' % (self.uri, c))
                self.account_info.call.dial_dtmf(c)
                sleep(0.3)

    @Trace(log)
    def set_monitor_on(self):
        pass

    @Trace(log)
    def set_monitor_off(self):
        pass


class MyAccountCallback(pj.AccountCallback):

    sem = None
    call_info = None

    def __init__(self, acct_info):
        pj.AccountCallback.__init__(self)
        log.debug("MyAccountCallback.__init__(%s)" % acct_info)
        self.acct_info = acct_info
        pass

    def wait(self):
        self.sem = threading.Semaphore(0)
        self.sem.acquire()

    def on_reg_state(self):
        reg_info = self.account.info()
        log.debug("%s: on_reg_state - registration status = %s (%s)" % (reg_info.uri, reg_info.reg_status,
                                                                        reg_info.reg_reason))
        self.acct_info.reg_status = reg_info.reg_status
        if self.sem and self.acct_info.reg_status == 200:
            self.sem.release()
            self.sem = None

    def on_incoming_call(self, call):
        log.debug('on_incoming_call: acct_info = %s' % self.acct_info)
        self.acct_info.call = call
        call.set_callback(MyCallCallback(self.acct_info))
        # on_incoming_call_cb defaults to None, but it can designate an external callback to be called here
        if self.acct_info.incoming_response:
            call.answer(self.acct_info.incoming_response)


# look up new_call_states[old_state][(call_state, media_state)]
# to get a dictionary that will contain 'new_state' and might contain 'media actions'
new_call_statuses = {
    'idle': {
        (pj.CallState.CONFIRMED, pj.MediaState.ACTIVE): {'status': 'call', 'actions': ['create_media', 'connect_media']},
        (pj.CallState.CONFIRMED, pj.MediaState.NULL): {'status': 'error'},
        (pj.CallState.EARLY, pj.MediaState.ACTIVE): {'status': 'early'},
        (pj.CallState.EARLY, pj.MediaState.NULL): {'status': 'early'},
        (pj.CallState.INCOMING, pj.MediaState.ACTIVE): {'status': 'idle'},
        (pj.CallState.INCOMING, pj.MediaState.NULL): {'status': 'idle'},
        (pj.CallState.CONNECTING, pj.MediaState.ACTIVE): {'status': 'idle'},
        (pj.CallState.CONNECTING, pj.MediaState.NULL): {'status': 'idle'},
        (pj.CallState.DISCONNECTED, pj.MediaState.ACTIVE): {'status': 'idle'},
        (pj.CallState.DISCONNECTED, pj.MediaState.NULL): {'status': 'idle'},
    },
    'early': {
        (pj.CallState.CONFIRMED, pj.MediaState.ACTIVE): {'status': 'call', 'actions': ['create_media', 'connect_media']},
        (pj.CallState.CONFIRMED, pj.MediaState.NULL): {'status': 'early'},
        (pj.CallState.EARLY, pj.MediaState.ACTIVE): {'status': 'early'},
        (pj.CallState.EARLY, pj.MediaState.NULL): {'status': 'early'},
        (pj.CallState.CONNECTING, pj.MediaState.ACTIVE): {'status': 'early'},
        (pj.CallState.CONNECTING, pj.MediaState.NULL): {'status': 'early'},
        (pj.CallState.DISCONNECTED, pj.MediaState.ACTIVE): {'status': 'idle'},
        (pj.CallState.DISCONNECTED, pj.MediaState.NULL): {'status': 'idle'},
    },
    'call': {
        (pj.CallState.CONFIRMED, pj.MediaState.ACTIVE): {'status': 'call'},
        (pj.CallState.CONFIRMED, pj.MediaState.NULL): {'status': 'hold', 'actions': ['disconnect_media']},
        (pj.CallState.EARLY, pj.MediaState.ACTIVE): {'status': 'error'},
        (pj.CallState.EARLY, pj.MediaState.NULL): {'status': 'error'},
        (pj.CallState.CONNECTING, pj.MediaState.ACTIVE): {'status': 'error'},
        (pj.CallState.CONNECTING, pj.MediaState.NULL): {'status': 'error'},
        (pj.CallState.DISCONNECTED, pj.MediaState.ACTIVE): {'status': 'idle', 'actions': [
            'disconnect_media', 'destroy_media', 'end_call']},
        (pj.CallState.DISCONNECTED, pj.MediaState.NULL): {'status': 'idle', 'actions': [
            'disconnect_media', 'destroy_media', 'end_call']}
    },
    'hold': {
        (pj.CallState.CONFIRMED, pj.MediaState.ACTIVE): {'status': 'call', 'actions': ['connect_media']},
        (pj.CallState.CONFIRMED, pj.MediaState.NULL): {'status': 'hold'},
        (pj.CallState.EARLY, pj.MediaState.ACTIVE): {'status': 'error'},
        (pj.CallState.EARLY, pj.MediaState.NULL): {'status': 'error'},
        (pj.CallState.CONNECTING, pj.MediaState.ACTIVE): {'status': 'error'},
        (pj.CallState.CONNECTING, pj.MediaState.NULL): {'status': 'error'},
        (pj.CallState.DISCONNECTED, pj.MediaState.ACTIVE): {'status': 'idle', 'actions': [
            'destroy_media', 'end_call']},
        (pj.CallState.DISCONNECTED, pj.MediaState.NULL): {'status': 'idle', 'actions': [
            'destroy_media', 'end_call']}
    },
}


class MyCallCallback(pj.CallCallback):
    """Callback to receive events from Call"""
    def __init__(self, acct_info):
        pj.CallCallback.__init__(self, acct_info.call)
        self.acct_info = acct_info
        self.rec_slot = None
        self.rec_id = None
        self.pb_id = None
        self.pb_slot = None
        self.acct_info.state = pj.CallState.NULL
        self.media_connected = False

    def _on_state(self):
        media_ops = {
            'create_media': self.create_media,
            'connect_media': self.connect_media,
            'disconnect_media': self.disconnect_media,
            'destroy_media': self.destroy_media,
            'end_call': self.end_call
        }
        call_info = self.acct_info.call.info()
        remote_uri = re.match('("[^"]*"\s+)?<?([^>]+)', call_info.remote_uri).group(2)
        self.acct_info.state = call_info.state
        self.acct_info.media_state = call_info.media_state
        log.debug("%s: ci.remote_uri=%s state %s media_state %s" % (
            call_info.uri, remote_uri, call_state_text[call_info.state], media_state_text[call_info.media_state]))
        new_call_status = new_call_statuses[self.acct_info.call_status][(call_info.state, call_info.media_state)]
        self.acct_info.call_status = new_call_status['status']
        if 'actions' in new_call_status:
            for action in new_call_status['actions']:
                media_ops[action]()

    def on_state(self):
        with logging_esi.msg_src_cm('on_state'):
            self._on_state()

    def on_media_state(self):
        with logging_esi.msg_src_cm('on_media_state'):
            self._on_state()

    @Trace(log)
    def create_media(self):
        log.info("%s: called create_media" % self.acct_info.uri)

    @Trace(log)
    def destroy_media(self):
        log.info("%s: called destroy_media" % self.acct_info.uri)

    @Trace(log)
    def disconnect_media(self):
        log.info("%s: called disconnect_media" % self.acct_info.uri)

    @Trace(log)
    def end_call(self):
        log.info("%s: called end_call" % self.acct_info.uri)
        self.acct_info.call = None

    @Trace(log)
    def connect_media(self):
        log.info("%s: called connect_media" % self.acct_info.uri)
        # if self.rec_id is None:
        #     raise Ux("connect_media: no media exists")
        # self.rec_slot = self.lib.recorder_get_slot(self.rec_id)
        # my_uri = self.call.info().account.info().uri
        #     # self.media_call_slot is set to the call's conference slot when connecting media,
        #     # and set to None when disconnecting, so if it is not None, this is a reconnect
        #     if self.media_call_slot is not None:
        #         # if self.media_call_slot is not None but is not the current call's conference slot,
        #         # it isn't a reconnect, it's a structural program error
        #         if self.media_call_slot != self.call.info().conf_slot:
        #             raise Ux("connect_media: call at slot %d media already connected to call slot %d"
        #                      % (self.call.info().conf_slot, self.media_call_slot))
        #         log.debug("%s: disconnecting call slot %d from recorder %s at slot %d"
        #                   % (my_uri, self.media_call_slot, self.rec_id, self.rec_slot))
        #         lib.conf_disconnect(self.media_call_slot, self.rec_slot)
        #         if self.pb_id is not None:
        #             self.pb_slot = lib.player_get_slot(self.pb_id)
        #             log.debug("%s: disconnecting player %s at slot %d to call slot %d"
        #                       % (my_uri, self.pb_id, self.pb_slot, self.media_call_slot))
        #             lib.conf_disconnect(self.pb_slot, self.media_call_slot)
        #         self.media_call_slot = None
        #     log.debug("%s: connecting call slot %d to recorder %s at slot %d"
        #               % (my_uri, self.call.info().conf_slot, self.rec_id, self.rec_slot))
        #     lib.conf_connect(self.call.info().conf_slot, self.rec_slot)
        #     # if there is a player ID then the player was created during create_media and we can connect it, too
        #     if self.pb_id is not None:
        #         self.pb_slot = lib.player_get_slot(self.pb_id)
        #         log.debug("%s: connecting player %s at slot %d to call slot %d"
        #                   % (my_uri, self.pb_id, self.pb_slot, self.call.info().conf_slot))
        #         lib.conf_connect(self.pb_slot, self.call.info().conf_slot)
        #     self.media_call_slot = self.call.info().conf_slot


class MyAccountInfo:

    def __init__(self, account):
        self.account = account
        self.uri = None
        self.state = pj.CallState.NULL
        self.media_state = pj.MediaState.NULL
        self.call_status = 'idle'
        self.reg_status = None
        self.call = None
        self.hold = False
        self.incoming_response = None


class PjsuaLib(pj.Lib):

    def __init__(self, quality=10, tx_drop_pct=0, rx_drop_pct=0):
        pj.Lib.__init__(self)
        self.quality = quality
        self.tx_drop_pct = tx_drop_pct
        self.rx_drop_pct = rx_drop_pct
        self.tcp = False

    def __del__(self):
        pass

    def start(self, log_cb=pjl_log_cb, null_snd=False, tcp=False, dns_list=None):
        self.tcp = tcp
        my_ua_cfg = pj.UAConfig()
        my_ua_cfg.max_calls = 8
        my_media_cfg = pj.MediaConfig()
        my_media_cfg.tx_drop_pct = self.tx_drop_pct
        my_media_cfg.rx_drop_pct = self.rx_drop_pct
        my_media_cfg.quality = self.quality
        my_media_cfg.ptime = 20
        if dns_list:
            my_ua_cfg.nameserver = dns_list
        self.init(log_cfg=pj.LogConfig(level=4, callback=log_cb), ua_cfg=my_ua_cfg, media_cfg=my_media_cfg)
        if self.tcp:
            transport = self.create_transport(pj.TransportType.TCP, pj.TransportConfig())
        else:
            transport = self.create_transport(pj.TransportType.UDP, pj.TransportConfig())
        log.debug("Listening on %s:%s" % (transport.info().host, transport.info().port))
        pj.Lib.start(self)
        if null_snd:
            self.set_null_snd_dev()
        self.set_codec_priority('PCMU/8000/1', 150)
        self.set_codec_priority('PCMU/8000/1', 149)
        self.set_codec_priority('G722/16000/1', 148)

    def add_account(self, number, domain, proxy, pw):
        uri = "sip:%s@%s" % (number, domain)
        if uri in account_infos:
            log.warn('%s: account already created' % uri)
        else:
            acc_cfg = pj.AccountConfig()
            acc_cfg.id = uri
            acc_cfg.reg_uri = "sip:%s" % proxy
            acc_cfg.proxy = ["sip:%s" % proxy]
            acc_cfg.allow_contact_rewrite = False
            acc_cfg.auth_cred = [pj.AuthCred(realm="*", username=number, passwd=pw)]
            account = self.create_account(acc_cfg)
            account_info = MyAccountInfo(account)
            account_info.uri = uri
            account_infos[uri] = account_info
            account_cb = MyAccountCallback(account_info)
            account.set_callback(account_cb)
            account_cb.wait()
            return account_info

