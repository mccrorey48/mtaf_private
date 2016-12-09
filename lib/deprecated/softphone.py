import Queue
import random
import re
from time import time, sleep

import lib.deprecated.pjsua_lib as pjl
import lib.logging_esi as logging_esi
from ePhone7.utils.configure import cfg
from lib.softphone.wav_audio import create_wav_file
from lib.user_exception import UserException as Ux
from lib.wrappers import Trace

log = logging_esi.get_logger('esi.softphone')

softphones = {}


def Softphone(user_cfg):
    uri = 'sip:%s@%s' % (user_cfg['UserId'], user_cfg['DomainName'])
    if uri in softphones:
        return softphones[uri]
    else:
        softphone = _Softphone(user_cfg)
        softphones[uri] = softphone
        return softphone


class _Softphone:

    account = None
    uri = None
    status = None
    pjl = None
    cmd_q = None
    dst_uri = None

    @Trace(log)
    def __init__(self, user_cfg):
        pbfile = user_cfg['pbfile']
        create_wav_file(pbfile, cfg.site['Quiet'])
        uri = 'sip:%s@%s' % (user_cfg['UserId'], user_cfg['DomainName'])
        proxy = user_cfg['Proxy']
        passwd = user_cfg['Password']
        if len(softphones) == 0:
            pjl.lib.start(null_snd=cfg.site['NullSound'], dns_list=cfg.site['DnsList'], tcp=cfg.site['UseTcp'])
            pjl.lib.connect_monitor(None)
            pjl.cmd_q = Queue.Queue()
        self.pjl = pjl
        self.cmd_q = pjl.cmd_q
        self.uri = uri
        self.pjl.pbfile_strings[self.uri] = pbfile
        self.account = self.pjl.lib.add_account(self.uri, proxy, passwd)

    def __del__(self):
        if self.uri in self.pjl.current_calls:
            self.pjl.current_calls[self.uri].hangup()

    @Trace(log)
    def wait_for_call_status(self, desired_status, timeout):
        start = time()
        while time() - start < timeout:
            if self.cmd_q.empty():
                sleep(0.1)
            else:
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
