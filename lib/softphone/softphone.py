from lib.softphone.pjsua_lib import lib, MyCallCallback as CallCb
from lib.common.user_exception import UserException as Ux
import Queue
import lib.common.logging_esi as logging_esi
from lib.common.wrappers import Trace
from time import time, sleep
from lib.softphone.wav_audio import create_wav_file
from lib.common.configure import cfg
import re
import random

log = logging_esi.get_logger('esi.softphone')
src_cfg = cfg.site['Accounts']['SoftphoneUser']
softphone = None


class Softphone:

    account = None
    uri = None
    status = None

    @Trace(log)
    def __init__(self, uri, proxy, passwd, pbfile, null_snd=False, tcp=False, dns_list=[]):
        lib.start(null_snd=null_snd, dns_list=dns_list, tcp=tcp)
        lib.set_gui_cmd_q(Queue.Queue())
        lib.connect_monitor(None)
        lib.set_wav_dir('wav/')
        self.uri = uri
        lib.set_pbfile_strings({self.uri: pbfile})
        self.account = lib.add_account(self.uri, proxy, passwd)

    @Trace(log)
    def wait_for_call_status(self, desired_status, timeout):
        start = time()
        cmd_q = lib.get_gui_cmd_q()
        while time() - start < timeout:
            if not cmd_q.empty():
                txt = cmd_q.get()
                log.debug("[wait_for_call_status] cmd_q: " + txt)
                m = re.match('call\s+(\S+)\s.*(sip:\d+@\S+).*(sip:\d+@\S+)', txt)
                if m:
                    self.status = m.group(1)
                    src_uri = m.group(2)
                    log.debug("[wait_for_call_status] %s status = %s" % (src_uri, self.status))
                    if self.status == desired_status and src_uri == self.uri:
                        log.debug("[wait_for_call_status] %s successfully reached status %s" % (self.uri, self.status))
                        # return how long the wait was, in case the caller wants to check
                        return time() - start
                    if self.status == 'call' and desired_status == 'early':
                        self.teardown_call()
                        raise Ux('wait for call status "early" terminated call because status was "call"')
                sleep(0.1)
        else:
            raise Ux('wait for call status "%s" timed out after %s seconds' % (desired_status, timeout))

    # using two soft phone accounts, have one call the other
    # then wait for the call status to verify both calls are set up
    @Trace(log)
    def make_call(self, _dst_uri):
        if self.account.info().reg_status != 200:
            raise Ux("Can't set up call, registration status (src) %s" % self.account.info().reg_status)
        log.debug("Calling %s" % _dst_uri)
        lib.get_current_calls()[self.uri] = self.account.make_call(_dst_uri, CallCb())

    @Trace(log)
    def leave_msg(self, length=None):
        if self.uri not in lib.get_current_calls():
            raise Ux("%s not in current_calls" % self.uri)
        sleep(10)
        lib.get_current_calls()[self.uri].dial_dtmf('2')
        if length is None:
            random.seed(time())
            length = random.randrange(10, 30, 1)
        sleep(length)

    @Trace(log)
    def teardown_call(self):
        if self.uri in lib.get_current_calls():
            call = lib.get_current_calls()[self.uri]
            # print "STATE = %d" % call.info().state
            call.hangup()
            log.debug("%s hanging up" % self.uri)
            log.debug("calling wait_for_call_status(%s, 'end', 15)" % self.uri)
            self.wait_for_call_status('disconnected', 15)

    @Trace(log)
    def dial_dtmf(self, dtmf_string):
        current_calls = lib.get_current_calls()
        if self.uri in current_calls:
            for c in list(dtmf_string):
                log.debug('%s:send dtmf %s' % (self.uri, c))
                current_calls[self.uri].dial_dtmf(c)
                sleep(0.3)

    @Trace(log)
    def set_monitor_on(self):
        lib.connect_monitor(self.uri)

    @Trace(log)
    def set_monitor_off(self):
        lib.connect_monitor(None)

def get_softphone():
    global softphone
    if softphone is None:
        user_cfg = cfg.site['Accounts']['SoftphoneUser']
        id = user_cfg['UserId']
        create_wav_file(user_cfg['pbfile'])
        domain = user_cfg['DomainName']
        uri = 'sip:%s@%s' % (id, domain)
        proxy = user_cfg['Proxy']
        passwd = user_cfg['Password']
        dns_list = user_cfg['dns_list']
        softphone = Softphone(uri, proxy, passwd, 'wav/2202.wav', dns_list=dns_list)
    return softphone

