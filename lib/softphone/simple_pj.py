import re
import threading

import pjsua as pj

import lib.logging_esi as logging_esi

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


# callback used by the pjsip/pjsua libraries for logging
def pjl_log_cb(level, _str, _len):
    log.debug(_str.strip())


class MyAccountCallback(pj.AccountCallback):

    sem = None
    call_info = None

    def __init__(self, acct_info):
        pj.AccountCallback.__init__(self)
        log.debug("MyAccountCallback.__init__(%s)" % acct_info)
        self.acct_info = acct_info

    def wait(self):
        self.sem = threading.Semaphore(0)
        self.sem.acquire()

    def on_reg_state(self):
        _info = self.account.info()
        log.debug("%s: on_reg_state - registration status = %s (%s)" % (_info.uri, _info.reg_status, _info.reg_reason))
        self.acct_info.reg_status = _info.reg_status
        if self.sem and self.acct_info.reg_status == 200:
            self.sem.release()
            self.sem = None

    def on_incoming_call(self, call):
        log.debug('on_incoming_call: acct_info = %s' % self.acct_info)
        self.acct_info.call = call
        call.set_callback(MyCallCallback(self.acct_info))
        # on_incoming_call_cb defaults to None, but it can designate an external callback to be called here
        if self.acct_info.on_incoming_call_cb:
            self.acct_info.on_incoming_call_cb(self.acct_info)


class MyCallCallback(pj.CallCallback):
    """Callback to receive events from Call"""
    def __init__(self, acct_info):
        pj.CallCallback.__init__(self, acct_info.call)
        self.acct_info = acct_info
        self.rec_slot = None
        self.rec_id = None
        self.player_id = None
        self.pb_slot = None
        self.old_pbfile = None
        self.acct_info.state = pj.CallState.NULL
        self.media_connected = False

    def _on_state(self):
        _info = self.acct_info.call.info()
        remote_uri = re.match('("[^"]*"\s+)?<?([^>]+)', _info.remote_uri).group(2)
        log.debug("%s: ci.remote_uri=%s state %s media_state %s" % (
            _info.uri, remote_uri, call_state_text[_info.state], media_state_text[_info.media_state]))
        if self.acct_info.state != _info.state:
            log.debug("%s: call transition %s --> %s" % (_info.uri, call_state_text[self.acct_info.state],
                                                         call_state_text[_info.state]))
            self.acct_info.state = _info.state
            if self.acct_info.state == pj.CallState.NULL or self.acct_info.state == pj.CallState.DISCONNECTED:
                self.acct_info.call = None
                self.acct_info.call_status = 'idle'
            elif self.acct_info.state == pj.CallState.EARLY:
                self.acct_info.call_status = 'early'
        if self.acct_info.media_state != _info.media_state:
            log.debug("%s: media transition %s --> %s" % (_info.uri, media_state_text[self.acct_info.media_state],
                                                          media_state_text[_info.media_state]))
            self.acct_info.media_state = _info.media_state
            if _info.state == pj.CallState.CONFIRMED:
                new_hold_state = self.acct_info.media_state != pj.MediaState.ACTIVE
                if self.acct_info.hold != new_hold_state:
                    log.debug("%s: hold transition %s --> %s" % (_info.uri, self.acct_info.hold, new_hold_state))
                    self.acct_info.hold = new_hold_state
                    if self.acct_info.hold:
                        self.acct_info.call_status = 'hold'
                    else:
                        self.acct_info.call_status = 'call'
        # on_state_cb defaults to None, but it can designate an external callback to be called here
        if self.acct_info.on_state_cb:
            self.acct_info.on_state_cb(self.acct_info)

    def on_state(self):
        with logging_esi.msg_src_cm('on_state'):
            self._on_state()

    def on_media_state(self):
        with logging_esi.msg_src_cm('on_media_state'):
            self._on_state()


class AccountInfo:

    def __init__(self, account):
        self.account = account
        self.account_cb = None
        self.state = pj.CallState.NULL
        self.media_state = pj.MediaState.NULL
        self.call_status = 'idle'
        self.reg_status = None
        self.call = None
        self.hold = False
        self.on_state_cb = None
        self.on_incoming_call_cb = None


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
            account_info = AccountInfo(account)
            account_info.account_cb = MyAccountCallback(account_info)
            account.set_callback(account_info.account_cb)
            account_infos[uri] = account_info
            account_info.account_cb.wait()
            return account_info

