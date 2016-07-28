import lib.softphone.pjsua_lib as pjl
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
softphones = {}


class Softphone:

    account = None
    uri = None
    status = None
    pjl = None
    cmd_q = None
    dst_uri = None


    @Trace(log)
    def __init__(self, user_name, null_snd, tcp):
        user_cfg = cfg.site['Accounts'][user_name]
        pbfile = user_cfg['pbfile']
        create_wav_file(pbfile)
        uri = 'sip:%s@%s' % (user_cfg['UserId'], user_cfg['DomainName'])
        proxy = user_cfg['Proxy']
        passwd = user_cfg['Password']
        if len(softphones) == 0:
            pjl.lib.start(null_snd=null_snd, dns_list=user_cfg['dns_list'], tcp=tcp)
            pjl.lib.connect_monitor(None)
            pjl.cmd_q = Queue.Queue()
        self.pjl = pjl
        self.cmd_q = pjl.cmd_q
        self.uri = uri
        self.pjl.pbfile_strings[self.uri] = pbfile
        self.account = self.pjl.lib.add_account(self.uri, proxy, passwd)
        softphones[user_name] = self

    def __del__(self):
        if self.uri in self.pjl.current_calls:
            self.pjl.current_calls[self.uri].hangup()

    @Trace(log)
    def wait_for_call_status(self, desired_status, timeout):
        start = time()
        while time() - start < timeout:
            if not self.cmd_q.empty():
                txt = self.cmd_q.get()
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

    @Trace(log)
    def make_call(self, dst_uri):
        self.dst_uri = dst_uri
        if self.account.info().reg_status != 200:
            raise Ux("Can't set up call, registration status (src) %s" % self.account.info().reg_status)
        log.debug("%s calling %s" % (self.uri, self.dst_uri))
        self.pjl.current_calls[self.uri] = self.account.make_call(self.dst_uri, self.pjl.MyCallCallback())

    @Trace(log)
    def end_call(self):
        if self.uri not in self.pjl.current_calls:
            raise Ux("end_call(): %s not in current_calls" % self.uri)
        log.debug("%s ending call to %s" % (self.uri, self.dst_uri))
        self.pjl.current_calls[self.uri].hangup()

    @Trace(log)
    def leave_msg(self, length=None):
        if self.uri not in self.pjl.current_calls:
            raise Ux("leave_msg(): %s not in current_calls" % self.uri)
        sleep(10)
        self.pjl.current_calls[self.uri].dial_dtmf('2')
        if length is None:
            random.seed(time())
            length = random.randrange(10, 30, 1)
        sleep(length)

    def teardown_call(self):
        if self.uri in self.pjl.current_calls:
            call = self.pjl.current_calls[self.uri]
            # print "STATE = %d" % call.info().state
            call.hangup()
            log.debug("%s hanging up" % self.uri)
            log.debug("calling wait_for_call_status(%s, 'end', 15)" % self.uri)
            self.wait_for_call_status('disconnected', 15)

    @Trace(log)
    def dial_dtmf(self, dtmf_string):
        if self.uri in self.pjl.current_calls:
            for c in list(dtmf_string):
                log.debug('%s:send dtmf %s' % (self.uri, c))
                self.pjl.current_calls[self.uri].dial_dtmf(c)
                sleep(0.3)

    @Trace(log)
    def set_monitor_on(self):
        self.pjl.lib.connect_monitor(self.uri)

    @Trace(log)
    def set_monitor_off(self):
        self.pjl.lib.connect_monitor(None)


def get_softphone(user_name=None, null_snd=False, tcp=False):
    if user_name is None:
        user_name = cfg.site["DefaultSoftphoneUser"]
    if user_name in softphones:
        return softphones[user_name]
    else:
        return Softphone(user_name, null_snd, tcp)

