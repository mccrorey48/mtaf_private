# softphone class that uses simple_pj
import random
import re
from time import time, sleep

import lib.logging_esi as logging_esi
from lib.wrappers import Trace

import lib.softphone.simple_pj as pj
from lib.softphone.wav_audio import create_wav_file
from lib.user_exception import UserException as Ux

log = logging_esi.get_logger('esi.softphone2')

softphones = {}


class SoftphoneConfig:
    def __init__(self, uri, proxy, password, null_snd=True, dns_list=None, tcp=False, pbfile=None, rec=True, quiet=True):
        self.uri = uri
        self.proxy = proxy
        self.password = password
        self.null_snd = null_snd
        self.tcp = tcp
        self.dns_list = dns_list
        self.pbfile = pbfile
        self.quiet = quiet
        self.rec = rec


class Softphone:

    lib = None
    pbfile = None
    dst_uri = None

    @Trace(log)
    def __init__(self, cfg):
        self.cfg = cfg
        if not self.lib:
            Softphone.lib = pj.PjsuaLib()
            self.lib.start(null_snd=self.cfg.null_snd, dns_list=self.cfg.dns_list, tcp=self.cfg.tcp)
        if self.cfg.pbfile:
            create_wav_file(self.cfg.pbfile, self.cfg.quiet)
        m = re.match('sip:([^@]+)@(.+)', self.cfg.uri)
        if m:
            self.lib.add_account(m.group(1), m.group(2), self.cfg.proxy, self.cfg.password)
            self.account_info = pj.account_infos[self.cfg.uri]

    @Trace(log)
    def wait_for_call_status(self, desired_status, timeout=30):
        # possible desired_status values: 'call', 'idle', 'early', 'hold'
        start = time()
        while time() - start < timeout:
            if self.account_info.call_status == desired_status:
                return time() - start
            sleep(0.1)
            if self.account_info.call_status == 'call' and desired_status == 'early':
                self.teardown_call()
                raise Ux('wait for call status "early" terminated call because status was "call"')
        else:
            raise Ux('wait for call status "%s" timed out after %s seconds' % (desired_status, timeout))

    @Trace(log)
    def make_call(self, dst_uri):
        self.dst_uri = dst_uri
        if self.account_info.reg_status != 200:
            raise Ux("Can't set up call, registration status (src) %s" % self.account_info.reg_status)
        log.debug("%s calling %s" % (self.cfg.uri, self.dst_uri))
        # print self.dst_uri
        self.account_info.call = self.account_info.account.make_call(self.dst_uri)
        self.account_info.call.set_callback(pj.MyCallCallback(self.account_info))

    @Trace(log)
    def end_call(self):
        if not self.account_info.call:
            raise Ux("end_call(): %s not in call" % self.cfg.uri)
        log.debug("%s ending call to %s" % (self.cfg.uri, self.dst_uri))
        self.account_info.call.hangup()

    @Trace(log)
    def leave_msg(self, length=None):
        if not self.account_info.call:
            raise Ux("leave_msg(): %s not in call" % self.cfg.uri)
        sleep(10)
        self.account_info.call.dial_dtmf('2')
        if length is None:
            random.seed(time())
            length = random.randrange(10, 30, 1)
        sleep(length)

    def teardown_call(self):
        if self.account_info.call:
            self.account_info.call.hangup()
            log.debug("%s hanging up" % self.cfg.uri)
            log.debug("calling wait_for_call_status(%s, 'end', 15)" % self.cfg.uri)
            self.wait_for_call_status('disconnected', 15)

    @Trace(log)
    def dial_dtmf(self, dtmf_string):
        if self.account_info.call:
            for c in list(dtmf_string):
                log.debug('%s:send dtmf %s' % (self.cfg.uri, c))
                self.account_info.call.dial_dtmf(c)
                sleep(0.3)

    @Trace(log)
    def set_monitor_on(self):
        pass

    @Trace(log)
    def set_monitor_off(self):
        pass
